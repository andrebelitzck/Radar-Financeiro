# Radar Financeiro Backend

Backend leve em FastAPI para preparar sincronização incremental entre desktop, app futuro e banco em nuvem.

## O que é

Este projeto expõe um contrato mínimo de sincronização local com SQLite de desenvolvimento, pronto para evoluir depois para PostgreSQL/Supabase.

## Instalação

```powershell
cd /d D:\ProjetosPython\RadarFinanceiro_Backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Rodar localmente

```powershell
uvicorn main:app --reload
```

## Health check

Acesse:

```text
GET /health
```

Resposta esperada:

```json
{"status":"ok","service":"Radar Financeiro Backend"}
```

## Testar push/pull

### Push

```http
POST /sync/push
```

### Pull

```http
GET /sync/pull?user_id=usuario_teste&since=2026-06-10T10:00:00
```

### Status

```http
GET /sync/status
```

## Avisos

- Esta etapa não usa dados reais.
- Esta etapa não está conectada ao desktop ainda.
- Esta etapa não está conectada ao Android ainda.
- Esta etapa não tem login real ainda.
