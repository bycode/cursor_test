from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models import Task


def test_list_and_detail(tmp_path, sample_image, monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "images_dir", str(tmp_path / "images"))
    monkeypatch.setattr(settings, "inbox_dir", str(tmp_path / "inbox"))
    settings.ensure_data_dirs()
    image_path = tmp_path / "images" / "t1" / "origin.jpg"
    image_path.parent.mkdir(parents=True)
    image_path.write_bytes(sample_image.read_bytes())

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    db = TestingSession()
    db.add(
        Task(
            id="t1",
            status="succeeded",
            source="api",
            alarm_bboxes=[{"x": 1, "y": 2, "w": 3, "h": 4}],
            detections=[{"label": "x", "confidence": 0.5}],
            image_path=str(image_path),
        )
    )
    db.commit()
    db.close()

    def override_db():
        session = TestingSession()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_db
    try:
        with TestClient(app) as client:
            listed = client.get("/api/v1/tasks")
            assert listed.status_code == 200
            assert listed.json()["total"] == 1
            detail = client.get("/api/v1/tasks/t1")
            assert detail.status_code == 200
            assert detail.json()["detections"][0]["label"] == "x"
            assert "改判" not in detail.text
            img = client.get("/api/v1/tasks/t1/image")
            assert img.status_code == 200
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
