# CONTEXT — 项目域语言与默认决策

> 跨 change 共享。追加更新，勿删历史决策（过时则标 `deprecated`）。

---

## 术语表

| 术语 | 定义 |
|------|------|
| 二次识别 | 对上游已报警的图片再次做目标检测，产出类别与置信度，用于降误报参考 |
| 报警 bbox | 上游一次检测给出的框信息，随图传入，供对照展示；不作为二次识别的唯一输入约束（全图/框内策略见 DESIGN） |
| sidecar | 与图片同主文件名的 JSON 文件，例如 `foo.jpg` + `foo.json` |
| 校验任务 | 一次入图（API 或目录）对应的处理单元，含状态与识别结果 |
| 审核日志台 | 只读 Web 界面，用于查看任务列表与详情；不介入判定 |
| 类别+置信度 | 二次识别的标准产出：`label` + `confidence`（0~1） |

## 已锁决策

| ID | 决策 | 来源 |
|----|------|------|
| D-001 | 产品/Change 命名不绑定具体检测模型品牌 | CHANGE |
| D-002 | 人工侧只做日志复核，不改判、不覆盖模型输出 | CHANGE |
| D-003 | v1 不回写 / 不回调上游告警程序 | CHANGE |
| D-004 | 入图 API 为同步：响应内直接带识别结果 | REQUIREMENT |
| D-005 | 目录入图采用同名 sidecar：`image` + `同名.json` | REQUIREMENT |
| D-006 | 审核台 v1 = 列表 + 详情，不做筛选大盘 | REQUIREMENT |
| D-007 | 视觉调性：3 工业（Industrial） | CHANGE |
| D-008 | 不做：多租户、复杂权限、大盘统计、移动端 | CHANGE |
| D-009 | 技术栈：FastAPI + Vite/React/TS | DESIGN |
| D-010 | v1 同步内联推理，无消息队列 | DESIGN / ADR-002 |
| D-011 | SQLite + 本地磁盘存图 | DESIGN / ADR-003 |
| D-012 | Detector 接口 + Ultralytics 默认实现；v1 全图推理 | DESIGN / ADR-004 |
| D-013 | 未戴帽误报：单独检 cabin；框中心落入 cabin → false_alarm | cabin-false-alarm |
| D-014 | 无 cabin → uncertain；中心不在 cabin → confirm（保留告警） | cabin-false-alarm |
| D-015 | 项目依赖只装进仓库 `.venv`；Label Studio 用 conda env `label-studio`；禁止污染 base | cabin-train-tool |

## 默认行为（给 AI 的可信默认）

- **bbox JSON v1 schema**（单文件可含多框）:

```json
{
  "alarm_id": "optional-string",
  "bboxes": [
    {
      "x": 0,
      "y": 0,
      "w": 100,
      "h": 80,
      "label": "optional-upstream-label",
      "confidence": 0.93
    }
  ]
}
```

- 坐标：相对原图像素的 `xywh`（左上角 x/y + 宽高），整数或浮点均可。
- 支持图片后缀（目录与上传）：`.jpg` / `.jpeg` / `.png` / `.bmp` / `.webp`。
- 目录扫描：成对出现才进入识别；仅图无 json → 跳过，不记成功。
- 同步 API 出错：4xx + 可读错误信息；不落「成功」任务。
- 识别响应至少包含：`task_id`、`detections[]`（`label`、`confidence`，若有框则含 `x,y,w,h`）。

## 偏好

- 工件与说明文档：中文
- 代码标识符：英文
- 空仓首建：优先简单可跑通闭环，避免过早引入消息队列（除非 DESIGN 论证必要）
