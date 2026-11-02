---
name: 报警二次校验 · 审核日志台
description: 工业风深色复核台——双层框对照优先，密列表次之，无 KPI 墙

colors:
  brand: "oklch(0.78 0.14 75)"
  brand-deep: "oklch(0.62 0.13 70)"
  brand-mute: "oklch(0.78 0.14 75 / 0.18)"
  bg: "oklch(0.18 0.02 250)"
  bg-elevated: "oklch(0.22 0.02 250)"
  surface: "oklch(0.25 0.018 250)"
  surface-hover: "oklch(0.28 0.02 250)"
  text-primary: "oklch(0.92 0.01 250)"
  text-secondary: "oklch(0.72 0.02 250)"
  text-tertiary: "oklch(0.55 0.02 250)"
  border: "oklch(0.35 0.02 250)"
  border-strong: "oklch(0.45 0.025 250)"
  alarm-box: "oklch(0.78 0.14 75)"
  detect-box: "oklch(0.75 0.12 230)"
  success: "oklch(0.72 0.12 145)"
  danger: "oklch(0.65 0.18 25)"
  warning: "oklch(0.78 0.14 85)"

typography:
  display:
    fontFamily: "\"Barlow Condensed\", \"Arial Narrow\", sans-serif"
    fontSize: "clamp(1.75rem, 2.5vw, 2.25rem)"
    fontWeight: 600
    lineHeight: 1.1
    italic: false
  headline:
    fontFamily: "\"Barlow Condensed\", \"Arial Narrow\", sans-serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: 1.2
  title:
    fontFamily: "\"IBM Plex Sans\", \"Segoe UI\", sans-serif"
    fontSize: "1rem"
    fontWeight: 550
    lineHeight: 1.35
  body:
    fontFamily: "\"IBM Plex Sans\", \"Segoe UI\", sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.45
  supporting:
    fontFamily: "\"IBM Plex Sans\", \"Segoe UI\", sans-serif"
    fontSize: "0.75rem"
    fontWeight: 400
    lineHeight: 1.4
  label:
    fontFamily: "\"IBM Plex Sans\", \"Segoe UI\", sans-serif"
    fontWeight: 500
    fontSize: "0.6875rem"
    textTransform: uppercase
    letterSpacing: "0.06em"
  mono:
    fontFamily: "\"IBM Plex Mono\", ui-monospace, monospace"
    fontSize: "0.75rem"
    fontWeight: 400
    lineHeight: 1.35

spacing:
  "2xs": "4px"
  xs: "10px"
  sm: "16px"
  md: "28px"
  lg: "44px"
  xl: "72px"
  "2xl": "112px"

rounded:
  none: "0"
  hair: "2px"

motion:
  ease-out: "cubic-bezier(0.16, 1, 0.3, 1)"
  duration-fast: "150ms"
  duration-base: "250ms"
  duration-slow: "400ms"

shadow:
  focus-ring: "0 0 0 2px oklch(0.18 0.02 250), 0 0 0 4px oklch(0.78 0.14 75)"
  none-rest: "none"
---

# UI Design: 报警二次校验 · 审核日志台

## 1. 美学北极星

深色工业复核台：左密列表、右大图对照。用户第一眼应看懂「原告警框 vs 二次识别框」，而不是统计卡片。硬边、细网格、等宽数据、单一琥珀强调；零营销话术、零改判控件。

### v0 确认摸路

- **已确认的假设**：
  - 深色台（监控场景例外，非装饰性 dark）
  - 主布局 = 顶栏 + 左列表 + 右详情（图上双层框）
  - 字体三件套：Barlow Condensed / IBM Plex Sans / IBM Plex Mono
  - 强调色琥珀；二次框用冷蓝描边作**语义区分**（框图层，不算第二装饰强调色滥用于 UI chrome）
- **用户指出的偏差**：无（回复 go）

## 2. 4 个决策问题

- **目的**：审核人员事后核对入图与二次识别结果，以降误报排查；核心动作 = 选任务 → 看图对照 → 读类别/置信度
- **调性**：3 工业（Industrial）
- **约束**：Vite + React；键盘可达列表/详情；对比度可读；无品牌 VI；内网部署
- **差异化**：图上双层 bbox 对照是唯一英雄视觉

## 3. 颜色系统

### Primary

- **琥珀 brand** `oklch(0.78 0.14 75)`：焦点行、主按钮、原告警框描边、就绪指示。**绝不用于**大面积填充背景或渐变字。

### Neutral（全部带轻微蓝 chroma）

- **bg** `oklch(0.18 0.02 250)`：主背景
- **surface** `oklch(0.25 0.018 250)`：列表行/面板
- **text-primary** `oklch(0.92 0.01 250)`：主文字
- **border** `oklch(0.35 0.02 250)`：网格与分割线

### 语义（仅状态与图层）

- **detect-box** `oklch(0.75 0.12 230)`：二次识别框描边（仅 canvas）
- **success / danger / warning**：任务状态点，不用于装饰

### 命名规则

- **The One Voice Rule**：UI chrome 主色只有琥珀
- **The Tinted Neutral Rule**：中性色全部带 hue 250 微量 chroma，禁用纯灰/#000/#fff

## 4. 字体系统

- **Display / Headline**：Barlow Condensed — 压缩标题，提高信息密度；**不用 Inter/Roboto**：工业监控感需要有条件的字宽，而非中性 SaaS 默认
- **Body**：IBM Plex Sans — 工程可读、与 mono 同家族气质但不同字体文件（满足「display≠body 同族字重」）
- **Mono**：IBM Plex Mono — task_id、confidence、时间戳

### 层次表

