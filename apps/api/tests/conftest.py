import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure stub detector and isolated sqlite for tests before app imports settings-heavy modules.
os.environ["DETECTOR_BACKEND"] = "stub"
os.environ["DATABASE_URL"] = "sqlite://"


@pytest.fixture()
def db_session(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from app.config import settings
    from app.db import Base

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
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def sample_image(tmp_path: Path) -> Path:
    from PIL import Image

    path = tmp_path / "sample.jpg"
    Image.new("RGB", (120, 80), color=(30, 40, 50)).save(path)
    return path
