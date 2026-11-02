import type { TaskSummary } from "../api/types";

type Props = {
  task: TaskSummary;
  selected: boolean;
  onSelect: (id: string) => void;
};

export function TaskRow({ task, selected, onSelect }: Props) {
  return (
    <button
      type="button"
      className={`task-row${selected ? " is-selected" : ""}`}
      onClick={() => onSelect(task.task_id)}
    >
      <span className="task-row__id">{task.task_id.slice(0, 12)}</span>
      <span className="task-row__meta">
        <span>{task.created_at ? new Date(task.created_at).toLocaleString() : "—"}</span>
        <span className="task-row__status" data-status={task.status}>
          {task.status}
        </span>
      </span>
    </button>
  );
}
