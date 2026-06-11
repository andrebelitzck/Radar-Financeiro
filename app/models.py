from __future__ import annotations

from sqlalchemy import Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SyncRecord(Base):
    __tablename__ = 'sync_records'
    __table_args__ = (
        Index('idx_sync_user_updated_at', 'user_id', 'updated_at'),
        Index('idx_sync_user_entity', 'user_id', 'entity_type'),
        Index('idx_sync_uuid', 'uuid', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(String(32), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(32), nullable=False)
    deleted_at: Mapped[str | None] = mapped_column(String(32), nullable=True)
    device_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    sync_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
