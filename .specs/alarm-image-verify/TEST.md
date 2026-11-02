# TEST: 报警图片二次校验平台

- **Change ID**: alarm-image-verify
- **关联**: `@.specs/alarm-image-verify/REQUIREMENT.md`、`@.specs/alarm-image-verify/DESIGN.md`
- **执行时间**: 2026-11-02

## 适用矩阵

| 轮次 | 状态 | 范围 | 跳过理由 |
|---|---|---|---|
| 第 1 轮 · 功能 | ✅ 必跑 | AC-1~7 | — |
| 第 2 轮 · 性能 | ⚠️ 部分 | 软目标基线记录 | 无 k6；NFR 为软目标非硬门禁 |
| 第 3 轮 · 安全 | ⚠️ 部分 | 上传类型/大小与 4xx | v1 无鉴权；未跑全量 CVE 扫描工具 |
| 第 4 轮 · 兼容 | ⚠️ 部分 | API 契约 + Web build | 未做多浏览器手工矩阵 |
| 第 5 轮 · 可观测 | ⚠️ 部分 | healthz + 扫描日志 | 无独立监控大盘（out of scope） |

---

## 第 1 轮 · 功能测试

### AC 覆盖矩阵

| AC | 自动化 | 结果 |
|----|--------|------|
| AC-1 同步 API 返回类别+置信度 | `tests/test_api_verify.py` | ✅ |
| AC-2 缺参/坏 JSON 4xx | `tests/test_api_verify.py` | ✅ |
| AC-3 目录 sidecar | `tests/test_scanner.py` / `test_ac_directory_flow.py` | ✅ |
| AC-4 仅图跳过 | 同上 | ✅ |
| AC-5 列表只读 | `tests/test_api_tasks.py` + Web TaskList | ✅ API；UAT 见下 |
| AC-6 详情对照 | API detail + Web ImageStage | ✅ API；UAT 见下 |
| AC-7 同步响应可消费 | `test_api_verify.py` | ✅ |

### 命令输出

```text
cd apps/api && python -m pytest -q
..........                                                               [100%]
10 passed, 1 warning in 0.83s
```

### UAT（审核台）

1. 启动 API + Web，打开审核台
2. 调用一次 `/api/v1/verify` 或投放 sidecar
3. 列表出现任务；点开详情可见原图与结果表；无改判按钮

---

## 第 2 轮 · 性能

- 预算：单张 P95 < 5s（模型已加载，软目标）
- 本次：stub 检测路径 pytest/API 亚秒级；**未跑 k6**
- 结论：⚠️ 基线未量化门禁，stub 路径无阻塞

## 第 3 轮 · 安全

- 上传后缀白名单 + max_upload_bytes；坏 JSON → 400
- 受信网、无鉴权（REQUIREMENT）
- 结论：⚠️ 符合 v1 假设；生产暴露公网前需补鉴权 CHANGE

## 第 4 轮 · 兼容

- `npm run build` 通过（Chrome/Edge 现代浏览器目标）
- OpenAPI 路径 `/api/v1/verify`、`/api/v1/tasks` 存在

## 第 5 轮 · 可观测

- `GET /healthz` 返回 status / detector_backend / model_ready
- 目录扫描有 INFO/WARNING 日志
- 无大盘（刻意 out）

---

## 总结

功能轮 **10/10 自动化通过**。审核台 UAT 与本轮「打开界面」一并执行。
