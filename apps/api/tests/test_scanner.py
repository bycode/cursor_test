import json

from app.detect.stub import StubDetector
from app.ingest.scanner import DirectoryScanner
from app.services.verify import VerifyService
from app.tasks.repo import TaskRepository


def test_scanner_pair_and_skip(db_session, sample_image, tmp_path, monkeypatch):
    from app.config import settings

    inbox = tmp_path / "inbox"
    monkeypatch.setattr(settings, "inbox_dir", str(inbox))
    monkeypatch.setattr(settings, "images_dir", str(tmp_path / "images"))
    settings.ensure_data_dirs()

    img = inbox / "foo.jpg"
    img.write_bytes(sample_image.read_bytes())
    (inbox / "foo.json").write_text(
        json.dumps({"bboxes": [{"x": 0, "y": 0, "w": 5, "h": 5}]}),
        encoding="utf-8",
    )
    lonely = inbox / "bar.jpg"
    lonely.write_bytes(sample_image.read_bytes())

    scanner = DirectoryScanner(str(inbox))
    # inject via service path using same db
    processed = scanner.scan_once(db_session)
    assert len(processed) == 1
    assert not img.exists()
    assert lonely.exists()
    repo = TaskRepository(db_session)
    items, total = repo.list_tasks(limit=100)
    statuses = {t.status for t in items}
    assert "succeeded" in statuses
    assert "skipped" in statuses
