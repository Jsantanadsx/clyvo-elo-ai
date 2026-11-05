# Resultado dos testes automatizados — QA Sprint 4

Ferramenta: Newman / Postman Collection
Ambiente: FastAPI local, http://127.0.0.1:8000
Dados: sinteticos
Data: 04/11/2026

| Caso | Resultado | Status |
|---|---|---|
| CT01 - Lara | HTTP 200; zero alertas | Aprovado |
| CT02 - Zakaria | HTTP 200; quatro alertas | Aprovado |
| CT03 - Bolt | HTTP 200; alerta clinico presente | Aprovado |
| CT04 - Entrada invalida | HTTP 422; validacao correta | Aprovado |

Total: 4 requisicoes, 8 assertivas, zero falhas.

Evidencias:
- [Relatorio JSON](../evidencias/qa/newman-resultado.json)
- [Console Newman](../evidencias/qa/newman-console.txt)

Video: https://youtu.be/sNcjHBIQDv4

Azure Boards: https://dev.azure.com/clyvo-elo-fiap/CLYVO%20Elo

Os 14 casos manuais estao cadastrados nos work items #39 a #52, mas nao devem ser considerados executados ou aprovados.
