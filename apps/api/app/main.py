from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import tasks as tasks_api
from app.api import verify as verify_api
from app.config import settings
from app.ingest.scanner import scanner_loop

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.ensure_data_dirs()
    stop_event = asyncio.Event()
    task = asyncio.create_task(scanner_loop(stop_event))
    app.state.scanner_stop = stop_event
    app.state.scanner_task = task
    logger.info("directory scanner started; inbox=%s", settings.inbox_dir)
    try:
        yield
    finally:
        stop_event.set()
        await task


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(verify_api.router)
app.include_router(tasks_api.router)


@app.get("/healthz")
def healthz() -> dict[str, object]:
    return {
        "status": "ok",
        "model_ready": settings.detector_backend == "stub" or Path(settings.weights_path).exists(),
        "detector_backend": settings.detector_backend,
    }


_web_dist = Path(__file__).resolve().parents[2] / "web" / "dist"
if settings.serve_web and _web_dist.is_dir():
    app.mount("/", StaticFiles(directory=str(_web_dist), html=True), name="web")
