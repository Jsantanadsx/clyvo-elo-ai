"""Cenários controlados de QA: regras, API e integração simulada do CLIENTE OpenAI.

Importante: client mockado testa o contrato de integração, não comprova chamada externa.
"""
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.ai_service import gerar_orientacao, validar_orientacao, IAIndisponivel, AVISO
from app.rules import analisar_dados

ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def ler(nome):
    return json.loads((ROOT / 'data' / ('cenario_' + nome + '.json')).read_text(encoding='utf-8'))


@pytest.fixture(autouse=True)
def sem_token_configurado(monkeypatch):
    monkeypatch.delenv('CLYVO_API_TOKEN', raising=False)
    # Os testes funcionais usam somente demonstração local explícita.
    monkeypatch.setenv('CLYVO_LOCAL_DEMO', 'true')


def test_CT01_cenario_normal_sem_alertas():
    r = client.post('/api/alertas', json=ler('normal'))
    assert r.status_code == 200
    assert r.json()['quantidade_alertas'] == 0
    assert r.json()['ia_generativa_utilizada'] is False


def test_CT02_cenario_alerta_quatro_alertas_classificados():
    r = client.post('/api/alertas', json=ler('alerta'))
    assert r.status_code == 200
    assert [(a['tipo'], a['prioridade']) for a in r.json()['alertas']] == [
        ('NIVEL_AGUA', 'ALTA'), ('NIVEL_RACAO', 'MEDIA'),
        ('TEMPERATURA', 'ALTA'), ('UMIDADE', 'MEDIA')]


def test_CT03_pos_operatorio_alertas_e_contexto():
    dados = ler('pos_operatorio')
    r = client.post('/api/alertas', json=dados)
    assert r.status_code == 200
    assert [x['tipo'] for x in r.json()['alertas']] == [
        'NIVEL_AGUA', 'NIVEL_RACAO', 'ACOMPANHAMENTO_CLINICO']


def test_CT04_dados_sensor_invalidos_rejeitados():
    dados = ler('alerta')
    dados['sensores']['umidade'] = 150
    r = client.post('/api/alertas', json=dados)
    assert r.status_code == 422


