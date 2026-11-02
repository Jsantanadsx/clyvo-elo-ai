# Plano inicial de testes QA — CLYVO Elo AI, Sprint 4

> A parte abaixo documenta o COMPONENTE de IA. É necessário complementar o Azure Boards com testes de todas as funções principais do CLYVO Elo, de acordo com os PBIs e release plan efetivos. Identificadores CT01–CT10 aqui são locais e devem ser associados aos work items corretos.

## Casos de teste automatizados e determinísticos

| ID | Objetivo | Dados de entrada controlados | Saída esperada | Procedimento |
|---|---|---|---|---|
| CT01 | Verificar cenário sem alerta | `cenario_normal.json` (água=75, ração=65, temperatura=24, umidade=50) | HTTP 200; 0 alertas | POST `/api/alertas`; conferir quantidade 0 |
| CT02 | Verificar quatro alertas e prioridade | `cenario_alerta.json` (12, 8, 32, 78) | HTTP 200; água ALTA, ração MÉDIA, temperatura ALTA, umidade MÉDIA | POST `/api/alertas`; conferir tipos/ordem/prioridades |
| CT03 | Verificar contexto pós-operatório | `cenario_pos_operatorio.json` (18, 6.5, 29.5, 55; `POS_OPERATORIO`) | HTTP 200; 3 alertas, incluindo `ACOMPANHAMENTO_CLINICO` ALTA | POST `/api/alertas`; verificar 3 alertas |
| CT04 | Rejeitar leitura inválida | Como CT02, alterando umidade=150 | HTTP 422; validação de campo | POST `/api/alertas`; verificar erro |
| CT05 | Diferenciar IA real de simulação | `cenario_normal.json`, sem `OPENAI_API_KEY` | HTTP 503; erro explícito sem mensagem supostamente gerada | POST `/api/analisar` sem chave; verificar erro |
| CT06 | Validar contrato do modelo usando mock | Cenário alerta + cliente injetado mockado | Contexto JSON contém alertas; resposta e aviso exibidos | Executar pytest; conferir `responses.create` e argumentos |
| CT07 | Proteger API em modo token | Cenário normal; `CLYVO_API_TOKEN=token-exemplo-teste` | HTTP 401 sem token e 200 com token | POST `/api/alertas` sem/com cabeçalho |
| CT08 | Verificar cenário inexistente | Código de cenário `inexistente` | HTTP 404 | GET `/api/cenarios/inexistente`; verificar 404 |


| CT09 | Confirmar contrato entre endpoint HTTP e serviço de IA (stub) | Cenário alerta + função generativa substituída em teste | HTTP 200; campo `orientacao` presente; quatro alertas | Executar pytest com monkeypatch; verificar retorno HTTP |
| CT10 | Confirmar interface de demonstração | GET `/` | HTTP 200; controles de análise presentes | Testar endpoint `/` e procurar título e botão |

## Manual — evidência para Azure Boards

Para cada caso manual, registrar: **Objetivo**, **PBI/Feature relacionado**, **pré-condições**, **dados de entrada explícitos**, **saída esperada**, **procedimento numerado**, **resultado efetivo** e **evidência (print/URL)**.

1. Abrir `http://127.0.0.1:8000` e selecionar o cenário controlado.
2. Clicar em **Executar motor de regras**. Verificar o resultado previsto na matriz.
3. Com `OPENAI_API_KEY` configurada, clicar em **Gerar orientação com IA**.
4. Evidenciar a orientação gerada, o aviso veterinário e a indicação `OPENAI_RESPONSES_API`.
5. Registrar o nome do modelo, data da execução e a saída obtida. Não usar dados reais do tutor/pet no teste.
6. Gravar o vídeo mostrando código/configuração, execução, resultado e correspondência com os PBIs.

**Nota:** Não é correto aprovar CT de integração real com IA externa somente com testes mockados. Faça pelo menos uma chamada REAL ao provedor antes da entrega e registre a evidência; resultados de texto livre podem variar e devem ser avaliados por propriedades, não por correspondência palavra a palavra.
