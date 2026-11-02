# API — 报警二次校验

FastAPI 服务：同步入图、目录 sidecar 扫描、任务查询。

```bash
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

- `GET /healthz` — 存活探针（模型就绪字段后续任务完善）
