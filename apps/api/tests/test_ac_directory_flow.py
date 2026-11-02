import json

from app.ingest.scanner import DirectoryScanner
from app.tasks.repo import TaskRepository


def test_ac_directory_flow(db_session, sample_image, tmp_path, monkeypatch):
    from app.config import settings

    inbox = tmp_path / "inbox"
    monkeypatch.setattr(settings, "inbox_dir", str(inbox))
    monkeypatch.setattr(settings, "images_dir", str(tmp_path / "images"))
    monkeypatch.setattr(settings, "detector_backend", "stub")
    settings.ensure_data_dirs()

    pair = inbox / "alarm1.jpg"
    pair.write_bytes(sample_image.read_bytes())
    (inbox / "alarm1.json").write_text(
        json.dumps({"alarm_id": "A-1", "bboxes": [{"x": 10, "y": 10, "w": 40, "h": 40, "label": "person"}]}),
        encoding="utf-8",
    )
    only = inbox / "orphan.jpg"
    only.write_bytes(sample_image.read_bytes())

    processed = DirectoryScanner(str(inbox)).scan_once(db_session)
    assert len(processed) == 1
    assert (inbox / "done" / "alarm1.jpg").exists()
    assert only.exists()

    items, _ = TaskRepository(db_session).list_tasks(limit=20)
    by_status = {}
    for t in items:
        by_status.setdefault(t.status, []).append(t)
    assert by_status["succeeded"][0].detections[0]["label"] == "cabin"
    assert by_status["succeeded"][0].bbox_verdicts[0]["verdict"] == "false_alarm"
    assert by_status["skipped"]
