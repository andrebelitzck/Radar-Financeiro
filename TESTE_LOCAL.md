# Teste Local

## Rodar os testes

```powershell
python -m pytest
```

## Verificar o serviço

```powershell
uvicorn main:app --reload
```

## Endpoints principais

- `GET /`
- `GET /health`
- `POST /sync/push`
- `GET /sync/pull`
- `GET /sync/status`
