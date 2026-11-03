# Plano de testes manuais para cadastro no Azure Boards — Sprint 4

**Origem dos critérios:** Challenge 2026, Sprint 4, QA pp. 46–47. Cada teste deve conter objetivo, entrada controlada, saída esperada, procedimento enumerado. A execução real, o ID do PBI e o resultado observado devem ser preenchidos **no Azure Boards**. Não trate esta proposta como Board já cadastrado.

**Pré-condições:** Java e banco funcionando em ambiente de testes; perfis ADMIN, DOUTOR e TUTOR criados com identidades sintéticas; dois tutores e pets distintos; dados de IoT artificiais; FastAPI com acesso local ou token no ambiente de testes. Registrar em cada caso: `PBI/Feature`, `Sprint`, `Executor`, `Data/hora`, `Resultado obtido`, `Status` e `Evidência`.

## Roteiros controlados

### MAN01 — Autenticar como tutor
- **Objetivo:** validar login e redirecionamento para o painel do tutor.
- **Entrada:** conta sintética TUTOR-A e senha exclusiva do ambiente de QA (não registrar a senha no Board).
- **Saída esperada:** sessão autenticada e painel com pets do próprio tutor; nenhum recurso administrativo exibido.
- **Passos:** 1) Abrir `/login`. 2) Informar credenciais da conta TUTOR-A. 3) Selecionar Entrar. 4) Verificar painel inicial. 5) Capturar a tela sem credenciais.

### MAN02 — Negar ação administrativa ao tutor
- **Objetivo:** validar autorização por papel.
- **Entrada:** sessão TUTOR-A, URL `/pets`.
- **Saída esperada:** acesso negado (`/acesso-negado` ou página de acesso negado), sem dados administrativos apresentados.
- **Passos:** 1) Entrar como TUTOR-A. 2) Acessar diretamente `/pets`. 3) Confirmar mensagem de acesso negado. 4) Verificar que listagem não foi exposta.

### MAN03 — Impedir acesso a pet de outro tutor
- **Objetivo:** validar isolamento de dados por proprietário.
- **Entrada:** TUTOR-A, PET-B pertencente a TUTOR-B (ID real do PET-B definido no preparo de QA).
- **Saída esperada:** pet de TUTOR-B não aparece na sessão A; URL `/minha-area/pets/{idPetB}` falha sem expor dados.
- **Passos:** 1) Criar TUTOR-A, TUTOR-B e seus pets. 2) Identificar ID do PET-B. 3) Entrar como TUTOR-A. 4) Abrir a URL do PET-B. 5) Confirmar bloqueio e ausência de informações.

### MAN04 — Cadastrar pet válido
- **Objetivo:** criar pet e validar persistência.
- **Entrada:** ADMIN, nome `QA-S4-PET-01`, espécie `CACHORRO`, raça `Labrador`, peso `24.5`, tutor `TUTOR-A`.
- **Saída esperada:** cadastro concluído e página de detalhes do pet com os mesmos valores.
- **Passos:** 1) Entrar como ADMIN. 2) Abrir `/pets/novo`. 3) Preencher os dados fixos e tutor de QA. 4) Salvar. 5) Abrir `/pets`, pesquisar o nome e validar os valores.

### MAN05 — Impedir peso inválido
- **Objetivo:** validar regras de formulário.
- **Entrada:** ADMIN, nome `QA-S4-PET-INVALIDO`, peso `0`, espécie `CACHORRO`, tutor `TUTOR-A`.
- **Saída esperada:** mensagem de validação do peso; nenhum cadastro com esse nome.
- **Passos:** 1) Entrar como ADMIN. 2) Abrir `/pets/novo`. 3) Informar peso `0` e demais campos obrigatórios. 4) Salvar. 5) Verificar erro e ausência na listagem.

### MAN06 — Agendar evento clínico
- **Objetivo:** validar agendamento e visibilidade do evento.
- **Entrada:** DOUTOR, PET-A, tipo `CHECKUP`, data `D+2` (registrar data absoluta na execução), descrição `Check-up preventivo QA`.
- **Saída esperada:** evento `PENDENTE`, associado ao PET-A, visível na agenda e na área do tutor.
- **Passos:** 1) Entrar como DOUTOR. 2) Abrir `/eventos/novo`. 3) Selecionar PET-A, tipo, data e descrição. 4) Salvar. 5) Validar detalhe e posteriormente histórico na sessão TUTOR-A.

### MAN07 — Concluir um evento
- **Objetivo:** registrar atendimento com persistência e exibição ao tutor.
- **Entrada:** DOUTOR, evento criado em MAN06, observação `Acompanhamento preventivo realizado em ambiente de QA`.
- **Saída esperada:** evento `CONCLUIDO`, responsável e observação registrados; tutor visualiza orientação.
- **Passos:** 1) Entrar como DOUTOR. 2) Abrir `/eventos/{idEvento}`. 3) Informar observação controlada. 4) Selecionar Atender. 5) Confirmar status e conferir histórico na área do tutor.

### MAN08 — Rejeitar segunda conclusão
- **Objetivo:** proteger integridade do evento concluído.
- **Entrada:** mesmo ID de MAN07 já `CONCLUIDO`, observação `Tentativa de repetição QA`.
- **Saída esperada:** operação recusada e observação original preservada.
- **Passos:** 1) Usar evento já concluído. 2) Tentar repetir a ação `/eventos/{id}/atender` com formulário válido e CSRF. 3) Conferir recusa. 4) Revisitar detalhe para validar a observação original.

