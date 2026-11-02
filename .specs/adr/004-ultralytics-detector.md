# ADR-004: 检测后端采用 Ultralytics 封装（可替换）

- **状态**: accepted
- **日期**: 2026-11-02
- **Change**: alarm-image-verify

## 背景

产品二次识别需要目标检测产出类别、置信度与可选框；用户技术偏好为 YOLO 系，但产品命名不绑定品牌。

## 决策

- 定义内部接口 `Detector.predict(image) -> list[Detection(label, confidence, xywh?)]`
- v1 默认实现：`UltralyticsDetector`（YOLO 权重可配置路径）
- 原告警 bbox 仅用于审核台对照展示；v1 默认对**全图**推理（框内裁剪策略留扩展点，不作为 v1 必选）

## 备选

- OpenCV DNN / ONNX Runtime 直接跑
- 云端检测 API

## 理由

Ultralytics 上手快、权重生态全；接口隔离保证可换 ONNX/其他实现而不改 API 契约。

## 后果

- 依赖 PyTorch/CUDA 环境，镜像体积大
- 须在配置中明确 `weights_path`、`conf_threshold`、`device`
- LICENSE/权重来源需部署时自行合规
