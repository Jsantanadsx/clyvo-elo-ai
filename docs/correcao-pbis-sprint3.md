# Correção orientada pelo feedback de QA da Sprint 3

Feedback do professor: (1) mais da metade dos PBIs não descrevia funcionalidades do ponto de vista do usuário (-10); (2) critérios de aceite fora do padrão de sala (-10).

**Importante:** estes itens são **modelos propostos**; antes de alterar o Azure Boards, é preciso ler os work items existentes e ajustar somente os que não correspondem a histórias de usuário. Não afirmamos ter corrigido a organização on-line.

## Regras de revisão

- PBI = capacidade de negócio percebida pela persona: **Como [persona], quero [ação/necessidade], para [benefício]**.
- Task = implementação técnica necessária para o PBI; exemplos: implementar endpoint, criar tabela, construir componente, preparar deploy, escrever teste.
- Critérios de aceite: condições concretas e testáveis, preferencialmente **Dado / Quando / Então**; seguir a convenção específica ensinada pelo professor caso seja diferente.
- Prioridade, esforço, dependências, sprint e critérios precisam corresponder ao release plan do Azure Boards.

## Exemplos de PBIs orientados à jornada real do CLYVO Elo

### PBI-EX01 — Consultar meus pets (Tutor)

**Como** tutor autenticado, **quero** visualizar os pets vinculados à minha conta, **para** acompanhar os cuidados de cada animal.

- Dado que estou autenticado como tutor e tenho pets vinculados, quando acessar minha área, então o sistema exibe somente meus pets.
- Dado que estou autenticado como tutor, quando tentar consultar por URL o pet de outra pessoa, então o acesso será negado sem exposição dos dados.

**Tasks técnicas possíveis:** consulta filtrada no banco, controller, template, testes de autorização.

### PBI-EX02 — Relatar uma situação observada no pet (Tutor)

**Como** tutor, **quero** registrar um relato sobre meu pet, **para** informar a clínica sobre uma situação que merece acompanhamento.

- Dado que sou tutor autorizado do pet, quando envio um relato válido, então o sistema registra o alerta e o disponibiliza para a equipe veterinária.
- Dado que não sou autorizado para o pet, quando tento registrar um relato, então o sistema bloqueia a operação.

**Tasks possíveis:** formulário, serviço de alerta, validação, teste de API/UI.

### PBI-EX03 — Acompanhar alertas (Veterinário)

**Como** veterinário, **quero** assumir e acompanhar os alertas de pets, **para** registrar as ações de acompanhamento realizadas pela clínica.

- Dado um alerta disponível, quando o veterinário o assume, então o sistema registra o profissional responsável e atualiza o status.
- Dado um alerta resolvido, quando alguém tenta adicionar um novo acompanhamento, então o sistema impede a alteração.

**Tasks possíveis:** regras no domínio, registro de acompanhamento, interface, testes.

### PBI-EX04 — Receber orientação sobre dados monitorados (Tutor)

**Como** tutor, **quero** visualizar uma orientação compreensível baseada nos alertas monitorados do meu pet, **para** saber o que verificar e quando contatar a clínica.

- Dado um conjunto válido de leituras, quando solicito a análise, então vejo os alertas classificados pelo motor de regras.
- Dado que o provedor de IA está disponível, quando solicito orientação, então uma resposta contextual gerada por IA é exibida com aviso de que não substitui o veterinário.
- Dado que o provedor de IA está indisponível, quando solicito orientação, então o sistema apresenta erro compreensível e não inventa uma resposta gerada.

**Tasks possíveis:** integração Python/OpenAI, endpoint HTTP, controle de erro, teste end-to-end.

## Procedimento no Azure Boards

1. Entrar no projeto existente e exportar a lista de PBIs atuais (não criar uma nova organização).
2. Para cada PBI, perguntar: "isso é algo que o tutor, veterinário ou clínica percebe e valoriza?".
3. Se for infraestrutura ou implementação interna, transformá-lo em Task (ou reclassificar conforme a hierarquia disponível).
4. Corrigir critérios de aceite de cada PBI com entradas, ações e saídas verificáveis.
5. Validar esforço/prioridade/sprint original e vínculos de dependência.
6. Vincular o plano de testes do Azure Boards aos PBIs da Sprint 4 e conferir acesso Basic + Admin do professor.
