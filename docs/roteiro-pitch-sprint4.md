# Roteiro de vídeo Sprint 4 — 5 minutos (IoT & IA)

1. **00:00–00:45 — Problema.** CLYVO Elo mantém continuidade do cuidado pet entre consultas. Sensores e histórico geram dados pouco acessíveis ao tutor.
2. **00:45–01:30 — Evolução da Sprint 3.** Mostrar regras para água/ração/temperatura/umidade e acompanhamento pós-operatório. O professor pediu integração generativa; demonstrar onde ela foi adicionada.
3. **01:30–02:15 — Arquitetura.** FastAPI recebe dados, motor de regras define prioridades, Responses API produz mensagem contextual, aplicação a exibe. Dados da demonstração são sintéticos.
4. **02:15–03:45 — Demonstração real.** Executar cenário normal, alertas, pós-operatório; abrir resposta real do modelo e destacar aviso. Mostrar `/docs`, identificação do modelo e resultado completo. Não chamar saída simulada de LLM.
5. **03:45–04:30 — Testes e evidências.** Rodar `python -m pytest -q` (10 testes) e demonstrar casos determinísticos; diferenciar mock de integração real.
6. **04:30–05:00 — Benefícios, limites e próximos passos.** Mensagens mais compreensíveis ao tutor, consistência nas prioridades, sem diagnóstico. Mencionar status real da integração com o painel Java sem exageros.

## Antes de gravar

- Confirmar que `OPENAI_API_KEY` e créditos estão funcionando, sem exibir a chave.
- Deixar navegador e terminal configurados; mostrar app funcionando com código entregue.
- Não usar prontuários reais nem afirmar integração ao Java se ainda não estiver implementada.
- Publicar no YouTube como **Não listado** e colar o link no README/ZIP.
