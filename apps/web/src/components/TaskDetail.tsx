import type { TaskDetail as TaskDetailType } from "../api/types";
import { ImageStage } from "./ImageStage";
import { VerdictTable } from "./VerdictTable";

type Props = {
  task: TaskDetailType | null;
};

export function TaskDetail({ task }: Props) {
  if (!task) {
    return <p className="task-list__empty">选择左侧任务查看详情</p>;
  }
  const cabins = task.cabin_bboxes?.length
    ? task.cabin_bboxes
    : (task.detections || []).filter((d) => d.label?.toLowerCase() === "cabin");
  return (
    <div className="task-detail">
      <div className="task-detail__head">
        <h2 className="task-detail__title">任务详情</h2>
        <span className="task-detail__id">{task.task_id}</span>
      </div>
      <ImageStage
        imageUrl={task.image_url}
        alarmBoxes={task.alarm_bboxes || []}
        cabinBoxes={cabins}
      />
      <div>
        <div className="task-list__label" style={{ marginBottom: "8px" }}>
          逐框判定
        </div>
        <VerdictTable verdicts={task.bbox_verdicts || []} />
      </div>
    </div>
  );
}
