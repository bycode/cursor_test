from __future__ import annotations

import asyncio
import logging
import shutil
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal
from app.detect.factory import get_detector
from app.models import Task
from app.services.verify import VerifyError, VerifyService
from app.tasks.repo import TaskRepository

logger = logging.getLogger(__name__)

IMAGE_SUFFIXES = settings.allowed_suffix_set


class DirectoryScanner:
    def __init__(self, inbox_dir: str | None = None) -> None:
        self.inbox = Path(inbox_dir or settings.inbox_dir)
        self.done_dir = self.inbox / "done"
        self.done_dir.mkdir(parents=True, exist_ok=True)

    def scan_once(self, db: Session | None = None) -> list[str]:
        owns_session = db is None
        session = db or SessionLocal()
        processed: list[str] = []
        try:
            service = VerifyService(session, get_detector())
            for image_path in sorted(self.inbox.iterdir()):
                if not image_path.is_file():
                    continue
                if image_path.suffix.lower() not in IMAGE_SUFFIXES:
                    continue
                json_path = image_path.with_suffix(".json")
                if not json_path.exists():
                    logger.info("skip unpaired image: %s", image_path.name)
                    repo = TaskRepository(session)
                    skip = Task(
                        id=f"skip-{image_path.stem}-{image_path.stat().st_mtime_ns}",
                        status="skipped",
                        source="directory",
                        error=f"missing sidecar {json_path.name}",
                    )
                    existing = repo.get(skip.id)
                    if existing is None:
                        repo.create(skip)
                    continue

                image_bytes = image_path.read_bytes()
                bbox_raw = json_path.read_text(encoding="utf-8")
                try:
                    result = service.run(
                        image_bytes=image_bytes,
                        filename=image_path.name,
                        bbox_raw=bbox_raw,
                        source="directory",
                    )
                    processed.append(result["task_id"])
                    self._archive(image_path, json_path)
                except VerifyError as exc:
                    logger.warning("directory verify failed for %s: %s", image_path.name, exc.message)
        finally:
            if owns_session:
                session.close()
        return processed

    def _archive(self, image_path: Path, json_path: Path) -> None:
        self.done_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(image_path), self.done_dir / image_path.name)
        shutil.move(str(json_path), self.done_dir / json_path.name)


async def scanner_loop(stop_event: asyncio.Event) -> None:
    scanner = DirectoryScanner()
    while not stop_event.is_set():
        try:
            await asyncio.to_thread(scanner.scan_once)
        except Exception:  # noqa: BLE001
            logger.exception("directory scanner iteration failed")
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=settings.scan_interval_seconds)
        except TimeoutError:
            continue
