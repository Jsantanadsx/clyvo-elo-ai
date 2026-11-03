# CLYVO ELO — COMECE AQUI (Sprint 4)

## 1. Extrair o ZIP e abrir no VS Code

Extraia `clyvo-elo-ai-sprint4-validado.zip` em uma pasta no Windows, por exemplo `C:\Users\Santana\Downloads\clyvo-elo-ai-sprint4`. Depois, abra a pasta no VS Code e um terminal PowerShell.

## 2. Instalar e executar os testes (sem gastar API)

Se ainda não tiver um ambiente virtual, crie com `python -m venv .venv` (no seu Windows o comando `py` não está disponível).

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe app/main.py --cenario 2 --somente-regras
```

Espera-se `21 passed` no pytest e os quatro alertas para Zakaria.

## 3. Fazer a integração real com IA Generativa

**Não envie a chave pelo chat nem a publique no GitHub.** Obtenha uma chave de API da OpenAI em sua própria conta com faturamento habilitado. Na MESMA janela do PowerShell:

```powershell
$env:OPENAI_API_KEY = "SUA_CHAVE_PRIVADA_AQUI"
$env:OPENAI_MODEL = "gpt-4o-mini"
$env:CLYVO_LOCAL_DEMO = "true"  # somente execução local sem token
.\.venv\Scripts\python.exe -m uvicorn app.api:app --host 127.0.0.1 --port 8000
```

Acesse `http://127.0.0.1:8000`. Teste os três cenários com `Executar motor de regras` e `Gerar orientação com IA`. Verifique no resultado a origem `OPENAI_RESPONSES_API`. O provedor requer internet e pode cobrar por uso.

## 4. Preparar QA

- No Insomnia, importar o arquivo `qa-postman-collection.json` como **Postman Collection** (ou abrir no Postman).
- Importar e executar a pasta **QA - 4 testes automatizados**, com a API Python ligada no terminal.
- Conferir o resultado dos quatro testes e registrar vídeo mostrando preparação/configuração/execução.
- O teste `IA REAL` fica separado para não causar chamadas pagas involuntárias.
- Cadastrar os testes MANUAIS também no Azure Boards, com objetivos, dados de entrada, saídas esperadas, passos, vínculos PBI e evidências.

## 5. Aplicar correções do PR #1

Esta revisão já usa a branch `sprint4-ia-generativa` no repositório `clyvo-elo-ai-git`. **Não execute novamente o script de clonagem** nem crie outra branch se estiver atualizando o PR existente.

Copie os arquivos atualizados preservando `.git`, execute `python -m pytest -q`, `git diff --check`, `git add`, `git commit` e `git push` **na branch existente**. Veja `docs/atualizar-pr1.md`.

## 5a. Procedimento original (primeira publicação)

O repositório anterior já existe: https://github.com/Jsantanadsx/clyvo-elo-ai

Depois dos testes, abra **outro terminal** e execute:

```powershell
cd "$env:USERPROFILE\Downloads"
git clone https://github.com/Jsantanadsx/clyvo-elo-ai.git clyvo-elo-ai-git
cd clyvo-elo-ai-git
git checkout -b sprint4-ia-generativa
```

Agora copie os arquivos e pastas da pasta **extraída do ZIP** para dentro de `clyvo-elo-ai-git`, substituindo quando solicitado **sem apagar o `.git`**. Não copie `.venv` nem `.env`. Depois:

```powershell
git add .
git status
git commit -m "feat: integrar IA generativa e testes da sprint 4"
git push -u origin sprint4-ia-generativa
```

Use a versão **validada** deste ZIP, que já inclui capturas de três cenários com chamadas generativas reais e a documentação de evidências. Confira os arquivos na nova branch. Abra um Pull Request `sprint4-ia-generativa` → `main`, revise e faça o merge. Não inclua chave/token.

## 6. Prazo e evidência

- Prazo geral no documento: **04/11/2026**. Conferir o horário efetivo da atividade no portal.
- Pitch IoT: aproximadamente 5 minutos, no YouTube como **não listado**.
- Na entrega de IoT: ZIP contendo o link do vídeo e o link do repositório.
- Na entrega de QA: repositório público contendo, **na branch `develop`**, os links do Azure Boards e do vídeo de automação.
- **Integração final no painel Java ainda não está feita**. Um patch adicional de integração Java foi preparado em `clyvo-elo-java-integracao-sprint4.zip`; é necessário aplicar e testar esse patch no repositório Java antes de declarar integração concluída no vídeo.
