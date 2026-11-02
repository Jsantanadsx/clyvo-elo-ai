# CLYVO Elo AI — Sprint 4 | IoT, IoB & IA Generativa

Evolução da Sprint 3 da FIAP para o Challenge CLYVO VET. Preserva o **motor de regras** e os **três cenários JSON sintéticos** e integra uma chamada **real** a um LLM pela **OpenAI Responses API**. Inclui API FastAPI, interface web de demonstração, dez testes automatizados e documentos técnicos.

## Equipe

| Integrante | RM |
|---|---|
| João Victor Santana dos Santos | 566063 |
| Gabriel Cabral Mendes Mariano | 563230 |

## 1. Funcionalidades

- Carrega cenários de Lara (normal), Zakaria (alertas ambientais) e Bolt (pós-operatório).
- Identifica alertas por regras **determinísticas**: água abaixo de 20, ração abaixo de 10, temperatura acima de 30°C, umidade fora de 30–70%; pós-operatório gera alerta alto. Esses limites são de **demonstração** e não são protocolos veterinários validados.
- Chama um modelo OpenAI com contexto estruturado e alertas priorizados, gerando orientação em português para o tutor.
- Acrescenta aviso de que o texto não substitui o médico-veterinário.
- Apresenta os resultados pela interface `/` e pela API documentada em `/docs`.
- O LLM **não decide prioridade**: as prioridades vêm de `app/rules.py`.

## 2. Pré-requisitos e configuração

- Python 3.11+; conexão com internet para chamada real à OpenAI.
- Chave OpenAI API com créditos/faturamento habilitados. A assinatura do ChatGPT **não** inclui automaticamente créditos da API.

### Windows PowerShell (VS Code)

```powershell
git clone https://github.com/Jsantanadsx/clyvo-elo-ai.git
cd clyvo-elo-ai
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
# Defina a chave na sessão, sem gravar no Git:
$env:OPENAI_API_KEY = "SUA_CHAVE_PRIVADA"
$env:OPENAI_MODEL = "gpt-4o-mini"
.\.venv\Scripts\python.exe -m uvicorn app.api:app --host 127.0.0.1 --port 8000
```

Abra `http://127.0.0.1:8000` e selecione um cenário. Use **Executar motor de regras** e depois **Gerar orientação com IA**. A API interativa estará em `http://127.0.0.1:8000/docs`.

**Atenção:** comandos `git clone` acima só terão o código novo depois de ele ser publicado no GitHub. Se usar o pacote ZIP recebido antes do push, entre na pasta extraída e execute os passos a partir de `python -m venv .venv`.

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export OPENAI_API_KEY='SUA_CHAVE_PRIVADA'
python -m uvicorn app.api:app --host 127.0.0.1 --port 8000
```

Não coloque a chave em frontend, capturas de tela, commits, README ou gravações. `.env` está no `.gitignore`; a aplicação **não carrega `.env` automaticamente**, configure as variáveis de ambiente na sessão/serviço.

## 3. Execução via terminal

```bash
python app/main.py --cenario 1 --somente-regras
python app/main.py --cenario 2
python app/main.py --cenario 3
```

O modo `--somente-regras` não chama IA generativa. Com a chave ausente, qualquer solicitação generativa falha de forma explícita com erro, em vez de simular um LLM.

## 4. Exemplos de API

```bash
# Health e cenários
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/cenarios/alerta

# Windows PowerShell:
$payload = Get-Content data/cenario_alerta.json -Raw
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/alertas -ContentType 'application/json' -Body $payload
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/analisar -ContentType 'application/json' -Body $payload
```

### Endpoints

| Método | Endpoint | Resultado |
|---|---|---|
| GET | `/` | Interface de demonstração |
| GET | `/health` | Estado da API e da configuração |
| GET | `/docs` | Documentação interativa FastAPI |
| GET | `/api/cenarios` | Lista de cenários |
| GET | `/api/cenarios/{codigo}` | JSON controlado do cenário |
| POST | `/api/alertas` | Alertas por regras, sem LLM |
| POST | `/api/analisar` | Alertas + orientação real do LLM |

Quando `CLYVO_API_TOKEN` estiver definida, o cabeçalho `X-CLYVO-TOKEN` é obrigatório nos dois POSTs. **Não publique esse protótipo aberto na internet** sem autenticação adequada, limites de requisições, HTTPS e controles de custos; a interface é um ambiente de demonstração local.

## 5. Testes automatizados

```bash
python -m pytest -q
```

Dez testes em `tests/test_sprint4.py`: cenário normal, quatro alertas, pós-operatório, validação de dados, indisponibilidade sem chave, contrato do LLM (mock), token e cenário inexistente.

**Limitação importante:** os testes locais não fazem chamadas pagas ao provedor. O mock valida somente o contrato. Para comprovar IA real ao professor, configure a chave, faça a solicitação `/api/analisar` e grave o resultado. Documente também a data, modelo e cenário executado.

## 6. Arquitetura

```text
JSON de demonstração / aplicação CLYVO
               |
               v
        FastAPI /api/alertas ------------------> Motor de regras -> prioridades
               |
        /api/analisar
               |                  (alertas + dados controlados)
               +----------------------------------------+
                                                        v
                                            OpenAI Responses API
                                                        |
                                                        v
                                              Orientação ao tutor
