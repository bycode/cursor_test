import type { TaskSummary } from "../api/types";
import { TaskRow } from "./TaskRow";

type Props = {
  tasks: TaskSummary[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  onRefresh: () => void;
  loading: boolean;
};

export function TaskList({ tasks, selectedId, onSelect, onRefresh, loading }: Props) {
  return (
    <div className="task-list">
      <div className="task-list__toolbar">
        <span className="task-list__label">任务列表</span>
        <button type="button" className="btn btn--ghost" onClick={onRefresh} disabled={loading}>
          刷新列表
        </button>
      </div>
      {tasks.length === 0 ? (
        <p className="task-list__empty">等待 API 或目录投递任务</p>
      ) : (
        tasks.map((task) => (
          <TaskRow
            key={task.task_id}
            task={task}
            selected={task.task_id === selectedId}
            onSelect={onSelect}
          />
        ))
      )}
    </div>
  );
}
