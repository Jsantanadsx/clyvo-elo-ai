# Atualizar PR #1 após o Code Review — Windows PowerShell

O diretório de trabalho já publicado é `C:\Users\Santana\Desktop\clyvo-elo-ai-git` (branch `sprint4-ia-generativa`). **Não execute `PREPARAR-PUBLICACAO-GITHUB.ps1` novamente**.

1. Extraia o pacote `CLYVO_ELO_SPRINT4_CR_CORRIGIDO.zip` numa nova pasta, por exemplo `C:\Users\Santana\Desktop\clyvo-elo-ai-sprint4-cr`.
2. Abra PowerShell na pasta extraída e execute `Unblock-File .\ATUALIZAR-PR1.ps1` e ` .\ATUALIZAR-PR1.ps1`. O script confere a branch e copia apenas os arquivos da revisão. **Não apaga `.git`, não copia `.venv` e não faz commit/push.**
3. No PowerShell dentro de `clyvo-elo-ai-git`:

```powershell
cd "C:\Users\Santana\Desktop\clyvo-elo-ai-git"
git branch --show-current
# Esperado: sprint4-ia-generativa
.\..\clyvo-elo-ai-sprint4\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\..\clyvo-elo-ai-sprint4\.venv\Scripts\python.exe -m pytest -q
# Esperado: 21 passed (sem chamadas pagas)
git status --short
git add app/api.py app/ai_service.py tests/test_sprint4.py README.md COMECE-AQUI.md .env.example docs .github
# Se o JSON da coleção tiver sido atualizado, incluir com git add qa-postman-collection.json
git diff --cached --check
git diff --cached --stat
git commit -m "fix: reforcar autenticacao validacao de IA e cobertura sprint 4"
git push origin sprint4-ia-generativa
```

4. O PR aberto em `https://github.com/Jsantanadsx/clyvo-elo-ai/pull/1` recebe o commit automaticamente.
5. Em **Actions**, verificar o workflow `Python CI — regras e API` com aprovação. Se a execução não aparecer por restrição da conta, registrar execução local e não declarar CI aprovada.
6. **Teste manual depois da atualização**: para modo local, na janela que inicia Uvicorn configure:

```powershell
$env:CLYVO_LOCAL_DEMO = "true"
$env:OPENAI_API_KEY = Read-Host "Chave OpenAI (nao publique)"
$env:OPENAI_MODEL = "gpt-4o-mini"
.\.venv\Scripts\python.exe -m uvicorn app.api:app --host 127.0.0.1 --port 8000
```

Opcional para integração servidor-servidor: configure `CLYVO_API_TOKEN` em Python e o mesmo valor em `CLYVO_AI_TOKEN` no Java, sem ligar o modo local. As rotas POST ficam fechadas se nenhum modo explícito/token estiver definido.

7. Execute Lara, Zakaria e Bolt; após a nova camada de validação, a chamada pode retornar 503 se o modelo incluir linguagem clínica inadequada. Isso é falha segura deliberada; não reporte tal resposta como aprovação generativa.
8. **Antes de fazer merge:** confirmar que integração Java, QA no Azure e vídeos estão com status real documentado.
