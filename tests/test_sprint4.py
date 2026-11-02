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
from app.ai_service import gerar_orientacao, IAIndisponivel, AVISO
from app.rules import analisar_dados

ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def ler(nome):
    return json.loads((ROOT / 'data' / ('cenario_' + nome + '.json')).read_text(encoding='utf-8'))


@pytest.fixture(autouse=True)
def sem_token_configurado(monkeypatch):
    monkeypatch.delenv('CLYVO_API_TOKEN', raising=False)


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
