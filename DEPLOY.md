# Deploy

## Objetivo

Subir o Radar Financeiro Backend em nuvem com baixo consumo de dados e sem mudar o contrato de sincronização.

## Preparação

- configurar `DATABASE_URL` para PostgreSQL/Supabase
- configurar `CORS_ORIGINS` se houver cliente web no futuro
- manter `POST /sync/push` e `GET /sync/pull` como contrato estável

## Build local com Docker

```powershell
docker build -t radar-financeiro-backend .
docker run -p 8000:8000 radar-financeiro-backend
```

## Variáveis de ambiente sugeridas

- `APP_NAME`
- `ENVIRONMENT`
- `DATABASE_URL`
- `CORS_ORIGINS`

## Observação

- não usar dados reais nesta etapa
- não conectar desktop ainda
- não conectar Android ainda
- não criar login real ainda
