# Roteiro do vídeo QA — Sprint 4

**Ferramenta:** Insomnia (importação de `qa-postman-collection.json` como Postman Collection) ou Postman. A demonstração deve provar **4 casos automatizados do sistema** e exibir configuração, execução, testes/assertivas e resultados.

1. **00:00–00:30 — Contexto**: apresentação do CLYVO Elo, repositório, diferença entre motor de regras e LLM.
2. **00:30–01:00 — Preparação**: mostrar servidor Python rodando em `127.0.0.1:8000` com `CLYVO_LOCAL_DEMO=true` e **sem mostrar chave**. Abrir ferramenta e importar collection.
3. **01:00–01:40 — Configuração**: confirmar `baseUrl=http://127.0.0.1:8000` e os scripts de assertiva JavaScript em cada caso.
4. **01:40–03:20 — Execução**: rodar CT01 (0 alertas), CT02 (4 alertas), CT03 (3 alertas com pós-operatório), CT04 (HTTP 422); mostrar cada resultado e status. O quarto caso deve passar porque valida a rejeição esperada do dado inválido.
5. **03:20–04:00 — Resultado**: mostrar 4 casos aprovados e os detalhes dos testes. Se Insomnia não suportar os scripts `pm.test` da coleção nessa versão, usar Postman para executar os scripts e mostrar o resultado, não alegar execução automática apenas por HTTP 200.
6. **04:00–04:30 — Vínculo com QA manual**: indicar os casos MANxx e o projeto Azure Boards, com a correspondência a PBIs reais.

Depois: subir vídeo (visibilidade conforme exigido pelo professor), inserir URL em `docs/links-entrega-qa.md` e publicar em `develop`. Verificar em navegador anônimo ou acesso autorizado, sem revelar senhas.
