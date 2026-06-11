# Radar Financeiro Backend

Backend leve em FastAPI para preparar sincronização incremental entre desktop, app futuro e banco em nuvem.

## Como rodar localmente

```powershell
cd /d D:\ProjetosPython\RadarFinanceiro_Backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

## Variáveis de ambiente

Use `RADAR_*` no `.env` local:

- `RADAR_ENV=development`
- `RADAR_DATABASE_URL=sqlite:///./radar_sync_dev.db`
- `RADAR_SECRET_KEY=change-me`
- `RADAR_ALLOW_TEST_AUTH=true`

## Rotas principais

- `GET /`
- `GET /health`
- `GET /sync/status`
- `POST /sync/push`
- `GET /sync/pull`

## Avisos

- Não usar `.env` real no GitHub.
- Não subir banco real, logs ou segredos.
- Esta etapa ainda é de teste e preparação.
- Em produção futura, o ideal é PostgreSQL/Supabase com autenticação e HTTPS.
