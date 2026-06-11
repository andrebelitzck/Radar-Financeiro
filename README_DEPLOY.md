# Deploy do Radar Financeiro Backend

Esta API ainda é um ambiente de teste.
Não conectar dados reais.
Não usar em produção sem autenticação, HTTPS, banco PostgreSQL e validações finais.

## 1. Rodar localmente

```powershell
cd /d D:\ProjetosPython\RadarFinanceiro_Backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

## 2. Variáveis de ambiente

Use um arquivo `.env` local com exemplos como:

```env
RADAR_ENV=development
RADAR_DATABASE_URL=sqlite:///./radar_sync_dev.db
RADAR_SECRET_KEY=change-me
RADAR_ALLOW_TEST_AUTH=true
CORS_ORIGINS=
```

## 3. Publicar em host de teste

### Opção Docker

- build da imagem usando o `Dockerfile`
- definir a variável `PORT` do host
- iniciar com `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Opção Heroku/Render-like

- usar o `Procfile`
- configurar as variáveis de ambiente no painel do host
- apontar o deploy para o branch `main`

## 4. Validar `/health`

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health -UseBasicParsing
```

Resposta esperada:

```json
{"status":"ok","service":"Radar Financeiro Backend"}
```

## 5. Testar `/sync/push`

Enviar um payload com um registro de teste via `POST /sync/push` e confirmar `received`, `created` e `updated`.

## 6. Testar `/sync/pull`

Consultar com `GET /sync/pull?user_id=...` e verificar se o registro enviado aparece.

## 7. O que ainda não está pronto para produção

- autenticação real
- autorização por usuário
- banco PostgreSQL/Supabase em produção
- estratégia final de migração de dados
- observabilidade e monitoramento

## 8. Aviso final

Esta API ainda é ambiente de teste.
Não conectar dados reais.
Não usar em produção sem autenticação, HTTPS, banco PostgreSQL e validações finais.
