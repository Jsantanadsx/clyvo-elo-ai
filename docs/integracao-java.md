# Integração do componente de IA com o painel Java do grupo

Painel Spring Boot: https://github.com/GabrielCabralmm/clyvo-elo-java

O painel já possui área do tutor, alertas e página `/ecossistema`. O serviço de IA pode ser chamado pelo backend Spring Boot com `RestClient`, de modo que **o navegador do tutor não precise acessar diretamente o endpoint Python**, e a credencial não fique exposta ao usuário.

## Contrato HTTP

- `POST /api/alertas`: recebe dados de pet, sensores e evento; retorna tipos e prioridades por regras.
- `POST /api/analisar`: recebe os mesmos dados e retorna os alertas MAIS `orientacao` gerada por LLM real.
- Cabeçalhos: `Content-Type: application/json` e, caso `CLYVO_API_TOKEN` esteja configurado no Python, `X-CLYVO-TOKEN: <token>`.
- `503`: modelo indisponível ou sem configuração; apresentar erro amigável e permitir exibir apenas alertas, sem fingir geração.
- `422`: JSON inválido; validar formulário antes de enviar.
- `GET /health`: status do serviço e indicação se chave está configurada (não revela credenciais).

## Próxima etapa obrigatória para integração com painel final

1. Criar serviço Java `ClyvoAiClient` chamando `/api/analisar` com `RestClient`.
2. No fluxo do pet do tutor, obter dados **autorizados** do banco (pet/eventos) e leituras de sensores disponíveis; não inventar que sensores simulados sejam reais.
3. Criar botão e apresentar orientação na área do tutor, mantendo a autenticação do Spring Security e validação de propriedade do pet.
4. Tratar timeout e `503` e testar ao menos um fluxo ponta a ponta.
5. Configurar `CLYVO_AI_URL` e `CLYVO_AI_TOKEN` como variáveis do servidor Java.

**Situação nesta entrega:** esta pasta contém o contrato e um painel de demonstração funcional do serviço Python. A integração final no painel Java deve ser implementada e testada separadamente; não a declare concluída antes de executar o fluxo ponta a ponta.
