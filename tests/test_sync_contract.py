from __future__ import annotations

from datetime import datetime, timezone, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def _record(uuid_value: str, entity_type: str = 'entradas', value: int = 1, updated_at: str | None = None, deleted_at: str | None = None) -> dict:
    ts = updated_at or datetime.now(timezone.utc).isoformat()
    return {
        'uuid': uuid_value,
        'entity_type': entity_type,
        'payload': {'valor': value},
        'created_at': ts,
        'updated_at': ts,
        'deleted_at': deleted_at,
    }


def test_push_and_pull_roundtrip() -> None:
    user_id = f'user-{uuid4().hex[:8]}'
    device_id = 'desktop-001'
    uuid_value = str(uuid4())
    payload = {'user_id': user_id, 'device_id': device_id, 'records': [_record(uuid_value, value=10)]}
    response = client.post('/sync/push', json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body['received'] == 1
    assert body['created'] == 1

    pull = client.get('/sync/pull', params={'user_id': user_id})
    assert pull.status_code == 200
    data = pull.json()
    assert data['status'] == 'ok'
    assert len(data['records']) == 1
    assert data['records'][0]['uuid'] == uuid_value


def test_update_same_uuid_and_ignore_old_version() -> None:
    user_id = f'user-{uuid4().hex[:8]}'
    device_id = 'desktop-001'
    uuid_value = str(uuid4())
    base_time = datetime.now(timezone.utc)
    first = _record(uuid_value, value=10, updated_at=base_time.isoformat())
    second = _record(uuid_value, value=20, updated_at=(base_time + timedelta(minutes=5)).isoformat())
    old = _record(uuid_value, value=5, updated_at=(base_time - timedelta(minutes=5)).isoformat())

    r1 = client.post('/sync/push', json={'user_id': user_id, 'device_id': device_id, 'records': [first]})
    assert r1.json()['created'] == 1
    r2 = client.post('/sync/push', json={'user_id': user_id, 'device_id': device_id, 'records': [second]})
    assert r2.json()['updated'] == 1
    r3 = client.post('/sync/push', json={'user_id': user_id, 'device_id': device_id, 'records': [old]})
    assert r3.json()['ignored'] == 1

    pull = client.get('/sync/pull', params={'user_id': user_id})
    record = pull.json()['records'][0]
    assert record['payload']['valor'] == 20


def test_deleted_at_and_since_filter() -> None:
    user_id = f'user-{uuid4().hex[:8]}'
    device_id = 'desktop-001'
    uuid_value = str(uuid4())
    first = _record(uuid_value, value=10, updated_at=datetime.now(timezone.utc).isoformat())
    deleted = _record(uuid_value, value=10, updated_at=(datetime.now(timezone.utc) + timedelta(minutes=1)).isoformat(), deleted_at=datetime.now(timezone.utc).isoformat())
    client.post('/sync/push', json={'user_id': user_id, 'device_id': device_id, 'records': [first]})
    client.post('/sync/push', json={'user_id': user_id, 'device_id': device_id, 'records': [deleted]})

    status = client.get('/sync/status')
    assert status.status_code == 200
    assert status.json()['records'] >= 1

    since = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    empty_pull = client.get('/sync/pull', params={'user_id': user_id, 'since': since})
    assert empty_pull.status_code == 200
    assert empty_pull.json()['records'] == []

    pull = client.get('/sync/pull', params={'user_id': user_id})
    data = pull.json()['records'][0]
    assert data['deleted_at'] is not None
