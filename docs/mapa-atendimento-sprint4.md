# Cobertura de requisitos da Sprint 4 — Challenge FIAP 2026

Fonte: PDF oficial `2TDS Fevereiro - Challenge 2026 - 2º Semestre (1).pdf`, pp. 46–47 (QA) e 56–58 (IoT/IA). O status abaixo é conservador: **proposta/documentação não equivale à execução real**.

## IoT, IoB e IA generativa

| Exigência | Evidência disponível | Estado |
|---|---|---|
| Funcionalidade da IA definida na Sprint 3, com geração real | `app/ai_service.py`, `app/rules.py`, screenshots anteriores | Implementado; reteste ao vivo necessário após CR |
| Dados preparados e validados | `data/` e `tests/test_sprint4.py` (21 testes) | Implementado com dados sintéticos |
| Comunicação com API de IA e interface | FastAPI `app/api.py`, `static/index.html` | Implementado localmente |
| Integração com aplicação do grupo, interface, banco, APIs | Patch Java opcional e contrato `docs/integracao-java.md` | **Pendente aplicar e testar ponta a ponta no Java com dados do banco** |
| Teste em situações de uso e avaliação dos resultados | 3 cenários, evidências capturadas antes do CR, suíte pytest | Parcial: repetir testes reais após CR e testar Java |
| Pitch ~5 min com IA, benefícios tutor/clínica, integração | `docs/roteiro-pitch-sprint4.md` | **Pendente gravar/publicar** |
| Vídeo YouTube *não listado* | Campo no README para link | **Pendente** |
| ZIP obrigatório com link YouTube + GitHub | `docs/links-entrega-iot.txt` (preencher) | **Pendente link do vídeo** |

## QA

| Exigência | Evidência disponível | Estado |
|---|---|---|
| Plano manual no Azure Boards, cobrindo funcionalidades principais | `docs/qa-execucao-azure-boards.md` (14 casos) | **Pendente cadastrar no Boards** |
| Objetivos, entradas, saídas e passos | Cada MAN01–MAN14 possui os campos | Documento completo; **Boards pendente** |
| Dados controlados e alinhamento ao release/backlog | Valores definidos e checklist de ligação ao PBI | **Pendente conciliar com PBIs reais e release plan** |
| Link Azure + professor Basic/Admin | `docs/links-entrega-qa.md` (preencher/verificar) | **Pendente confirmar acesso** |
| Ao menos 4 casos automatizados | `qa-postman-collection.json` + 21 testes pytest | Implementados; **executar collection na ferramenta** |
| Vídeo de preparo/configuração/execução/resultados | `docs/roteiro-video-qa.md` | **Pendente gravar/publicar** |
| GitHub público, branch `develop`, links Boards + vídeo | `docs/links-entrega-qa.md` preparado | **Pendente publicar em `develop`** |

**Nota:** ter 21 testes Python não substitui testes de sistema Java e critérios de aceite nos PBIs do Azure Boards. O vídeo não é gerado por este repositório; é necessário gravar execução real e cadastrar links.
