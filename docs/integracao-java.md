# Integração implementada — Java Spring Boot + Python FastAPI + OpenAI

**Serviços:**

- [Painel Java](https://clyvo-elo-java.onrender.com) — [repositório Java](https://github.com/GabrielCabralmm/clyvo-elo-java)
- [API Python FastAPI](https://clyvo-elo-ai-python.onrender.com) — [estado `/health`](https://clyvo-elo-ai-python.onrender.com/health)

## Fluxo integrado

1. Um tutor autenticado abre um pet autorizado e clica em **Gerar orientação com IA (demo)**.
2. O Java obtém do banco os dados cadastrais do pet e o último evento clínico. Água, ração, temperatura e umidade são **leituras sintéticas, informadas manualmente**, não medidas por sensores em operação.
3. O serviço Java `ClyvoAiClient` envia um POST HTTPS a `/api/analisar` no backend Python, acrescentando `X-CLYVO-TOKEN` no servidor.
4. O Python valida o contrato, aplica regras determinísticas para definir os alertas e consulta a OpenAI Responses API para produzir a orientação.
5. O JSON devolvido contém `alertas`, `quantidade_alertas`, `origem` e `orientacao`; o Java exibe o resultado na tela do tutor.

O painel Java também oferece `/ecossistema/ia` para executar os cenários sintéticos Lara, Zakaria e Bolt com os perfis de clínica autorizados.

## Contrato HTTP

| Método | Endpoint | Retorno |
|---|---|---|
| GET | `/health` | Estado do serviço e indicação de modelo configurado, sem revelar chave |
| GET | `/api/cenarios/{codigo}` | JSON sintético do cenário |
| POST | `/api/alertas` | Alertas e prioridades gerados por regras, sem LLM |
| POST | `/api/analisar` | Alertas e orientação do LLM real |

POSTs exigem `Content-Type: application/json` e `X-CLYVO-TOKEN`. Código HTTP `401` indica token incorreto/ausente; `422`, dados inválidos; `503`, serviço ou modelo indisponível.

## Configuração segura

O Java utiliza `CLYVO_AI_URL=https://clyvo-elo-ai-python.onrender.com` e `CLYVO_AI_TOKEN`. O Python utiliza `CLYVO_API_TOKEN` (mesmo segredo), `OPENAI_API_KEY` e `OPENAI_MODEL`. **Não publicar os valores dos segredos.** As instâncias Render se comunicam pela URL HTTPS pública; não é necessário estarem na mesma conta.

## Evidências observadas na aplicação publicada

| Condições de demonstração para a Pipoca | Resultado |
|---|---|
| Água 75%, ração 65%, temperatura 24 °C, umidade 50% | **0 alertas**, orientação preventiva, `OPENAI_RESPONSES_API` |
| Água 5%, ração 15%, temperatura 34 °C, umidade 50% | **2 alertas ALTA**, orientação contextualizada, `OPENAI_RESPONSES_API` |

Esses resultados foram apresentados durante a validação do sistema. Para prova visual adicional no repositório, anexar as capturas correspondentes, caso o professor solicite.

**Limitações:** sem sensores físicos integrados e sem diagnóstico clínico; mensagens orientativas devem ser avaliadas por profissionais antes de qualquer uso real.