### MAN09 — Enviar relato pelo tutor
- **Objetivo:** registrar alerta a partir de percepção do tutor.
- **Entrada:** TUTOR-A, PET-A, texto `QA: recipiente de água precisa de verificação`, prioridade `MEDIA` (ou opção equivalente disponível no formulário).
- **Saída esperada:** relato gerando alerta associado a PET-A e visível para equipe veterinária.
- **Passos:** 1) Entrar como TUTOR-A. 2) Abrir `/minha-area/pets/{idPetA}`. 3) Preencher urgência e relato. 4) Enviar. 5) Entrar como DOUTOR e localizar o alerta criado.

### MAN10 — Acompanhar e resolver alerta
- **Objetivo:** validar acompanhamento clínico e resolução persistida.
- **Entrada:** DOUTOR, alerta criado em MAN09, anotação `Verificação registrada em QA`, resolução `Recipiente conferido em QA`.
- **Saída esperada:** veterinário responsável; anotação no histórico; status resolvido com nota de resolução.
- **Passos:** 1) Entrar como DOUTOR. 2) Abrir `/alertas/{idAlerta}`. 3) Assumir. 4) Registrar anotação. 5) Resolver com texto fixo. 6) Verificar status e resultado exibido para o tutor.

### MAN11 — Regra ambiental de Zakaria
- **Objetivo:** validar prioridades determinísticas dos sensores.
- **Entrada:** `nivel_agua=12`, `nivel_racao=8`, `temperatura=32`, `umidade=78`, evento CHECKUP PENDENTE; token autorizado ou demo local.
- **Saída esperada:** `POST /api/alertas` HTTP 200, `quantidade_alertas=4`, prioridades `[ALTA, MEDIA, ALTA, MEDIA]` na ordem água, ração, temperatura, umidade.
- **Passos:** 1) Iniciar FastAPI com autenticação/demonstração adequada. 2) Abrir `/docs` ou Insomnia. 3) Enviar JSON fixo de `data/cenario_alerta.json`. 4) Verificar status 200. 5) Comparar cada tipo, prioridade e quantidade com o esperado.

### MAN12 — Orientação preventiva de Lara
- **Objetivo:** comprovar fluxo generativo real sem alertas.
- **Entrada:** água `75`, ração `65`, temperatura `24`, umidade `50`, evento CHECKUP CONCLUIDO, chave OpenAI válida.
- **Saída esperada:** `POST /api/analisar` HTTP 200, `quantidade_alertas=0`, `origem=OPENAI_RESPONSES_API`, texto de orientação e aviso de uso responsável.
- **Passos:** 1) Iniciar API configurada. 2) Enviar `data/cenario_normal.json`. 3) Validar HTTP/origem/alertas. 4) Ler resposta para verificar ausência de diagnóstico/prescrição. 5) Guardar tela com dados sintéticos, sem chave.

### MAN13 — Orientação pós-operatório de Bolt
- **Objetivo:** comprovar uso do contexto clínico e regras separadas da geração.
- **Entrada:** água `18`, ração `6.5`, temperatura `29.5`, umidade `55`, evento POS_OPERATORIO, chave OpenAI válida.
- **Saída esperada:** HTTP 200, três alertas (água ALTA, ração MEDIA, acompanhamento clínico ALTA), orientação contextual e aviso; **sem dose/prescrição nova**.
- **Passos:** 1) Enviar `data/cenario_pos_operatorio.json` a `/api/analisar`. 2) Verificar os três alertas. 3) Validar origem OpenAI. 4) Revisar conteúdo gerado. 5) Capturar evidência. Em caso de filtro de segurança retornar 503, registrar como rejeição segura, não como sucesso gerativo.

### MAN14 — Falha segura do serviço generativo
- **Objetivo:** impedir simulação silenciosa de IA quando a chave falta.
- **Entrada:** FastAPI com `CLYVO_LOCAL_DEMO=true` em loopback e `OPENAI_API_KEY` vazia; JSON de Lara.
- **Saída esperada:** `/api/analisar` → 503, com erro claro; `/api/alertas` → 200, com zero alertas e `ia_generativa_utilizada=false`.
- **Passos:** 1) Iniciar API sem chave no servidor de QA. 2) Fazer POST para `/api/analisar` com JSON fixo. 3) Confirmar 503. 4) Repetir para `/api/alertas`. 5) Confirmar 200 e zero alertas. 6) Registrar logs sem segredos.

## Critério de conclusão e alinhamento

- **Manual:** cadastrar e vincular no Azure Boards cada caso às Features/PBIs funcionais efetivamente implementadas. Atualizar os critérios de aceite seguindo o padrão exigido pelo professor e vincular ao release plan. **Não inventar IDs**.
- **Execução:** preencher `Resultado real`, `Passou/Falhou/Bloqueado`, data e evidência. Casos Java devem ser comprovados no sistema Java; não basta os dez/21 testes do Python.
- **Automação:** quatro casos sem LLM em `qa-postman-collection.json` e testes Python em `tests/test_sprint4.py`. Executar e gravar vídeo mostrando ferramenta, configuração, execução e resultado.
- **Entrega:** Branch `develop` de repositório público contendo links corretos Azure Boards e vídeo. Professor com nível **Basic** na organização e **Administrador** no projeto.
