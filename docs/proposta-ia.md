# CLYVO AI — Proposta de Inteligência Artificial

## 1. Visão Geral

O CLYVO Elo é uma solução voltada à continuidade do cuidado veterinário nos
intervalos entre consultas.

A proposta combina três frentes principais:

- acompanhamento preventivo;
- continuidade terapêutica;
- monitoramento contínuo do bem-estar por meio de dispositivos IoT.

Dentro dessa solução, o **CLYVO AI** representa o componente inteligente
responsável por analisar informações provenientes do acompanhamento do pet,
identificar situações relevantes e produzir orientações contextualizadas para
o tutor.

A Inteligência Artificial atua como ferramenta de apoio e não como substituta
da avaliação realizada por um médico-veterinário.


## 2. Problema de Negócio

Grande parte do acompanhamento de um animal acontece fora da clínica
veterinária.

Durante esse período, informações importantes podem ser geradas por sensores,
pelo histórico clínico e pelo próprio acompanhamento do tratamento, mas esses
dados isolados nem sempre são facilmente interpretados pelo tutor.

Por exemplo, um dispositivo pode identificar:

- redução do nível de água;
- redução do nível de ração;
- temperatura ambiental elevada;
- umidade fora do padrão.

Além disso, o animal pode estar passando por uma situação clínica específica,
como acompanhamento pós-operatório ou utilização de medicamentos.

O problema tratado pelo CLYVO AI consiste em transformar esses diferentes
dados em informações priorizadas e compreensíveis, auxiliando o tutor a
identificar quando determinada situação merece atenção.


## 3. Solução Proposta

O CLYVO AI utiliza uma abordagem híbrida composta por:

1. motor de regras;
2. componente de Inteligência Artificial Generativa.

O motor de regras analisa dados estruturados e identifica situações
previamente definidas como relevantes.

Exemplos:

- nível de água abaixo do limite esperado;
- nível de ração abaixo do limite esperado;
- temperatura acima do limite;
- umidade fora da faixa esperada;
- existência de acompanhamento pós-operatório.

Após essa análise, os alertas identificados são enviados para uma camada de
IA Generativa, responsável por utilizar o contexto disponível para produzir
uma orientação personalizada e de fácil compreensão.

Dessa forma, regras determinísticas são utilizadas para identificar condições
objetivas, enquanto a IA Generativa é utilizada para contextualização e
comunicação.


## 4. Abordagem de Inteligência Artificial

A abordagem escolhida é a combinação de um **motor de regras inteligentes com
IA Generativa baseada em LLM (Large Language Model)**.

### Motor de regras

O motor de regras é adequado para condições objetivas e verificáveis.

Exemplo:

```text
SE nivel_agua < limite
ENTÃO gerar alerta de nível de água