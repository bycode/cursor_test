"""Verify API app loads and optional static web mount wiring."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    web_dist = Path(__file__).resolve().parents[2] / "web" / "dist"
    serve = os.environ.get("SERVE_WEB", "").lower() in {"1", "true", "yes"}
    print(f"web_dist_exists={web_dist.is_dir()}")
    print(f"serve_web_env={serve}")
    os.environ.setdefault("DETECTOR_BACKEND", "stub")
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as client:
        assert client.get("/healthz").status_code == 200
        paths = client.get("/openapi.json").json()["paths"]
        assert "/api/v1/verify" in paths
        assert "/api/v1/tasks" in paths
    print("static_check_ok")


if __name__ == "__main__":
    main()
