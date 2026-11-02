import type { TaskDetail, TaskSummary } from "./types";

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(path);
  if (!res.ok) {
    throw new Error(`request failed: ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function fetchTasks(): Promise<{ items: TaskSummary[]; total: number }> {
  return getJson("/api/v1/tasks");
}

export async function fetchTask(taskId: string): Promise<TaskDetail> {
  return getJson(`/api/v1/tasks/${taskId}`);
}
