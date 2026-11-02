# TASK: 报警图片二次校验平台

- **Change ID**: alarm-image-verify
- **关联**: `@.specs/alarm-image-verify/REQUIREMENT.md`、`@.specs/alarm-image-verify/DESIGN.md`、`@.specs/alarm-image-verify/UI-DESIGN.md`

---

## 波次划分

```
Wave 1 (parallel): T01[P], T02[P]
Wave 2 (parallel): T03[P], T04[P], T05[P]     (depends: T01；T05 可读 T01)
Wave 3 (parallel): T06[P], T07[P]               (T06→T05；T07→T03,T04)
Wave 4:            T08                           (depends: T05, T07)
Wave 5 (parallel): T09[P], T10[P], T11[P]       (depends: T08；T10 可仅依赖 T07 但与 T09 同契约，挂 T08 后)
Wave 6 (parallel): T12[P], T13                   (T12→T02；T13→T12)
Wave 7 (parallel): T14[P], T15[P]               (depends: T13；联调契约读 T10)
Wave 8:            T16                           (depends: T10, T14, T15)
Wave 9 (parallel): T17[P], T18[P]               (T17→T09,T10,T11；T18→T01,T02)
Wave 10:           T19                           (depends: T16, T18)
```

> 同 wave = 可并行；跨 wave = 必须顺序执行。

---

## 任务清单

