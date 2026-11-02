# CHANGE: 驾驶室豁免误报判定

- **Change ID**: cabin-false-alarm
- **创建日期**: 2026-11-02
- **路径建议**: 最短（基于已有平台增量）
- **状态**: active
- **依赖**: `@.specs/alarm-image-verify/`

---

## Why

上游「未戴安全帽」告警在驾驶室内属合规，造成误报。需要二次校验按情境豁免。

## What

对上游每个未戴帽 bbox：单独检测 `cabin`；若框中心落入任一驾驶室框 → 判 `false_alarm`；未落入 → `confirm`；未检出驾驶室 → `uncertain`。结果落库并在审核台展示。

## 影响面

- [x] REQUIREMENT / DESIGN 增量
- [x] VerifyService 判定逻辑
- [x] API 响应与任务详情
- [x] 审核台展示逐框结论

## 范围排除

- 先检 vehicle 再判室内
- 人工改判
- 回写上游 Webhook（仍不强制；响应可供上游拉取）

## 验收线

- 中心在 cabin 内的上游框 → false_alarm
- 中心在 cabin 外 → confirm
- 无 cabin → uncertain
