from app.models import Task
from app.tasks.repo import TaskRepository


def test_repo_create_get_list(db_session):
    repo = TaskRepository(db_session)
    task = Task(id="t1", status="succeeded", source="api", detections=[{"label": "a", "confidence": 0.9}])
    repo.create(task)
    assert repo.get("t1") is not None
    items, total = repo.list_tasks()
    assert total == 1
    assert items[0].id == "t1"
