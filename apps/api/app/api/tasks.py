from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.tasks.repo import TaskRepository

router = APIRouter(prefix="/api/v1", tags=["tasks"])


def _task_summary(task) -> dict:
    return {
        "task_id": task.id,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "status": task.status,
        "source": task.source,
    }


@router.get("/tasks")
def list_tasks(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> dict:
    items, total = TaskRepository(db).list_tasks(limit=limit, offset=offset)
    return {"items": [_task_summary(t) for t in items], "total": total}


@router.get("/tasks/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db)) -> dict:
    task = TaskRepository(db).get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return {
        **_task_summary(task),
        "alarm_id": task.alarm_id,
        "alarm_bboxes": task.alarm_bboxes or [],
        "detections": task.detections or [],
        "cabin_bboxes": [
            d
            for d in (task.detections or [])
            if str(d.get("label", "")).lower() == "cabin"
        ],
        "bbox_verdicts": task.bbox_verdicts or [],
        "image_url": f"/api/v1/tasks/{task.id}/image",
        "error": task.error,
    }


@router.get("/tasks/{task_id}/image")
def get_task_image(task_id: str, db: Session = Depends(get_db)) -> FileResponse:
    task = TaskRepository(db).get(task_id)
    if task is None or not task.image_path:
        raise HTTPException(status_code=404, detail="image not found")
    path = Path(task.image_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="image file missing")
    return FileResponse(path)