```xml
<task id="T01" parallel="true" status="done">
  <name>初始化 API 工程骨架与依赖锁定</name>
  <read_files>
    .specs/alarm-image-verify/DESIGN.md
    .specs/CONTEXT.md
  </read_files>
  <write_files>
    apps/api/pyproject.toml
    apps/api/README.md
    apps/api/app/__init__.py
    apps/api/app/main.py
    apps/api/app/config.py
    .gitignore
    README.md
  </write_files>
  <action>
    创建 FastAPI 应用包结构、pyproject/依赖（fastapi、uvicorn、sqlalchemy、alembic、pydantic-settings、pillow、ultralytics、httpx、pytest）、最小 /healthz 路由与配置入口；根 README 仅占位说明 monorepo。
  </action>
  <verify>
    cd apps/api &amp;&amp; python -c "from app.main import app; print(app.title)"
  </verify>
  <done>
    API 包可导入且存在健康检查路由定义（AC 基础设施）
  </done>
  <depends_on></depends_on>
</task>

<task id="T02" parallel="true" status="done">
  <name>初始化 Web（Vite React TS）工程</name>
  <read_files>
    .specs/alarm-image-verify/DESIGN.md
    .specs/alarm-image-verify/UI-DESIGN.md
  </read_files>
  <write_files>
    apps/web/package.json
    apps/web/tsconfig.json
    apps/web/vite.config.ts
    apps/web/index.html
    apps/web/src/main.tsx
    apps/web/src/App.tsx
    apps/web/src/vite-env.d.ts
  </write_files>
  <action>
    搭建 Vite + React 18 + TypeScript 工程，可 npm run build；App 仅占位标题「报警二次校验」。
  </action>
  <verify>
    cd apps/web &amp;&amp; npm install &amp;&amp; npm run build
  </verify>
  <done>
    Web 工程可成功生产构建
  </done>
  <depends_on></depends_on>
</task>

<task id="T03" parallel="true" status="done">
  <name>配置项：路径、扫描间隔、模型与上传限制</name>
  <read_files>
    apps/api/app/config.py
    .specs/CONTEXT.md
    .specs/alarm-image-verify/DESIGN.md
  </read_files>
  <write_files>
    apps/api/app/config.py
    apps/api/.env.example
  </write_files>
  <action>
    用 pydantic-settings 固化：数据库 URL、data/images、inbox 目录、扫描间隔、权重路径、device、conf_threshold、最大上传字节、允许后缀；提供 .env.example。
  </action>
  <verify>
    cd apps/api &amp;&amp; python -c "from app.config import settings; assert settings.scan_interval_seconds &lt;= 10; print(settings.inbox_dir)"
  </verify>
  <done>
    配置可加载且扫描间隔默认满足 NFR（≤10s）
  </done>
  <depends_on>T01</depends_on>
</task>

<task id="T04" parallel="true" status="done">
  <name>任务表模型 + Alembic 初始迁移</name>
  <read_files>
    apps/api/app/config.py
    .specs/alarm-image-verify/DESIGN.md
  </read_files>
  <write_files>
    apps/api/app/db.py
    apps/api/app/models.py
    apps/api/alembic.ini
    apps/api/alembic/env.py
    apps/api/alembic/script.py.mako
    apps/api/alembic/versions/
  </write_files>
  <action>
    定义 Task 实体（task_id、created_at、status、source、alarm_bboxes JSON、detections JSON、image_path、alarm_id 可选、error 可选）；SQLite + Alembic 可逆初始迁移。
  </action>
  <verify>
    cd apps/api &amp;&amp; alembic upgrade head &amp;&amp; python -c "from app.models import Task; print(Task.__tablename__)"
  </verify>
  <done>
    库表可迁移创建，支撑任务落库（AC-1 持久化前提）
  </done>
  <depends_on>T01</depends_on>
</task>

<task id="T05" parallel="true" status="done">
  <name>Detector 协议 + Stub 实现（可测）</name>
  <read_files>
    .specs/adr/004-ultralytics-detector.md
    .specs/CONTEXT.md
    .specs/alarm-image-verify/DESIGN.md
  </read_files>
  <write_files>
    apps/api/app/detect/__init__.py
    apps/api/app/detect/base.py
    apps/api/app/detect/stub.py
    apps/api/tests/test_detector_stub.py
  </write_files>
  <action>
    定义 Detection 与 Detector 协议（predict→label/confidence/可选 xywh）；实现 StubDetector（固定或基于尺寸的可预测输出）供无权重环境测试。
  </action>
  <verify>
    cd apps/api &amp;&amp; python -m pytest tests/test_detector_stub.py -q
  </verify>
  <done>
    检测抽象可单测，不绑定 Ultralytics（ADR-004）
  </done>
  <depends_on>T01</depends_on>
</task>

<task id="T06" parallel="true" status="done">
  <name>UltralyticsDetector 默认实现与工厂选择</name>
  <read_files>
    apps/api/app/detect/base.py
    apps/api/app/config.py
    .specs/adr/004-ultralytics-detector.md
  </read_files>
  <write_files>
    apps/api/app/detect/ultralytics_impl.py
    apps/api/app/detect/factory.py
    apps/api/tests/test_detector_factory.py
  </write_files>
  <action>
    实现 UltralyticsDetector（全图推理、读 conf/device/weights）；factory 按配置在 stub/ultralytics 间切换；缺权重时测试走 stub。
  </action>
  <verify>
    cd apps/api &amp;&amp; python -m pytest tests/test_detector_factory.py -q
  </verify>
  <done>
    可通过配置选择检测后端，默认指向 Ultralytics
  </done>
  <depends_on>T05</depends_on>
</task>

<task id="T07" parallel="true" status="done">
  <name>TaskRepository 读写封装</name>
  <read_files>
    apps/api/app/models.py
    apps/api/app/db.py
    .specs/alarm-image-verify/DESIGN.md
  </read_files>
  <write_files>
    apps/api/app/tasks/__init__.py
    apps/api/app/tasks/repo.py
    apps/api/tests/test_task_repo.py
  </write_files>
  <action>
    实现创建/更新状态/按 id 查询/分页列表；JSON 字段存 alarm_bboxes 与 detections。
  </action>
  <verify>
    cd apps/api &amp;&amp; python -m pytest tests/test_task_repo.py -q
  </verify>
  <done>
    任务仓储可支撑列表与详情 API
  </done>
  <depends_on>T03,T04</depends_on>
</task>

<task id="T08" parallel="false" status="done">
  <name>VerifyService：校验→落盘→推理→落库</name>
  <read_files>
    apps/api/app/detect/base.py
    apps/api/app/tasks/repo.py
    apps/api/app/config.py
    .specs/CONTEXT.md
    .specs/adr/002-sync-inline-inference.md
  </read_files>
  <write_files>
    apps/api/app/services/__init__.py
    apps/api/app/services/verify.py
    apps/api/app/ingest/bbox.py
    apps/api/tests/test_verify_service.py
  </write_files>
  <action>
    解析 CONTEXT bbox schema；校验图片后缀与大小；写入 data/images/{task_id}/；调用 Detector；写 succeeded/failed；返回统一结果结构。API 与目录共用此服务。
  </action>
  <verify>
    cd apps/api &amp;&amp; python -m pytest tests/test_verify_service.py -q
  </verify>
  <done>
    入图主路径可单测跑通（AC-1/3 共用核心）
  </done>
  <depends_on>T05,T07</depends_on>
</task>

<task id="T09" parallel="true" status="done">
  <name>同步 POST /api/v1/verify 与错误 4xx</name>
  <read_files>
    apps/api/app/services/verify.py
    apps/api/app/main.py
    .specs/alarm-image-verify/REQUIREMENT.md
    .specs/alarm-image-verify/DESIGN.md
  </read_files>
  <write_files>
    apps/api/app/api/__init__.py
    apps/api/app/api/verify.py
    apps/api/app/main.py
    apps/api/tests/test_api_verify.py
  </write_files>
  <action>
    实现 multipart（file + bbox）同步接口；成功返回 task_id 与 detections；缺图/坏 JSON 返回 4xx；不产生成功任务。挂到 main。
  </action>
  <verify>
    cd apps/api &amp;&amp; python -m pytest tests/test_api_verify.py -q
  </verify>
  <done>
    覆盖 AC-1、AC-2、AC-7（同步响应可消费）
  </done>
  <depends_on>T08</depends_on>
</task>

<task id="T10" parallel="true" status="done">
  <name>任务查询 GET /api/v1/tasks 与详情/图像</name>
  <read_files>
    apps/api/app/tasks/repo.py
    apps/api/app/main.py
    .specs/alarm-image-verify/DESIGN.md
  </read_files>
  <write_files>
    apps/api/app/api/tasks.py
    apps/api/app/main.py
    apps/api/tests/test_api_tasks.py
  </write_files>
  <action>
    实现列表分页、详情（含 alarm_bboxes/detections/image_url）、GET 原图字节；只读无改判接口。
  </action>
  <verify>
    cd apps/api &amp;&amp; python -m pytest tests/test_api_tasks.py -q
  </verify>
  <done>
    支撑审核台数据与 AC-5/6 后端侧
  </done>
  <depends_on>T08</depends_on>
</task>

<task id="T11" parallel="true" status="done">
  <name>目录 sidecar 扫描器与跳过逻辑</name>
  <read_files>
    apps/api/app/services/verify.py
    apps/api/app/config.py
    .specs/CONTEXT.md
    .specs/alarm-image-verify/REQUIREMENT.md
  </read_files>
  <write_files>
    apps/api/app/ingest/__init__.py
    apps/api/app/ingest/scanner.py
    apps/api/app/main.py
    apps/api/tests/test_scanner.py
  </write_files>
  <action>
    按间隔扫描 inbox；同名图片+json 调用 VerifyService；成功后移至 done/ 或标记；仅有图无 json 跳过并打日志/可选 skipped 记录；应用 lifespan 启动扫描循环。
  </action>
  <verify>
    cd apps/api &amp;&amp; python -m pytest tests/test_scanner.py -q
  </verify>
  <done>
    覆盖 AC-3、AC-4
  </done>
  <depends_on>T08</depends_on>
</task>

<task id="T12" parallel="true" status="done">
  <name>物化 UI design tokens 为 CSS variables</name>
  <read_files>
    .specs/alarm-image-verify/UI-DESIGN.md
    apps/web/src/main.tsx
  </read_files>
  <write_files>
    apps/web/src/styles/tokens.css
    apps/web/src/styles/global.css
    apps/web/src/main.tsx
    apps/web/index.html
  </write_files>
  <action>
    将 UI-DESIGN frontmatter 的颜色/间距/圆角/动效写入 :root；引入 Barlow Condensed 与 IBM Plex 字体；global 基础 reset；尊重 prefers-reduced-motion。
  </action>
  <verify>
    cd apps/web &amp;&amp; npm run build
  </verify>
  <done>
    Tokens 可被后续组件引用（T-UI-01）
  </done>
  <depends_on>T02</depends_on>
</task>

<task id="T13" parallel="false" status="done">
  <name>审核台壳层：顶栏 + 左右分栏布局</name>
  <read_files>
    .specs/alarm-image-verify/UI-DESIGN.md
    apps/web/src/styles/tokens.css
    apps/web/src/App.tsx
  </read_files>
  <write_files>
    apps/web/src/App.tsx
    apps/web/src/components/TopBar.tsx
    apps/web/src/components/Shell.tsx
    apps/web/src/styles/shell.css
  </write_files>
  <action>
    实现工业风顶栏（产品名 + 就绪占位）与左列表/右详情分栏壳；无 KPI 卡片；无改判按钮。
  </action>
  <verify>
    cd apps/web &amp;&amp; npm run build
  </verify>
  <done>
    布局符合 UI-DESIGN v0 结构
  </done>
  <depends_on>T12</depends_on>
</task>

<task id="T14" parallel="true" status="done">
  <name>任务列表组件（只读行选中态）</name>
  <read_files>
    .specs/alarm-image-verify/UI-DESIGN.md
    apps/web/src/components/Shell.tsx
    .specs/alarm-image-verify/REQUIREMENT.md
  </read_files>
  <write_files>
    apps/web/src/components/TaskList.tsx
    apps/web/src/components/TaskRow.tsx
    apps/web/src/styles/task-list.css
    apps/web/src/App.tsx
  </write_files>
  <action>
    渲染任务行（task_id、时间、status）；选中态；空态文案；禁止改判控件。可用 props mock 数据先跑通 UI。
  </action>
  <verify>
    cd apps/web &amp;&amp; npm run build
  </verify>
  <done>
    满足 AC-5 UI 侧可展示列表
  </done>
  <depends_on>T13</depends_on>
</task>

<task id="T15" parallel="true" status="done">
  <name>任务详情 + ImageStage 双层框</name>
  <read_files>
    .specs/alarm-image-verify/UI-DESIGN.md
    apps/web/src/components/Shell.tsx
    .specs/CONTEXT.md
  </read_files>
  <write_files>
    apps/web/src/components/TaskDetail.tsx
    apps/web/src/components/ImageStage.tsx
    apps/web/src/components/DetectionTable.tsx
    apps/web/src/styles/task-detail.css
    apps/web/src/App.tsx
  </write_files>
  <action>
    详情展示原图；canvas/SVG 叠加原告警实线框与二次识别虚线框；下方 mono 表展示 label/confidence；无保存改判。
  </action>
  <verify>
    cd apps/web &amp;&amp; npm run build
  </verify>
  <done>
    满足 AC-6 UI 对照要素
  </done>
  <depends_on>T13</depends_on>
</task>

<task id="T16" parallel="false" status="done">
  <name>前端 API client + 列表/详情联调</name>
  <read_files>
    apps/web/src/components/TaskList.tsx
    apps/web/src/components/TaskDetail.tsx
    apps/api/app/api/tasks.py
    .specs/alarm-image-verify/DESIGN.md
  </read_files>
  <write_files>
    apps/web/src/api/client.ts
    apps/web/src/api/types.ts
    apps/web/src/App.tsx
    apps/web/vite.config.ts
  </write_files>
  <action>
    封装 GET tasks/详情；Vite 代理到 API；App 串联选中与拉取；刷新按钮文案符合 UI 规约。
  </action>
  <verify>
    cd apps/web &amp;&amp; npm run build
  </verify>
  <done>
    审核台可对真实 API 消费列表与详情（AC-5/6 联调前提）
  </done>
  <depends_on>T10,T14,T15</depends_on>
</task>

<task id="T17" parallel="true" status="done">
  <name>端到端 API 回归：sidecar 目录用例</name>
  <read_files>
    apps/api/app/ingest/scanner.py
    apps/api/tests/
    .specs/alarm-image-verify/REQUIREMENT.md
  </read_files>
  <write_files>
    apps/api/tests/test_ac_directory_flow.py
    apps/api/tests/fixtures/
  </write_files>
  <action>
    用临时目录投放成对 sidecar 与仅图文件，驱动 scanner/VerifyService，断言成功任务与跳过行为（AC-3/4 自动化）。
  </action>
  <verify>
    cd apps/api &amp;&amp; python -m pytest tests/test_ac_directory_flow.py -q
  </verify>
  <done>
    AC-3/4 有自动化命令可重复验证
  </done>
  <depends_on>T09,T10,T11</depends_on>
</task>

<task id="T18" parallel="true" status="done">
  <name>Docker Compose 与运行文档</name>
  <read_files>
    apps/api/pyproject.toml
    apps/web/package.json
    .specs/alarm-image-verify/DESIGN.md
  </read_files>
  <write_files>
    docker-compose.yml
    apps/api/Dockerfile
    apps/web/Dockerfile
    README.md
    apps/api/.env.example
  </write_files>
  <action>
    提供 api 服务镜像（CPU 默认）、卷挂载 data/images 与 inbox；README 写明启动、同步 API 示例、sidecar 约定、stub/权重切换；不写多租户/鉴权。
  </action>
  <verify>
    docker compose config
  </verify>
  <done>
    本地/容器启动路径文档化，上线风险 R3 有缓解入口
  </done>
  <depends_on>T01,T02</depends_on>
</task>

<task id="T19" parallel="false" status="done">
  <name>API 挂载 Web 静态资源（可选同港交付）</name>
  <read_files>
    apps/api/app/main.py
    apps/web/package.json
    .specs/alarm-image-verify/DESIGN.md
  </read_files>
  <write_files>
    apps/api/app/main.py
    apps/api/scripts/check_static.py
    README.md
  </write_files>
  <action>
    配置在存在 apps/web/dist 时挂载静态与 SPA fallback；脚本检测挂载逻辑不抛错；README 补充 build 顺序。
  </action>
  <verify>
    cd apps/api &amp;&amp; python scripts/check_static.py
  </verify>
  <done>
    单机可同端口打开审核台（与 DESIGN 部署一致）
  </done>
  <depends_on>T16,T18</depends_on>
</task>
```

---

## 状态字段说明

- `status="pending"` — 未开始
- `status="in_progress"` — 进行中
- `status="done"` — 已完成（verify 通过）
- `status="blocked"` — 阻塞（必须在「阻塞日志」记录）

---

## 阻塞日志

| 任务 | 阻塞原因 | 待人工决策项 | 时间 |
|---|---|---|---|
|  |  |  |  |

---

## Fix 任务（来自 REVIEW / INTEGRATION）

```xml
<!-- 占位 -->
```

---

## AC 映射速查

| AC | 任务 |
|----|------|
| AC-1 / AC-2 / AC-7 | T08, T09 |
| AC-3 / AC-4 | T11, T17 |
| AC-5 | T10, T14, T16 |
| AC-6 | T10, T15, T16 |
