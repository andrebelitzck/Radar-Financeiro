from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException, status

from app.config import ALLOW_TEST_AUTH


@dataclass(frozen=True)
class AuthContext:
    user_id: str
    device_id: str | None = None


def allow_test_auth() -> bool:
    return bool(ALLOW_TEST_AUTH)


def build_future_jwt_payload(user_id: str, device_id: str | None = None) -> dict[str, Any]:
    return {
        'sub': user_id,
        'device_id': device_id,
        'mode': 'test' if allow_test_auth() else 'future-jwt',
    }


def require_future_auth(user_id: str | None) -> AuthContext:
    if allow_test_auth():
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user_id é obrigatório neste modo de teste.')
        return AuthContext(user_id=user_id)
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail='Autenticação real ainda não implementada neste backend.',
    )