# Evidências da integração generativa — Sprint 4

**Data:** 02/11/2026  
**Ambiente observado:** Windows, Python 3.12.3, FastAPI/Uvicorn local em `127.0.0.1:8000`.  
**Integração:** OpenAI Responses API (`OPENAI_RESPONSES_API` exibido na interface).  
**Dados:** JSONs sintéticos oriundos da Sprint 3; nenhum prontuário real foi utilizado.

## Cenários executados no navegador

| Cenário | Entrada usada | Alertas esperados | Alertas observados | Orientação generativa | Evidência |
|---|---|---|---|---|---|
| Zakaria — alertas ambientais | Água 12, ração 8, temperatura 32°C, umidade 78% | 4: água ALTA, ração MÉDIA, temperatura ALTA, umidade MÉDIA | **4**, com prioridades previstas | Gerada e indicada como `OPENAI_RESPONSES_API` | [Captura](../evidencias/zakaria-ia-real.png) |
| Lara — rotina normal | Água 75, ração 65, temperatura 24°C, umidade 50% | 0 | **0** | Orientação preventiva coerente, `OPENAI_RESPONSES_API` | [Captura](../evidencias/lara-ia-real.png) |
| Bolt — pós-operatório | Água 18, ração 6,5, temperatura 29,5°C, umidade 55%; evento `POS_OPERATORIO` | 3: água ALTA, ração MÉDIA, acompanhamento clínico ALTA | **3**, com prioridades previstas | Orientação relacionada ao pós-operatório, `OPENAI_RESPONSES_API` | [Captura](../evidencias/bolt-ia-real.png) |

### Capturas

**Zakaria**

![Zakaria: quatro alertas e orientação gerada](../evidencias/zakaria-ia-real.png)

**Lara**

![Lara: nenhum alerta e orientação preventiva](../evidencias/lara-ia-real.png)

**Bolt**

![Bolt: três alertas e orientação de acompanhamento](../evidencias/bolt-ia-real.png)

## Evidências de execução técnica

- A pessoa responsável executou `python -m pytest -q` com **10 passed, 1 warning** no ambiente Windows; o warning foi de depreciação `httpx`/Starlette, sem falha nos testes.
- Registro do servidor: `POST /api/analisar HTTP/1.1 200 OK`, durante o cenário Zakaria.
- O retorno exibido pela aplicação identificou `OPENAI_RESPONSES_API` nos três cenários, com texto variável gerado pelo modelo.
- **Importante:** os 10 testes automatizados usam mock/stub na camada de LLM; a prova da chamada real é a execução demonstrada nas capturas, não o `pytest`.
- As prioridades são **regras de demonstração** do projeto e não diagnósticos ou classificação clínica validada.

## Limitações para entrega final

- A API Python foi validada localmente. **A integração com o painel Java do grupo ainda não foi executada ponta a ponta.**
- As capturas não comprovam implantação pública, persistência em banco ou dispositivos IoT físicos; as leituras são sintéticas.
- O vídeo final de aproximadamente cinco minutos ainda precisa ser gravado, publicado como não listado e vinculado no README.
- Para validação de sistema completa de QA, associar os cenários aos PBIs e release plan efetivamente cadastrados no Azure Boards.
