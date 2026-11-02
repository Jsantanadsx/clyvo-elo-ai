# Sprint 4 - prepara um CLONE separado para publicacao (sem commit/push automatico).
# Execute a partir do PowerShell: .\PREPARAR-PUBLICACAO-GITHUB.ps1
$ErrorActionPreference = 'Stop'

$origem = Split-Path -Parent $MyInvocation.MyCommand.Path
$destino = Join-Path (Split-Path -Parent $origem) 'clyvo-elo-ai-git'

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git nao encontrado. Instale o Git for Windows ou use Git Bash.'
}
if (Test-Path $destino) {
    throw "A pasta $destino ja existe. Renomeie-a antes de continuar para evitar sobrescrita acidental."
}

Write-Host 'Clonando repositorio original, preservando o historico...' -ForegroundColor Cyan
git clone 'https://github.com/Jsantanadsx/clyvo-elo-ai.git' $destino
if ($LASTEXITCODE -ne 0) { throw 'Falha no git clone.' }
Push-Location $destino
try {
    git switch -c 'sprint4-ia-generativa'
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar branch.' }

    $itens = @(
        'README.md', 'COMECE-AQUI.md', 'PREPARAR-PUBLICACAO-GITHUB.ps1',
        'requirements.txt', 'requirements-dev.txt', '.env.example',
        'app', 'data', 'docs', 'static', 'tests', 'evidencias', 'qa-postman-collection.json'
    )
    foreach ($item in $itens) {
        $src = Join-Path $origem $item
        if (-not (Test-Path $src)) { throw "Item ausente: $item" }
        Copy-Item -LiteralPath $src -Destination $destino -Recurse -Force
    }

    # Mantem o .gitignore do repositorio clonado e garante exclusoes essenciais.
    $gitignore = Join-Path $destino '.gitignore'
    Add-Content -Path $gitignore -Encoding utf8 -Value "`n# Sprint 4: arquivos locais/sensiveis`n.env`n.env.*`n!.env.example`n.venv/`n__pycache__/`n.pytest_cache/`n*.pyc`n"

    # Evita que tokens locais sejam copiados ou adicionados ao Git.
    if (Test-Path (Join-Path $destino '.env')) { throw 'Foi encontrado um .env no clone; remova-o antes de publicar.' }

    git add -- README.md COMECE-AQUI.md PREPARAR-PUBLICACAO-GITHUB.ps1 `
        requirements.txt requirements-dev.txt .env.example .gitignore app data docs static tests evidencias qa-postman-collection.json
    if ($LASTEXITCODE -ne 0) { throw 'Falha no git add.' }

    Write-Host "`nRevisao: arquivos preparados na branch sprint4-ia-generativa:" -ForegroundColor Green
    git status --short
    Write-Host "`nNenhum commit ou push foi executado automaticamente." -ForegroundColor Yellow
    Write-Host "Confira o git status e, se estiver correto, execute:`n" -ForegroundColor Cyan
    Write-Host "cd `"$destino`""
    Write-Host 'git diff --cached --stat'
    Write-Host 'git commit -m "feat: integrar IA generativa e evidencias da sprint 4"'
    Write-Host 'git push -u origin sprint4-ia-generativa'
    Write-Host 'Depois abra Pull Request de sprint4-ia-generativa para main.'
}
finally { Pop-Location }
