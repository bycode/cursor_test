from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Task


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def save(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get(self, task_id: str) -> Task | None:
        return self.db.get(Task, task_id)

    def list_tasks(self, *, limit: int = 50, offset: int = 0) -> tuple[list[Task], int]:
        total = self.db.scalar(select(func.count()).select_from(Task)) or 0
        rows = self.db.scalars(
            select(Task).order_by(Task.created_at.desc()).limit(limit).offset(offset)
        ).all()
        return list(rows), int(total)