def test_CT05_servico_sem_chave_nao_simula_ia(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    r = client.post('/api/analisar', json=ler('normal'))
    assert r.status_code == 503
    assert 'OPENAI_API_KEY' in r.json()['detail']


def test_CT06_integracao_modelo_com_cliente_simulado(monkeypatch):
    """Mock comprova envio de contexto e uso da resposta, não substitui teste real."""
    monkeypatch.setenv('OPENAI_MODEL', 'gpt-4o-mini')
    fake = Mock()
    fake.responses.create.return_value = SimpleNamespace(
        output_text='O recipiente de água está com nível baixo. Confira o abastecimento.'
    )
    dados = ler('alerta')
    alertas = analisar_dados(dados)
    resposta = gerar_orientacao(dados, alertas, client=fake)
    fake.responses.create.assert_called_once()
    params = fake.responses.create.call_args.kwargs
    assert params['model'] == 'gpt-4o-mini'
    assert params['store'] is False
    assert json.loads(params['input'])['alertas_classificados'] == alertas
    assert 'Confira o abastecimento.' in resposta
    assert AVISO in resposta


def test_CT07_token_servidor_protege_analise(monkeypatch):
    monkeypatch.setenv('CLYVO_API_TOKEN', 'token-exemplo-teste')
    r = client.post('/api/alertas', json=ler('normal'))
    assert r.status_code == 401
    r2 = client.post('/api/alertas', json=ler('normal'),
                     headers={'X-CLYVO-TOKEN': 'token-exemplo-teste'})
    assert r2.status_code == 200


def test_CT08_cenario_inexistente_404():
    r = client.get('/api/cenarios/inexistente')
    assert r.status_code == 404


def test_CT09_endpoint_ia_com_provedor_substituido(monkeypatch):
    """Teste da camada HTTP com stub: não equivale a chamada real à OpenAI."""
    monkeypatch.setattr('app.api.gerar_orientacao', lambda dados, alertas: 'Orientação sintética de teste.')
    r = client.post('/api/analisar', json=ler('alerta'))
    assert r.status_code == 200
    assert r.json()['orientacao'] == 'Orientação sintética de teste.'
    assert r.json()['ia_generativa_utilizada'] is True
    assert r.json()['quantidade_alertas'] == 4


def test_CT10_interface_disponivel():
    r = client.get('/')
    assert r.status_code == 200
    assert 'CLYVO' in r.text
    assert 'Gerar orientação com IA' in r.text


# Regressões do Code Review PR #1 (Sprint 4)

def test_CT11_sem_token_e_sem_demo_falha_fechado(monkeypatch):
    monkeypatch.delenv('CLYVO_LOCAL_DEMO', raising=False)
    r = client.post('/api/alertas', json=ler('normal'))
    assert r.status_code == 503
    assert 'Autenticação' in r.json()['detail']


def test_CT12_com_token_exige_autorizacao_mesmo_em_demo(monkeypatch):
    monkeypatch.setenv('CLYVO_API_TOKEN', 'segredo-de-teste')
    assert client.post('/api/analisar', json=ler('normal')).status_code == 401
    assert client.post('/api/alertas', json=ler('normal'),
                       headers={'X-CLYVO-TOKEN': 'token-errado'}).status_code == 401
    assert client.post('/api/alertas', json=ler('normal'),
                       headers={'X-CLYVO-TOKEN': 'segredo-de-teste'}).status_code == 200


def test_CT13_demo_local_nao_abre_acesso_externo(monkeypatch):
    monkeypatch.setenv('CLYVO_LOCAL_DEMO', 'true')
    remoto = TestClient(app, client=('203.0.113.10', 50000))
    assert remoto.post('/api/alertas', json=ler('normal')).status_code == 503


def test_CT14_tipo_evento_case_insensitive_normalizado():
    dados = ler('pos_operatorio')
    dados['evento_clinico']['tipo'] = 'pos-operatorio'
    r = client.post('/api/alertas', json=dados)
    assert r.status_code == 200
    assert r.json()['quantidade_alertas'] == 3
    assert r.json()['alertas'][-1]['tipo'] == 'ACOMPANHAMENTO_CLINICO'


def test_CT15_tipo_evento_desconhecido_rejeitado():
    dados = ler('pos_operatorio')
    dados['evento_clinico']['tipo'] = 'evento-inventado'
    assert client.post('/api/alertas', json=dados).status_code == 422


def test_CT16_saida_com_dosagem_rejeitada():
    with pytest.raises(IAIndisponivel, match='validação'):
        validar_orientacao('Administre 10 mg de antibiótico ao pet.')


def test_CT17_saida_com_diagnostico_rejeitada():
    with pytest.raises(IAIndisponivel, match='validação'):
        validar_orientacao('O pet tem leptospirose.')


def test_CT18_saida_preventiva_permitida():
    txt = 'Confira o recipiente de água e contate a clínica se tiver dúvidas.'
    assert validar_orientacao(txt) == txt


def test_CT19_falha_provedor_gera_erro_controlado(monkeypatch):
    fake = Mock()
    fake.responses.create.side_effect = RuntimeError('chave-sensivel-abc123')
    with pytest.raises(IAIndisponivel) as exc:
        gerar_orientacao(ler('normal'), [], client=fake)
    assert 'chave-sensivel' not in str(exc.value)


def test_CT20_saida_inadequada_do_provedor_falha_segura():
    fake = Mock()
    fake.responses.create.return_value = SimpleNamespace(
        output_text='Administre 2 ml do remédio agora.'
    )
    with pytest.raises(IAIndisponivel, match='validação'):
        gerar_orientacao(ler('alerta'), analisar_dados(ler('alerta')), client=fake)


def test_CT21_limites_deterministicos():
    dados = ler('normal')
    dados['sensores'].update(nivel_agua=20, nivel_racao=10, temperatura=30, umidade=30)
    assert analisar_dados(dados) == []
    dados['sensores']['umidade'] = 70
    assert analisar_dados(dados) == []
    dados['sensores']['umidade'] = 70.1
    assert len(analisar_dados(dados)) == 1
