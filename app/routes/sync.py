from __future__ import annotations

from fastapi import APIRouter, Query

from app.schemas import SyncPushRequest, SyncPushResponse, SyncPullResponse, SyncStatusResponse
from app.sync import push_sync, pull_sync, sync_status

router = APIRouter(prefix='/sync', tags=['sync'])


@router.post('/push', response_model=SyncPushResponse)
def push(payload: SyncPushRequest) -> SyncPushResponse:
    return push_sync(payload)


@router.get('/pull', response_model=SyncPullResponse)
def pull(user_id: str = Query(min_length=1), since: str | None = None) -> SyncPullResponse:
    return pull_sync(user_id=user_id, since=since)


@router.get('/status', response_model=SyncStatusResponse)
def status() -> SyncStatusResponse:
    return sync_status()
