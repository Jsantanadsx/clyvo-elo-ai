# CLYVO Elo AI — Sprint 4 | IoT, IoB e Inteligência Artificial Generativa

Projeto do Challenge FIAP 2026 — CLYVO VET. Evolução da Sprint 3 com **motor de regras determinístico**, **geração real de orientações usando OpenAI Responses API** e **integração implementada com o painel Java** do grupo. Os valores de sensores demonstrados são **sintéticos**; não há sensores físicos transmitindo dados em tempo real.

## Integrantes

| Integrante | RM |
|---|---|
| João Victor Santana dos Santos | 566063 |
| Gabriel Cabral Mendes Mariano | 563230 |

## Demonstração e entrega — Sprint 4

| Recurso | Link |
|---|---|
| **Vídeo do pitch da Sprint 4** | [Assistir no YouTube](https://youtu.be/6hMTqWkoWbM) |
| **Interface Python publicada** | [CLYVO Elo AI](https://clyvo-elo-ai-python.onrender.com) |
| API Python — estado | [GET /health](https://clyvo-elo-ai-python.onrender.com/health) |
| Documentação interativa FastAPI | [Swagger /docs](https://clyvo-elo-ai-python.onrender.com/docs) |
| **Painel Java integrado** | [CLYVO Elo — Java](https://clyvo-elo-java.onrender.com) |
| Código-fonte | [Repositório público](https://github.com/Jsantanadsx/clyvo-elo-ai) |
| Arquivo para o ZIP | [docs/links-entrega-iot.txt](docs/links-entrega-iot.txt) |

**Antes de enviar:** conferir no YouTube Studio que o vídeo está **Não listado** e que abre em janela anônima. Serviços gratuitos no Render podem demorar para iniciar após inatividade.

## 1. Objetivo e evolução

Manter a continuidade dos cuidados do pet entre consultas. O serviço recebe informações estruturadas do pet, condições de água/ração/ambiente e, quando disponível, o contexto clínico. As prioridades de alertas são determinadas por regras previamente programadas; um LLM real transforma essas informações em uma mensagem contextualizada ao tutor.

**O modelo generativo não calcula nem altera prioridades.** Os limites são definidos somente para demonstração didática; não constituem protocolos clínicos validados.

## 2. Três cenários sintéticos

| Cenário | Água | Ração | Temperatura | Umidade | Alertas esperados |
|---|---:|---:|---:|---:|---:|
| Lara — rotina normal | 75% | 65% | 24 °C | 50% | **0** |
| Zakaria — alertas ambientais | 12% | 8% | 32 °C | 78% | **4** |
| Bolt — pós-operatório | 18% | 6,5% | 29,5 °C | 55% | **3** |

O código das regras está em [`app/rules.py`](app/rules.py). O cenário de pós-operatório inclui evento clínico. As entradas ficam em [`data/`](data/) e as capturas em [`evidencias/`](evidencias/). Confira a [matriz de validação](docs/evidencias-validacao-2026-11-02.md).

## 3. Arquitetura publicada

```text
Tutor no painel Java / Interface Python de demonstração
                       |
                       v
            FastAPI Python no Render
                       |
              Motor de regras --------> Alertas e prioridades
                       |
                       v
                OpenAI Responses API
                       |
                       v
             Orientação personalizada
                       |
                       v
              JSON de resposta ao Java
```

**Integração Java → Python → OpenAI:** implementada e demonstrada. O backend Java obtém os dados autorizados do pet e o último evento clínico na base da clínica, coleta leituras sintéticas preenchidas manualmente pelo tutor e envia a solicitação ao serviço FastAPI pela URL HTTPS pública, com autenticação de serviço. Em testes da Pipoca, o Java exibiu origem `OPENAI_RESPONSES_API` com **0 alertas** em condições normais e **2 alertas de prioridade alta** em condições de alerta.

Arquivos principais: `app/api.py` (FastAPI), `app/rules.py` (regras), `app/ai_service.py` (OpenAI), `static/index.html` (demonstração) e `tests/test_sprint4.py` (testes). Detalhes em [arquitetura](docs/arquitetura-sprint4.md) e [integração Java](docs/integracao-java.md).

## 4. Endpoints da API

| Método | Endpoint | Objetivo | Autenticação |
|---|---|---|---|
| GET | `/` | Interface web | Pública |
| GET | `/health` | Estado e indicação de modelo configurado | Pública |
| GET | `/docs` | Documentação Swagger | Pública |
| GET | `/api/cenarios` | Listagem de cenários | Pública |
| GET | `/api/cenarios/{codigo}` | JSON do cenário sintético | Pública |
| POST | `/api/alertas` | Análise determinística, sem LLM | Token |
| POST | `/api/analisar` | Alertas e orientação real por LLM | Token |

Os POSTs exigem cabeçalho `X-CLYVO-TOKEN` igual ao segredo do servidor Python `CLYVO_API_TOKEN`. No painel Java o backend envia a credencial configurada em `CLYVO_AI_TOKEN`, sem exigir que o tutor a digite. **Nunca exponha a chave `OPENAI_API_KEY` ao navegador, vídeo ou repositório.** O modo `CLYVO_LOCAL_DEMO=true` é restrito a demonstrações locais em loopback; não deve ser habilitado no Render.

## 5. Como executar localmente (Windows PowerShell)

Pré-requisitos: Python 3.11+ e, para usar a geração real, uma chave OpenAI API própria com créditos habilitados. A assinatura do ChatGPT não inclui automaticamente créditos da API.

```powershell
git clone https://github.com/Jsantanadsx/clyvo-elo-ai.git
cd clyvo-elo-ai
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Para testar o motor de regras sem fazer chamada paga:

```powershell
.\.venv\Scripts\python.exe app/main.py --cenario 2 --somente-regras
```

Para habilitar geração real localmente, configure a chave **privadamente na sessão de PowerShell**:

```powershell
$env:OPENAI_API_KEY = "SUA_CHAVE_PRIVADA"
$env:OPENAI_MODEL = "gpt-4o-mini"
$env:CLYVO_LOCAL_DEMO = "true"  # somente em 127.0.0.1
.\.venv\Scripts\python.exe -m uvicorn app.api:app --host 127.0.0.1 --port 8000
```

Abra `http://127.0.0.1:8000` e execute os três cenários. Com IA real, observe `origem: OPENAI_RESPONSES_API`. O provedor pode cobrar pelo uso; não registre segredos em arquivos versionados.

## 6. Testes e evidências

A suíte tem **21 testes** registrados como aprovados na revisão da Sprint 4. Testa dados e limites, autenticação, erros, cenários, motor de regras e contrato com o LLM. O workflow [Python tests](.github/workflows/python-tests.yml) executa testes sem credencial da OpenAI e sem custo de inferência.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

**Diferença importante:** os testes automatizados usam mocks da integração com LLM. Eles não provam uma chamada real ao provedor; a chamada real é demonstrada pelas capturas dos cenários, pelo vídeo do pitch e pela integração no painel Java. Consulte [as evidências](docs/evidencias-validacao-2026-11-02.md).

## 7. Segurança e limitações

- Token de integração entre backends; chave OpenAI restrita ao Python.
- Dados de demonstração sintéticos, sem telemetria física nem persistência das leituras no serviço Python.
- Validação de entrada e barreira heurística básica contra respostas de prescrição/dose/diagnóstico, sem garantia de segurança clínica.
- As regras e mensagens **não** constituem diagnóstico veterinário, prescrição ou triagem validada.
- Não enviar dados pessoais reais ou prontuários identificáveis a um LLM sem análise jurídica, de privacidade e de segurança pertinente.

## 8. Documentação e submissão

- [Checklist da entrega](docs/checklist-entrega.md)
- [Mapa de requisitos da Sprint 4 — IoT](docs/mapa-atendimento-sprint4.md)
- [Matriz e capturas](docs/evidencias-validacao-2026-11-02.md)
- [Arquitetura](docs/arquitetura-sprint4.md)
- [Integração com o painel Java](docs/integracao-java.md)
- [Roteiro do vídeo](docs/roteiro-pitch-sprint4.md)
- [Links para ZIP e submissão](docs/links-entrega-iot.txt)

O [PR #1](https://github.com/Jsantanadsx/clyvo-elo-ai/pull/1) da evolução IoT foi incorporado à branch `main`. O arquivo de entrega deve conter os links do YouTube e GitHub; confirmar os requisitos no portal da FIAP antes do envio.

**Histórico:** [pitch original da Sprint 3](https://www.youtube.com/watch?v=n-DC-6svdz8) — não substitui o vídeo desta Sprint 4.
