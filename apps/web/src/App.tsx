import { useCallback, useEffect, useState } from "react";
import { fetchTask, fetchTasks } from "./api/client";
import type { TaskDetail as TaskDetailType, TaskSummary } from "./api/types";
import { Shell } from "./components/Shell";
import { TaskDetail } from "./components/TaskDetail";
import { TaskList } from "./components/TaskList";

export default function App() {
  const [tasks, setTasks] = useState<TaskSummary[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<TaskDetailType | null>(null);
  const [loading, setLoading] = useState(false);
  const [ready, setReady] = useState(false);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchTasks();
      setTasks(data.items);
      setReady(true);
      setSelectedId((prev) => prev ?? data.items[0]?.task_id ?? null);
    } catch {
      setReady(false);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  useEffect(() => {
    if (!selectedId) {
      setDetail(null);
      return;
    }
    let cancelled = false;
    void fetchTask(selectedId)
      .then((d) => {
        if (!cancelled) setDetail(d);
      })
      .catch(() => {
        if (!cancelled) setDetail(null);
      });
    return () => {
      cancelled = true;
    };
  }, [selectedId]);

  return (
    <Shell
      ready={ready}
      aside={
        <TaskList
          tasks={tasks}
          selectedId={selectedId}
          onSelect={setSelectedId}
          onRefresh={() => void refresh()}
          loading={loading}
        />
      }
      main={<TaskDetail task={detail} />}
    />
  );
}
