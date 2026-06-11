from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4
import json
from typing import Any

from sqlalchemy import func, select

from app.database import get_db
from app.models import SyncRecord
from app.schemas import SyncPushRequest, SyncPushResponse, SyncPullResponse, SyncStatusResponse


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_newer(received: str, stored: str | None) -> bool:
    if not stored:
        return True
    try:
        return datetime.fromisoformat(received) > datetime.fromisoformat(stored)
    except Exception:
        return received > stored


def push_sync(payload: SyncPushRequest) -> SyncPushResponse:
    created = updated = ignored = 0
    with get_db() as db:
        for record in payload.records:
            existing = db.execute(select(SyncRecord).where(SyncRecord.uuid == record.uuid)).scalar_one_or_none()
            payload_json = json.dumps(record.payload, ensure_ascii=False)
            if existing is None:
                db.add(SyncRecord(
                    uuid=record.uuid or str(uuid4()),
                    user_id=payload.user_id,
                    entity_type=record.entity_type,
                    payload_json=payload_json,
                    created_at=record.created_at,
                    updated_at=record.updated_at,
                    deleted_at=record.deleted_at,
                    device_id=payload.device_id,
                    sync_version=1,
                ))
                created += 1
                continue
            if not _is_newer(record.updated_at, existing.updated_at):
                ignored += 1
                continue
            existing.user_id = payload.user_id
            existing.entity_type = record.entity_type
            existing.payload_json = payload_json
            existing.created_at = record.created_at or existing.created_at
            existing.updated_at = record.updated_at
            existing.deleted_at = record.deleted_at
            existing.device_id = payload.device_id
            existing.sync_version = (existing.sync_version or 1) + 1
            updated += 1
    return SyncPushResponse(received=len(payload.records), created=created, updated=updated, ignored=ignored)


def pull_sync(user_id: str, since: str | None = None) -> SyncPullResponse:
    with get_db() as db:
        query = select(SyncRecord).where(SyncRecord.user_id == user_id)
        if since:
            query = query.where(SyncRecord.updated_at > since)
        rows = db.execute(query.order_by(SyncRecord.updated_at.asc())).scalars().all()
        records = [
            {
                'uuid': row.uuid,
                'entity_type': row.entity_type,
                'payload': json.loads(row.payload_json),
                'created_at': row.created_at,
                'updated_at': row.updated_at,
                'deleted_at': row.deleted_at,
                'device_id': row.device_id,
                'sync_version': row.sync_version,
            }
            for row in rows
        ]
    return SyncPullResponse(server_time=_now_iso(), records=records)


def sync_status() -> SyncStatusResponse:
    with get_db() as db:
        total = db.execute(select(func.count()).select_from(SyncRecord)).scalar_one()
        last_update = db.execute(select(func.max(SyncRecord.updated_at))).scalar_one()
    return SyncStatusResponse(records=int(total or 0), last_update=last_update)
