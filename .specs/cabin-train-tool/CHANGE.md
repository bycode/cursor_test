# CHANGE: 驾驶室 YOLO 训练工具 + Label Studio 接入

- **Change ID**: cabin-train-tool
- **创建日期**: 2026-11-02
- **路径建议**: 最短
- **状态**: active

---

## Why

平台需 `cabin` 检测权重；需要可复现的标注→训练→导出路径，且**不污染系统默认/conda base Python**。

## What

- `tools/cabin-train`：数据集约定、Ultralytics 训练/评估脚本、导出权重到 API 可用路径
- Label Studio：文档说明复用已有 conda env `label-studio`；提供导出 YOLO 格式指引与目录对齐
- 项目根 `.venv`：API + 训练依赖隔离安装

## 范围排除

- 不改用户 conda base / 其它 named env 的包（仅文档指引）
- 不做自研标注 UI（用 Label Studio）
- 不在本 change 内完成大规模真实数据采集
