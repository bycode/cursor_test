from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    status: Mapped[str] = mapped_column(String(32), default="received", index=True)
    source: Mapped[str] = mapped_column(String(32), default="api")
    alarm_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    alarm_bboxes: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    detections: Mapped[list | None] = mapped_column(JSON, nullable=True)
    bbox_verdicts: Mapped[list | None] = mapped_column(JSON, nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