| 角色 | 字体 | 字号 | 字重 | 行高 | 备注 |
|---|---|---|---|---|---|
| Display | Barlow Condensed | clamp(1.75–2.25rem) | 600 | 1.1 | 顶栏产品名 |
| Headline | Barlow Condensed | 1.25rem | 600 | 1.2 | 详情区标题 |
| Title | IBM Plex Sans | 1rem | 550 | 1.35 | 面板小标题 |
| Body | IBM Plex Sans | 0.875rem | 400 | 1.45 | 说明 |
| Supporting | IBM Plex Sans | 0.75rem | 400 | 1.4 | 次要说明 |
| Label | IBM Plex Sans | 0.6875rem | 500 | 1.2 | 大写标签 |
| Mono | IBM Plex Mono | 0.75rem | 400 | 1.35 | 数据 |

## 5. 间距 & 圆角 & 动效

- 间距只许用 frontmatter：`2xs…2xl`（非线性：4/10/16/28/44/72/112）
- 圆角只许 `none` / `hair(2px)`
- 动效：`duration-fast/base` + `ease-out`；尊重 `prefers-reduced-motion: reduce` → duration 0
- 静止元素 **无** drop shadow；focus 仅用 `shadow.focus-ring`

## 6. 关键组件规约

### Button (Primary)

- **形状**：sharp（rounded.hair 可选）
- **背景**：brand；文字：bg（深底反白感用 `oklch(0.18 0.02 250)`）
- **内边距**：xs 垂直 / sm 水平
- **at rest**：无阴影；1px border brand-deep
- **hover**：背景 brand-deep
- **focus**：focus-ring
- **文案**：动词明确，如「刷新列表」；禁用 Submit / Learn more

### Button (Ghost / 次要)

- 透明底 + border；文字 text-primary；hover → surface-hover

### Input / Field

- **at rest**：bg-elevated + border；label 在字段上方（禁止只用 placeholder）
- **focus**：border → brand
- **error**：border danger + supporting 错误文案

### Card / Container

- **at rest**：surface 平面 + 1px border；**禁止**静止 drop shadow
- **hover**：列表行可用 surface-hover，不是抬升阴影
- **嵌套**：禁止 card 套 card；分区用 hairline 分割

### Navigation / Top bar

- 高度约 44px（spacing.lg）；产品名 Display；右侧仅状态指示（模型就绪 / 扫描中）
- active：无下划线装饰条过粗；用 brand 底 2px 线或文字色 brand

### Task list row

- mono task_id + 时间；status 色点（success/danger/warning/text-tertiary）
- selected：左边 2px brand（允许，作为选中态而非装饰侧条滥用于营销卡）；背景 surface-hover

### Image stage（核心）

- 深底；图居中 contain；overlay canvas
- 原告警框：alarm-box 实线 2px；二次框：detect-box 虚线 2px
- 图例：Label + 色键，放在图下方，不悬浮贴纸式 badge 堆叠

### Typography Hierarchy

见 §4。

### Data table（检测结果）

- mono 单元格；表头 Label 大写；无斑马炫光，用 1px border 分行

## 7. Do's and Don'ts（本项目特定）

### Do

- 把像素预算优先给大图对照区
- 状态用短词：成功 / 失败 / 跳过 / 处理中
- 置信度格式固定，如 `0.93`（两位小数）
- 空列表给一句操作指引：「等待 API 或目录投递任务」

### Don't

- KPI 四宫格、渐变 hero、玻璃拟态
- 紫/霓虹青装饰、Gradient text
- 改判 / 覆盖结果按钮
- emoji 状态、AI 插画、stock 监控室照片
- 卡片嵌套与大圆角营销按钮

## 8. 占位符策略

| 缺的东西 | 本项目有什么？ | 缺时用什么占位 | 禁什么 |
|---|---|---|---|
| 图标 | 线性几何（方/线） | [icon] 2xs 方块 | emoji / 粗糙 AI SVG |
| 头像 | 无用户系统 | — | AI 人脸 |
| 图片 | 任务原图 API | 固定比例空槽 +「无图像」Label | stock / AI 图 |
| 数据 | 真实 task API | 空态文案；开发可用 fixture，不假装生产指标 | 编造准确率大盘数字 |
| logo | 文字「报警二次校验」 | 文字 + 1px 几何角标 | AI 自绘 logo |

## 9. 反 AI-slop 自检结果

- [x] 字体类禁忌：未命中（非 Inter；display≠body 同族）
- [x] 颜色类禁忌：未命中（无紫渐变/霓虹青/纯黑白；第二色仅 bbox 语义层与状态）
- [x] 阴影类禁忌：未命中（静止无 shadow）
- [x] 边框类禁忌：未命中（选中 2px 为交互态；无渐变边框/玻璃）
- [x] 动效类禁忌：未命中（无 bounce；支持 reduced-motion）
- [x] 布局类禁忌：未命中（无统一卡片网格 KPI；深色为产品场景例外已声明）
- [x] 文案类禁忌：未命中
- [x] 组件类禁忌：未命中（label 不靠 placeholder 替代）

**例外声明**：深色默认 —— 工业监控复核台，对齐 Grafana 类工具，非营销站「为了酷而 dark」。

## 10. 触发任务

下一步 `flow-task` 时 UI 相关应覆盖：

- T-UI-01：tokens → CSS variables（`:root`）
- T-UI-02：typography + 顶栏
- T-UI-03：TaskList + Row 选中态
- T-UI-04：TaskDetail + ImageStage 双层框
- T-UI-05：DetectionTable + 空态
- T-UI-06：Button / Input 基础（刷新等）

---

> 实现阶段只许引用本文件 tokens；新增色值须先改本文件。
