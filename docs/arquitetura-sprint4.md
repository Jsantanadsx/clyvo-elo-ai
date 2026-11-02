# Arquitetura — CLYVO Elo AI Sprint 4

```mermaid
flowchart LR
    T["Tutor / clínica"] --> P["Painel CLYVO Elo (Spring Boot)"]
    P -. "Integração HTTP a validar" .-> A["API IA FastAPI"]
    D["Cenários JSON sintéticos"] --> A
    A --> R["Motor de regras"]
    R --> Q["Alertas priorizados"]
    A --> L["OpenAI Responses API"]
    Q --> L
    L --> O["Orientação personalizada"]
    O --> A
    A -. "Resposta HTTP" .-> P
    A --> W["Interface web local (demonstração concluída)"]
```

**Legendas:** linhas contínuas = fluxos implementados e demonstrados no serviço Python; linhas pontilhadas = integração Java ainda pendente de execução/validação. Sensores físicos e persistência em banco **não** foram implementados no protótipo Python; os JSONs representam leituras sintéticas.
