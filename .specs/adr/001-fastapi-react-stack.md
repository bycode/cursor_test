# ADR-001: 采用 FastAPI + React 技术栈

- **状态**: accepted
- **日期**: 2026-11-02
- **Change**: alarm-image-verify

## 背景

平台需要同步 HTTP 入图、目录扫描、目标检测推理，以及工业风只读审核台。

## 决策

采用 **FastAPI（Python 3.11+）+ Vite/React/TypeScript** 前后端分离；推理与 API 同属 Python 进程域。

## 备选

- Node/Nest 主 API + Python 推理旁路
- Go 主 API + Python 推理旁路
- Next.js 全栈

## 理由

二次识别依赖 Python 视觉生态；同步路径下同进程调用可减少 IPC 与序列化开销，利于 P95&lt;5s 软目标。

## 后果

- 前端需独立构建，由 FastAPI 挂载 `static` 或反向代理
- 团队需同时维护 Python 与 TypeScript
- 变栈须开新 CHANGE
