# Sync Contract

## Estratégia de baixo consumo

- sincronizar apenas deltas
- enviar apenas JSON do registro
- não enviar banco inteiro
- não enviar backups
- não enviar logs
- não enviar imagens
- usar `updated_at` como corte incremental
- usar `deleted_at` para exclusões lógicas
- evitar duplicação de dados

## Tabela genérica

`sync_records`

Campos:

- `id`
- `uuid`
- `user_id`
- `entity_type`
- `payload_json`
- `created_at`
- `updated_at`
- `deleted_at`
- `device_id`
- `sync_version`

Índices:

- `idx_sync_user_updated_at`
- `idx_sync_user_entity`
- `idx_sync_uuid`

## Push

Endpoint:

`POST /sync/push`

Entrada:

```json
{
  "user_id": "usuario_teste",
  "device_id": "desktop-001",
  "records": [
    {
      "uuid": "...",
      "entity_type": "entradas",
      "payload": {},
      "created_at": "2026-06-10T10:00:00",
      "updated_at": "2026-06-10T10:01:00",
      "deleted_at": null
    }
  ]
}
```

Regras:

- se `uuid` não existe, cria
- se `uuid` existe e `updated_at` for mais recente, atualiza
- se `deleted_at` vier preenchido, marca como excluído
- nunca apagar fisicamente nesta etapa

Resposta:

```json
{
  "status": "ok",
  "received": 10,
  "created": 4,
  "updated": 6,
  "ignored": 0
}
```

## Pull

Endpoint:

`GET /sync/pull?user_id=usuario_teste&since=2026-06-10T10:00:00`

Retorna apenas o que mudou depois de `since`.

## Compatibilidade futura

Este backend foi desenhado para aceitar desktop e Android depois, com PostgreSQL/Supabase, sem reenviar o banco inteiro.
