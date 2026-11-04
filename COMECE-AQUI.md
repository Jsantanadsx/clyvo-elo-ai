# Comece aqui — CLYVO Elo AI | Sprint 4 de IoT, IoB e IA Generativa

Esta é a entrada rápida para quem vai avaliar a entrega de **IoT/IA**.

## Aplicação publicada

- [Interface Python](https://clyvo-elo-ai-python.onrender.com)
- [Estado da API Python](https://clyvo-elo-ai-python.onrender.com/health)
- [Documentação FastAPI](https://clyvo-elo-ai-python.onrender.com/docs)
- [Painel Java integrado](https://clyvo-elo-java.onrender.com)
- [Vídeo da Sprint 4](https://youtu.be/6hMTqWkoWbM)
- [Código e documentação](https://github.com/Jsantanadsx/clyvo-elo-ai)

As instâncias gratuitas do Render podem hibernar. O endpoint `/health` pode ser acessado antes da demonstração. O token usado nos POSTs deve ser fornecido pelo responsável autorizado; não foi publicado no repositório.

## Testar localmente (Windows PowerShell)

```powershell
git clone https://github.com/Jsantanadsx/clyvo-elo-ai.git
cd clyvo-elo-ai
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe app/main.py --cenario 2 --somente-regras
```

A geração de IA real precisa de `OPENAI_API_KEY` configurada como segredo em sessão local, de internet e de créditos. Para uma demo **apenas em loopback**, defina `CLYVO_LOCAL_DEMO=true` e inicie:

```powershell
$env:CLYVO_LOCAL_DEMO = "true"  # exclusivamente localhost
$env:OPENAI_MODEL = "gpt-4o-mini"
.\.venv\Scripts\python.exe -m uvicorn app.api:app --host 127.0.0.1 --port 8000
```

Configure também `OPENAI_API_KEY` em variável privada antes de gerar orientações. **Não** habilite modo sem token em uma hospedagem pública. Os cenários disponíveis são Lara (0 alertas), Zakaria (4) e Bolt (3), todos sintéticos.

## Entrega

O arquivo [docs/links-entrega-iot.txt](docs/links-entrega-iot.txt) reúne GitHub, YouTube e serviços publicados. Conferir que o vídeo está **Não listado** e acessível sem autenticar como dono antes de enviar o ZIP pedido pelo professor.