```

Para uso real, dados e eventos vêm do backend/banco, não dos JSONs de demonstração. O painel Java do grupo já possui uma área do tutor; a integração proposta está documentada em [`docs/integracao-java.md`](docs/integracao-java.md) e **ainda precisa ser conectada e verificada no painel Java**.

## 7. Segurança, privacidade e limites

- Cenários de demonstração têm dados sintéticos; **não envie prontuários identificáveis ou dados pessoais reais ao LLM** sem avaliação de privacidade, base legal e medidas adequadas.
- O prompt recebe as leituras e alertas classificados, evita prescrição/diagnóstico e trata o texto como assistência informativa.
- Não substituir atendimento veterinário nem alterar prioridades via LLM.
- Falha de API retorna erro claro HTTP 503. Alertas determinísticos continuam disponíveis.
- Os limites usados pelo motor são didáticos, não validados clinicamente.

## 8. Evidências e entrega Sprint 4

- Código e documentação técnica: este repositório.
- Plano de QA: [`docs/plano-testes-qa.md`](docs/plano-testes-qa.md).
- **Evidência real da chamada OpenAI:** executada com os três cenários em 02/11/2026; [capturas e matriz de resultados](docs/evidencias-validacao-2026-11-02.md).
- **Integração ponta a ponta com painel Java:** pendente de implementação/verificação.
- **Vídeo pitch (~5 minutos):** [INSERIR LINK DEPOIS DE GRAVAR].
- ZIP da disciplina: incluir links do YouTube não listado e deste repositório.

## 9. Evidências da Sprint 4

- Zakaria: quatro alertas, prioridade conferida e orientação real.
- Lara: zero alertas, com orientação preventiva.
- Bolt: três alertas, com orientação contextualizada para o pós-operatório.
- Execução automatizada relatada no ambiente Windows: **10 passed, 1 warning**.
- Ver arquivos em [`evidencias/`](evidencias/) e a [matriz documentada](docs/evidencias-validacao-2026-11-02.md).
- **Ainda pendentes:** teste ponta a ponta com painel Java e vídeo final.

## 10. Pitch Sprint 3

[Vídeo original da Sprint 3](https://www.youtube.com/watch?v=n-DC-6svdz8) — histórico, não substitui o vídeo da Sprint 4.

## 11. Collection para a Sprint 4 de QA

A collection `qa-postman-collection.json` contém **4 testes automatizados HTTP com asserções JavaScript** sem custo de LLM. Importe no **Insomnia ou Postman**, inicie o servidor local e execute a pasta `QA - 4 testes automatizados (sem custo de LLM)`.

A pasta `Integração REAL com IA` faz chamada paga ao modelo e só deve ser executada após configurar e testar a chave. Gravar o vídeo mostrando importação/configuração, execução dos quatro testes e resultados, conforme o enunciado de QA.

Exemplos de correção dos PBIs e critérios de aceite estão em [`docs/correcao-pbis-sprint3.md`](docs/correcao-pbis-sprint3.md). Eles ainda precisam ser conferidos e aplicados no Azure Boards existente.

## 12. Planejamento de sistema e conferência final

- [Casos manuais para Azure Boards](docs/qa-testes-manuais-sistema.md) — propostas ainda não cadastradas.
- [Checklist da Sprint 4](docs/checklist-entrega.md).
- [Arquitetura demonstrada e integração pendente](docs/arquitetura-sprint4.md).
