import type { Detection } from "../api/types";

type Props = {
  detections: Detection[];
};

export function DetectionTable({ detections }: Props) {
  if (detections.length === 0) {
    return <p className="task-list__empty">无二次识别结果</p>;
  }
  return (
    <table className="detection-table">
      <thead>
        <tr>
          <th>类别</th>
          <th>置信度</th>
        </tr>
      </thead>
      <tbody>
        {detections.map((d, i) => (
          <tr key={`${d.label}-${i}`}>
            <td>{d.label}</td>
            <td>{d.confidence.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
