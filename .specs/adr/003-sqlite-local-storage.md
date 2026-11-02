# ADR-003: SQLite 元数据 + 本地文件系统存图

- **状态**: accepted
- **日期**: 2026-11-02
- **Change**: alarm-image-verify

## 背景

需持久化校验任务与识别结果，并保存原图供审核台查看；v1 单实例、受信网络。

## 决策

- 元数据：SQLAlchemy 2 + **SQLite**（文件库）
- 原图与派生物：本地目录（如 `data/images/{task_id}/...`）
- 迁移：Alembic（即使 SQLite 也保持可逆迁移习惯）

## 备选

- Postgres + 对象存储
- 仅文件系统 JSONL

## 理由

单机闭环成本最低，满足列表/详情查询；与「不做多租户」一致。结构化查询仍用 SQL，避免纯文件难筛。

## 后果

- 多实例横向扩展需迁移到 Postgres/共享存储（未来 CHANGE）
- 备份需同时拷贝 DB 文件与 `data/images`
- 写入并发有限，配合同步推理的低并发假设
