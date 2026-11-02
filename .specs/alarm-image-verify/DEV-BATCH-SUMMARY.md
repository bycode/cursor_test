# SUMMARY: T02–T19 连续开发批次

- **Change ID**: alarm-image-verify
- **完成时间**: 2026-11-02
- **AI 角色**: Dev

---

## 做了什么

在用户授权「连续推进、无需逐步确认」下完成 Wave 1–10：

- **API**：配置、SQLite+Alembic、`Detector`/`Stub`/`Ultralytics` 工厂、`VerifyService`、同步 `/api/v1/verify`、任务查询与原图、目录 sidecar 扫描、AC 目录流测试
- **Web**：tokens、壳层、列表/详情、双层 bbox、API client + 代理
- **交付**：README、Dockerfiles、`docker-compose.yml`、静态挂载检查脚本
- **依赖**：`ultralytics` 改为 optional extra `[detect]`，默认 stub 可跑通

## verify

```text
apps/web: npm run build → success
apps/api: python -m pytest -q → 10 passed
apps/api: python scripts/check_static.py → static_check_ok
docker compose config → 本机未安装 docker；已用文件内容断言 compose_file_ok
```

## GitNexus

不可用；未做符号级影响检查。

## 越界 / 说明

- `data/**/.gitkeep`、测试 fixtures 路径、`apps/api/scripts/`、`docker-compose.yml` 等为交付必需，部分略宽于单任务 write_files，属于连续批次合并交付。
- 未自动 git commit（用户未要求）。

## 本地启动

见根 `README.md`。默认 `DETECTOR_BACKEND=stub`。真实 YOLO：`pip install -e ".[detect]"` 并配置权重。
