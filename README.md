# 报警二次校验平台

对上游告警图片做二次识别（类别 + 置信度），支持同步 WebAPI 与目录 sidecar 投递；提供只读审核日志台。

## 结构

- `apps/api` — FastAPI（入图 / 扫描 / 任务查询）
- `apps/web` — Vite + React 审核台（工业风）
- `.specs/alarm-image-verify/` — 需求与设计

## Python 环境

**请用仓库根目录 `.venv`**，不要往 conda `base` 装本项目依赖。详见 `ENV.md`。  
Label Studio 用已有 conda env：`conda activate label-studio`。

驾驶室训练工具：`tools/cabin-train/README.md`。

## 本地开发

### API

```bash
# 在仓库根
.\.venv\Scripts\Activate.ps1
python -m pip install -e "apps/api[dev]"
cd apps/api
# 默认 stub 检测，无需 YOLO 权重
alembic upgrade head
uvicorn app.main:app --reload --app-dir .
```

健康检查：`GET http://127.0.0.1:8000/healthz`

同步校验示例：

```bash
curl -F "file=@sample.jpg" -F "bbox={\"bboxes\":[{\"x\":0,\"y\":0,\"w\":10,\"h\":10}]}" http://127.0.0.1:8000/api/v1/verify
```

目录投递：将 `foo.jpg` + `foo.json` 放入 `data/inbox/`（默认每 ≤10s 扫描），成功后移到 `data/inbox/done/`。

换真实检测：设置 `DETECTOR_BACKEND=ultralytics` 与 `WEIGHTS_PATH=...`（需安装 ultralytics）。

### Web

```bash
cd apps/web
npm install
npm run dev
```

开发服务器将 `/api` 代理到 `8000`。

同端口静态托管（可选）：先 `npm run build`，再以 `SERVE_WEB=true` 启动 API。

## Docker

```bash
docker compose up --build
```

- API: `http://localhost:8000`
- Web: `http://localhost:5173`

## 测试

```bash
cd apps/api
python -m pytest -q
```
