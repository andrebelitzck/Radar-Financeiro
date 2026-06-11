# Testar API Pública do Radar Financeiro

Esta API ainda é um ambiente de teste.
Não conectar dados reais.
Não usar em produção sem autenticação, HTTPS, banco PostgreSQL e validações finais.

## URLs para teste

Substitua `SUA-API-AQUI` pela URL pública do host de teste:

- `https://SUA-API-AQUI/`
- `https://SUA-API-AQUI/health`
- `https://SUA-API-AQUI/sync/status`
- `https://SUA-API-AQUI/sync/push`
- `https://SUA-API-AQUI/sync/pull?user_id=usuario_teste`

## 1. Testar health

```powershell
Invoke-WebRequest https://SUA-API-AQUI/health -UseBasicParsing
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "Radar Financeiro Backend"
}
```

## 2. Testar push

Exemplo com dados fictícios:

```json
{
  "user_id": "usuario_teste",
  "device_id": "desktop-teste",
  "records": [
    {
      "uuid": "11111111-1111-1111-1111-111111111111",
      "entity_type": "categorias",
      "payload": {
        "nome": "Categoria Teste"
      },
      "created_at": "2026-06-10T10:00:00",
      "updated_at": "2026-06-10T10:00:00",
      "deleted_at": null
    }
  ]
}
```

Exemplo PowerShell:

```powershell
$body = @{
  user_id = 'usuario_teste'
  device_id = 'desktop-teste'
  records = @(
    @{
      uuid = '11111111-1111-1111-1111-111111111111'
      entity_type = 'categorias'
      payload = @{ nome = 'Categoria Teste' }
      created_at = '2026-06-10T10:00:00'
      updated_at = '2026-06-10T10:00:00'
      deleted_at = $null
    }
  )
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri https://SUA-API-AQUI/sync/push -Method Post -ContentType 'application/json' -Body $body
```

## 3. Testar pull

```powershell
Invoke-WebRequest 'https://SUA-API-AQUI/sync/pull?user_id=usuario_teste' -UseBasicParsing
```

## 4. Host de teste

Use o plano gratuito disponível, se houver, ou um ambiente de teste de baixo custo.

Passos gerais:

1. conectar o repositório GitHub
2. escolher a branch `main`
3. configurar o build command
4. configurar o start command
5. configurar as variáveis de ambiente
6. publicar
7. testar `/health`

## 5. Variáveis de ambiente

- `RADAR_ENV=development`
- `RADAR_DATABASE_URL=sqlite:///./radar_sync_dev.db`
- `RADAR_SECRET_KEY=change-me`
- `RADAR_ALLOW_TEST_AUTH=true`
- `CORS_ORIGINS=`

## 6. O que ainda não está pronto

- autenticação real
- autorização por usuário
- produção com HTTPS obrigatório
- PostgreSQL/Supabase em produção
- validações finais de segurança
