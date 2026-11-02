from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.config import settings
from app.detect.base import Detector
from app.ingest.bbox import BBoxParseError, parse_bbox_payload
from app.models import Task
from app.services.cabin_rule import judge_alarm_bboxes
from app.tasks.repo import TaskRepository


class VerifyError(Exception):
    def __init__(self, message: str, *, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class VerifyService:
    def __init__(self, db: Session, detector: Detector) -> None:
        self.repo = TaskRepository(db)
        self.detector = detector
        settings.ensure_data_dirs()

    def run(
        self,
        *,
        image_bytes: bytes,
        filename: str,
        bbox_raw: str | bytes,
        source: str = "api",
    ) -> dict[str, Any]:
        suffix = Path(filename).suffix.lower()
        if suffix not in settings.allowed_suffix_set:
            raise VerifyError(f"unsupported image type: {suffix or '(none)'}")
        if len(image_bytes) == 0:
            raise VerifyError("empty image")
        if len(image_bytes) > settings.max_upload_bytes:
            raise VerifyError("image exceeds max_upload_bytes")

        try:
            bbox_data = parse_bbox_payload(bbox_raw)
        except BBoxParseError as exc:
            raise VerifyError(str(exc)) from exc

        task_id = uuid.uuid4().hex
        task_dir = Path(settings.images_dir) / task_id
        task_dir.mkdir(parents=True, exist_ok=True)
        image_path = task_dir / f"origin{suffix}"
        image_path.write_bytes(image_bytes)

        alarm_bboxes = bbox_data.get("bboxes") or []
        task = Task(
            id=task_id,
            status="received",
            source=source,
            alarm_id=bbox_data.get("alarm_id"),
            alarm_bboxes=alarm_bboxes,
            image_path=str(image_path),
        )
        self.repo.create(task)

        try:
            detections = self.detector.predict(image_path)
            payload = [d.to_dict() for d in detections]
            cabin_boxes = [
                d
                for d in payload
                if str(d.get("label", "")).lower() == "cabin"
                and d.get("x") is not None
                and d.get("y") is not None
                and d.get("w") is not None
                and d.get("h") is not None
            ]
            verdicts = judge_alarm_bboxes(alarm_bboxes, cabin_boxes)
            task.status = "succeeded"
            task.detections = payload
            task.bbox_verdicts = verdicts
            self.repo.save(task)
        except Exception as exc:  # noqa: BLE001 — persist failure for audit log
            task.status = "failed"
            task.error = str(exc)
            self.repo.save(task)
            raise VerifyError(f"detection failed: {exc}", status_code=500) from exc

        return {
            "task_id": task_id,
            "status": task.status,
            "detections": payload,
            "cabin_bboxes": cabin_boxes,
            "alarm_bboxes": task.alarm_bboxes,
            "bbox_verdicts": verdicts,
            "alarm_id": task.alarm_id,
        }
