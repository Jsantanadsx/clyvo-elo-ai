# Casos de teste MANUAIS de sistema — CLYVO Elo (proposta para Azure Boards)

**Status:** casos planejados; **não** foram executados ou cadastrados no Azure Boards. Validar contra os PBIs e release plan reais antes da importação/cadastro.

**Pré-condições gerais:** base de teste com dados sintéticos descartáveis, acesso aos perfis administrador/veterinário/tutor, aplicação Java e banco acessíveis. Cada caso precisa registrar resultado **obtido**, data, responsável, PBI e evidência. Não use dados pessoais ou de prontuário real.

| Caso | Objetivo | Entrada controlada | Saída esperada | Procedimento básico |
|---|---|---|---|---|
| MAN01 | Login válido do tutor | Conta sintética do perfil `TUTOR`, senha configurada no ambiente de teste | Autenticar; redirecionar para a área do tutor | Abrir `/login`, informar credenciais de teste, confirmar área do tutor |
| MAN02 | Proteger menu administrativo | Perfil `TUTOR` autenticado; URL `/pets` | HTTP 403 / acesso negado, sem dados administrativos | Logar como tutor, acessar `/pets` diretamente, registrar bloqueio |
| MAN03 | Restringir consulta de outro pet | Tutor A autenticado; ID do pet atribuído ao Tutor B | HTTP 404; não expor dados do outro tutor | Criar dois tutores e pets de teste, logar como A, acessar a URL do pet B |
| MAN04 | Cadastrar um pet | Admin autenticado; nome `QA-S4-Pet-01`; espécie e peso válidos | Pet criado, visível na lista, dados persistidos | Abrir cadastro, preencher valores controlados, salvar e consultar |
| MAN05 | Impedir formulário inválido | Admin autenticado; peso `0` kg | Campo inválido, registro não criado | Abrir cadastro, preencher peso `0`, tentar salvar, verificar mensagem |
| MAN06 | Agendar evento clínico | Veterinário autenticado; pet de teste; tipo de evento e data futura | Evento `PENDENTE` aparece na agenda e área do tutor | Agendar, abrir agenda, entrar como tutor e confirmar evento |
| MAN07 | Concluir atendimento | Evento `PENDENTE`; nota de orientação com 20–50 caracteres | Status `CONCLUIDO`, data e responsável salvos, orientação visível ao tutor | Abrir evento, concluir, consultar registros e área do tutor |
| MAN08 | Impedir atendimento repetido | Mesmo evento já concluído do MAN07 | Rejeitar segunda conclusão; não sobrescrever dados | Tentar abrir/reenviar ação de conclusão do evento |
| MAN09 | Enviar relato pelo tutor | Tutor autorizado; pet próprio; descrição `QA teste: reduziu o apetite hoje` e prioridade permitida | Alerta criado com origem tutor, aparece para veterinário | Enviar relato, logar como veterinário, consultar fila de alertas |
| MAN10 | Assumir e resolver alerta | Alerta aberto do MAN09; veterinário autenticado; anotação e resolução sintéticas | Responsável, acompanhamento e status de resolução persistidos | Assumir, registrar acompanhamento, resolver, consultar linha do tempo |
| MAN11 | Classificar cenário IoT Zakaria | JSON sintético: água=12, ração=8, temperatura=32, umidade=78 | HTTP 200; 4 alertas com prioridades ALTA/MÉDIA/ALTA/MÉDIA | POST `/api/alertas`, validar os quatro campos de saída |
| MAN12 | Gerar orientação OpenAI para Lara | JSON: água=75, ração=65, temperatura=24, umidade=50; API com chave válida | HTTP 200; `origem=OPENAI_RESPONSES_API`, 0 alertas, orientação textual | POST `/api/analisar`, validar origem, ausência de alertas e texto |
| MAN13 | Gerar orientação OpenAI para Bolt | JSON com `POS_OPERATORIO`, água=18, ração=6.5, temperatura=29.5, umidade=55 | HTTP 200; 3 alertas, texto de acompanhamento; sem diagnóstico | POST `/api/analisar`, validar três alertas e orientação |
| MAN14 | Tratar indisponibilidade da IA | Desligar provedor ou omitir chave no servidor de teste | `/api/analisar` → HTTP 503 e sem fingir geração; `/api/alertas` continua funcional | Parar servidor com chave, reiniciar sem chave, repetir requisições |

## Para cadastrar no Azure Boards

1. Vincule cada MANxx à **Feature/PBI existente** que efetivamente implementa o fluxo (não invente IDs).
2. No item de teste, use campos separados: **Objetivo**, **Dados de entrada (valores)**, **Resultado esperado**, **Passos numerados**, **Resultado obtido**, **Evidências** e **Status**.
3. Registre configurações de massa de dados e identidades sintéticas sem publicar senhas ou tokens.
4. Alinhe os casos MAN01–MAN10 ao release plan do painel Java. Os casos MAN11–MAN14 pertencem à funcionalidade de IA e ao plano de implementação confirmado.
5. O professor exige acesso **Basic** à organização e **Administrador** no projeto; confira isso antes da entrega.
6. **Não marque como aprovado caso que ainda não tenha sido executado.**
