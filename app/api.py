"""API da Sprint 4: regras determinísticas e geração de orientações com LLM.

Chamadas de análise são autenticadas por padrão; o modo de demonstração sem token
só é permitido explicitamente em loopback (não recomendado para deploy).
"""
import json
import os
import secrets
import unicodedata
from enum import Enum
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.ai_service import IAIndisponivel, gerar_orientacao
from app.rules import analisar_dados

ROOT = Path(__file__).resolve().parent.parent
CENARIOS = {
    'normal': 'cenario_normal.json',
    'alerta': 'cenario_alerta.json',
    'pos_operatorio': 'cenario_pos_operatorio.json',
}

app = FastAPI(
    title='CLYVO Elo AI — Sprint 4', version='4.1.0',
    description='Análise determinística e orientação personalizada com LLM.',
)


class Pet(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id_pet: int = Field(ge=1)
    nome: str = Field(min_length=1, max_length=60)
    especie: str = Field(min_length=1, max_length=30)
    raca: str = Field(min_length=1, max_length=60)
    peso_kg: float = Field(gt=0, le=150)


class Sensores(BaseModel):
    model_config = ConfigDict(extra='forbid')
    nivel_agua: float = Field(ge=0, le=100)
    nivel_racao: float = Field(ge=0, le=100)
    temperatura: float = Field(ge=-20, le=80)
    umidade: float = Field(ge=0, le=100)


class TipoEvento(str, Enum):
    CHECKUP = 'CHECKUP'
    POS_OPERATORIO = 'POS_OPERATORIO'
    CONSULTA = 'CONSULTA'
    RETORNO = 'RETORNO'
    VACINACAO = 'VACINACAO'
    VACINA = 'VACINA'
    MEDICACAO = 'MEDICACAO'
    EXAME = 'EXAME'
    OUTRO = 'OUTRO'


class EventoClinico(BaseModel):
    model_config = ConfigDict(extra='forbid')
    tipo: TipoEvento
    descricao: str = Field(min_length=1, max_length=250)
    status: str = Field(min_length=1, max_length=40)

    @field_validator('tipo', mode='before')
    @classmethod
    def normalizar_tipo(cls, valor):
        if not isinstance(valor, str):
            return valor
        sem_acentos = ''.join(c for c in unicodedata.normalize('NFKD', valor)
                             if not unicodedata.combining(c))
        return sem_acentos.strip().upper().replace('-', '_').replace(' ', '_')


class DadosAnalise(BaseModel):
    model_config = ConfigDict(extra='forbid')
    pet: Pet
    sensores: Sensores
    evento_clinico: Optional[EventoClinico] = None


def verificar_token(request: Request, x_clyvo_token: Optional[str] = Header(default=None)):
    """Autenticação fail-closed. Demo sem token apenas com opt-in e em loopback."""
    esperado = os.getenv('CLYVO_API_TOKEN', '').strip()
    if esperado:
        if not x_clyvo_token or not secrets.compare_digest(x_clyvo_token, esperado):
            raise HTTPException(status_code=401, detail='Token de integração inválido ou ausente.')
        return

    modo_demo = os.getenv('CLYVO_LOCAL_DEMO', '').strip().lower() in {'1', 'true', 'yes'}
    origem = request.client.host if request.client else ''
    if modo_demo and origem in {'127.0.0.1', '::1', 'localhost', 'testclient'}:
        return
    raise HTTPException(status_code=503, detail='Autenticação do serviço não configurada.')


@app.get('/')
def interface():
    return FileResponse(ROOT / 'static' / 'index.html')


@app.get('/health')
def health():
    return {'status': 'UP', 'modelo_configurado': bool(os.getenv('OPENAI_API_KEY')),
            'provedor': 'OpenAI Responses API'}


@app.get('/api/cenarios')
def listar_cenarios():
    return [{'codigo': codigo, 'descricao': codigo.replace('_', ' ').capitalize()}
            for codigo in CENARIOS]


@app.get('/api/cenarios/{codigo}')
def obter_cenario(codigo: str):
    if codigo not in CENARIOS:
        raise HTTPException(status_code=404, detail='Cenário inexistente.')
    return json.loads((ROOT / 'data' / CENARIOS[codigo]).read_text(encoding='utf-8'))


@app.post('/api/alertas', dependencies=[Depends(verificar_token)])
def alertas(dados: DadosAnalise):
    d = dados.model_dump(mode='json')
    lista = analisar_dados(d)
    return {'pet': dados.pet.nome, 'alertas': lista, 'quantidade_alertas': len(lista),
            'origem': 'MOTOR_REGRAS', 'ia_generativa_utilizada': False}


@app.post('/api/analisar', dependencies=[Depends(verificar_token)])
def analisar(dados: DadosAnalise):
    d = dados.model_dump(mode='json')
    lista = analisar_dados(d)
    try:
        orientacao = gerar_orientacao(d, lista)
    except IAIndisponivel as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {'pet': dados.pet.nome, 'alertas': lista, 'quantidade_alertas': len(lista),
            'orientacao': orientacao, 'origem': 'OPENAI_RESPONSES_API',
            'modelo': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            'ia_generativa_utilizada': True}
