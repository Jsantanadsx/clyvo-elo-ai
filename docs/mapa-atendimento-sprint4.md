# Rastreabilidade dos requisitos — IoT, IoB e IA Generativa | Sprint 4

**Fonte mencionada no mapa de planejamento original:** `2TDS Fevereiro - Challenge 2026 - 2º Semestre (1).pdf`, páginas 56–58. Este documento resume os requisitos como transcritos no projeto; para conferência definitiva, consultar o PDF original no ambiente da FIAP.

| Exigência | Evidência disponível | Situação |
|---|---|---|
| Evoluir a IA proposta na Sprint 3 com geração real | `app/rules.py`, `app/ai_service.py`, vídeo e capturas | Implementado e demonstrado |
| Preparar e validar os dados | `data/*.json`, `tests/test_sprint4.py` (21 testes registrados) | Implementado com dados sintéticos |
| Expor API e interface de IA | `app/api.py`, `static/index.html`, Render e `/docs` | Publicado |
| Integrar com a aplicação do grupo | Classe `ClyvoAiClient` no Java e tela de orientação da Pipoca | Validado ponta a ponta |
| Avaliar resultados em situações de uso | Lara, Zakaria e Bolt — [matriz e capturas](evidencias-validacao-2026-11-02.md) | Três cenários demonstrados |
| Produzir pitch de aproximadamente cinco minutos | https://youtu.be/6hMTqWkoWbM | Gravado; conferir duração/acesso |
| Disponibilizar vídeo no YouTube como Não listado | YouTube Studio | Conferência da configuração pendente |
| Fornecer ZIP com GitHub e vídeo | [docs/links-entrega-iot.txt](links-entrega-iot.txt) | Links prontos; ZIP e submissão pendentes |

**Ressalvas:** sensores e leituras do protótipo Python são sintéticos; não há hardware conectado. No fluxo Java, os dados autorizados do pet e do evento clínico vêm do banco da clínica, mas as leituras de água, ração, temperatura e umidade são fornecidas manualmente. A orientação gerada não substitui avaliação veterinária.
