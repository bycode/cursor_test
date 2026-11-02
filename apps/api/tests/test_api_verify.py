import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app


def test_api_verify_and_errors(tmp_path, sample_image, monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "images_dir", str(tmp_path / "images"))
    monkeypatch.setattr(settings, "inbox_dir", str(tmp_path / "inbox"))
    monkeypatch.setattr(settings, "detector_backend", "stub")
    settings.ensure_data_dirs()

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    def override_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db
    try:
        with TestClient(app) as client:
            bbox = json.dumps({"bboxes": [{"x": 0, "y": 0, "w": 10, "h": 10}], "alarm_id": "a1"})
            files = {"file": ("sample.jpg", sample_image.read_bytes(), "image/jpeg")}
            data = {"bbox": bbox}
            ok = client.post("/api/v1/verify", files=files, data=data)
            assert ok.status_code == 200, ok.text
            body = ok.json()
            assert body["detections"][0]["label"] == "cabin"
            assert body["bbox_verdicts"][0]["verdict"] in {"false_alarm", "confirm", "uncertain"}
            assert "task_id" in body

            bad = client.post(
                "/api/v1/verify",
                files={"file": ("sample.jpg", sample_image.read_bytes(), "image/jpeg")},
                data={"bbox": "{"},
            )
            assert bad.status_code == 400

            missing = client.post("/api/v1/verify", data={"bbox": bbox})
            assert missing.status_code == 422
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
