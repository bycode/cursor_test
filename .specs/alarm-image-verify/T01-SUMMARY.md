# SUMMARY: T01 - 初始化 API 工程骨架与依赖锁定

- **Change ID**: alarm-image-verify
- **Task ID**: T01
- **完成时间**: 2026-11-02
- **AI 角色**: Dev

---

## 做了什么（一段话）

空仓新建 `apps/api`：`pyproject.toml` 锁定 FastAPI 栈依赖（含 ultralytics 等）、`Settings` 配置入口、`FastAPI` 应用与 `GET /healthz`。根 `README` / `.gitignore` 就位。本机 verify 仅安装了导入所需核心包（fastapi / pydantic-settings / uvicorn）；完整 `pip install -e ".[dev]"`（含 ultralytics）留给后续检测任务，避免本任务超时。

## 改动文件

| 文件 | 性质 | 说明 |
|---|---|---|
| apps/api/pyproject.toml | 新增 | 依赖与 pytest 配置 |
| apps/api/README.md | 新增 | API 启动说明 |
| apps/api/app/__init__.py | 新增 | 包标记 |
| apps/api/app/main.py | 新增 | app + /healthz |
| apps/api/app/config.py | 新增 | pydantic-settings 入口 |
| .gitignore | 新增 | Python/Node/data 忽略 |
| README.md | 新增 | monorepo 占位 |
| .specs/LESSONS.md | 新增 | 流程要求空骨架（非 TASK write_files） |

## verify 输出（必填）

```text
> cd apps/api; python -c "from app.main import app; print(app.title)"
Alarm Image Verify

> python -c "from app.main import app; print([r.path for r in app.routes])"
['/openapi.json', '/docs', '/docs/oauth2-redirect', '/redoc', '/healthz']
```

## 6 维自查（生产代码改动必填）

### 沿用既有抽象（R6.4）

- grep/workspace：空仓，无既有 FastAPI/Repository 实现可复用。
- GitNexus：不可用，未做符号级影响检查（SUMMARY 标注）。

### 🟢 R1 · 认知过载：通过
**Symptom**：无超长函数  
**Source**：骨架仅健康检查  
**Consequence**：无  
**Remedy**：—

### 🟢 R2 · 变更传播：通过
**Symptom**：无  
**Source**：改动限于 write_files + LESSONS 流程文件  
**Consequence**：无  
**Remedy**：—

### 🟢 R3~R6：通过（无重复逻辑 / 无多余抽象 / 无错误依赖方向 / 领域名用 verify/healthz）

### 已知接受 + 理由（🟡）

- 未在本任务完整安装 ultralytics：verify 不依赖；完整安装在 T06 前执行。

## 数据库迁移

N/A

## 破坏性变更

N/A（新建）

## 越界检查

```text
实际新建：apps/api/**, .gitignore, README.md, .specs/LESSONS.md
TASK write_files：apps/api/pyproject.toml, README, app/*, .gitignore, 根 README
超出：.specs/LESSONS.md（flow-dev R1.8 要求创建空骨架）
```

## 提交

未提交（用户规则：未明确要求不自动 commit）。需要时可用：

`feat(alarm-image-verify): T01 scaffold FastAPI api package`
