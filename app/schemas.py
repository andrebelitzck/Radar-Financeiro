from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

EntityType = Literal['entradas', 'saidas', 'bancos', 'categorias', 'parcelamentos', 'parcelas', 'previsoes', 'dividas', 'chaves_pix', 'cartoes', 'investimentos']


class SyncRecordPayload(BaseModel):
    uuid: str
    entity_type: EntityType
    payload: dict[str, Any]
    created_at: str
    updated_at: str
    deleted_at: str | None = None


class SyncPushRequest(BaseModel):
    user_id: str = Field(min_length=1)
    device_id: str = Field(min_length=1)
    records: list[SyncRecordPayload] = Field(default_factory=list)


class SyncPushResponse(BaseModel):
    status: str = 'ok'
    received: int = 0
    created: int = 0
    updated: int = 0
    ignored: int = 0


class SyncPullResponse(BaseModel):
    status: str = 'ok'
    server_time: str
    records: list[dict[str, Any]]


class SyncStatusResponse(BaseModel):
    records: int
    last_update: str | None


class HealthResponse(BaseModel):
    status: str = 'ok'
    service: str = 'Radar Financeiro Backend'
