# Evidencias de integracao - painel Java + API Python no Render

Estas duas imagens foram capturadas durante a validacao em 03-04/11/2026.
A aplicacao Java consultou a FastAPI Python por HTTPS e apresentou respostas com origem OPENAI_RESPONSES_API.

- `../evidencias/pipoca-java-condicoes-normais.png`: Pipoca; agua 75%, racao 65%, temperatura 24 C, umidade 50%; zero alertas e orientacao preventiva.
- `../evidencias/pipoca-java-dois-alertas.png`: Pipoca; agua 5%, racao 15%, temperatura 34 C, umidade 50%; dois alertas de prioridade ALTA e orientacao contextualizada.

Todas as leituras foram preenchidas manualmente para demonstracao; nao sao obtidas de sensores fisicos.
Dados autorizados do cadastro e do evento clinico foram consultados pelo backend Java da clinica.
Nao ha diagnostico ou prescricao automatica.

- Python: https://clyvo-elo-ai-python.onrender.com
- Java: https://clyvo-elo-java.onrender.com
- Pitch: https://youtu.be/6hMTqWkoWbM