import type { BBoxVerdict } from "../api/types";

const LABEL: Record<string, string> = {
  false_alarm: "误报（驾驶室豁免）",
  confirm: "保留告警",
  uncertain: "不确定",
};

type Props = {
  verdicts: BBoxVerdict[];
};

export function VerdictTable({ verdicts }: Props) {
  if (!verdicts.length) {
    return <p className="task-list__empty">无逐框判定结果</p>;
  }
  return (
    <table className="detection-table">
      <thead>
        <tr>
          <th>#</th>
          <th>判定</th>
          <th>原因</th>
        </tr>
      </thead>
      <tbody>
        {verdicts.map((v) => (
          <tr key={v.index}>
            <td>{v.index}</td>
            <td data-verdict={v.verdict}>{LABEL[v.verdict] ?? v.verdict}</td>
            <td>{v.reason}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
