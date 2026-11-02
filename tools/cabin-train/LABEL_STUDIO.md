# Label Studio：标注驾驶室 cabin

环境：`conda activate label-studio`（不要用 base / 本仓库 `.venv`）

## 1. 准备待标注图片

把现场图放进：

`tools/cabin-train/raw_images/`

## 2. 启动

```powershell
conda activate label-studio
cd D:\dev\my_workspace\cursor_test
label-studio
```

浏览器打开：http://localhost:8080  
（首次会要求注册本地账号）

## 3. 建项目

1. Create Project → 名称如 `cabin-detect`
2. **Labeling Setup** → Code 模式，粘贴 `label_studio_config.xml` 全文（只有一个框：`cabin`）
3. **Import** → Upload Files，选 `raw_images` 里的图  
   或开启 Local Storage（高级）：指向 `raw_images` 绝对路径

## 4. 标注要点

- 框住**驾驶室主体**（窗+舱体即可，不必抠人）
- 一张图可多个 cabin（多车）
- 看不清 / 无驾驶室 → 跳过或标完不框

## 5. 导出给训练

**推荐**：Export → **YOLO**（若版本有该选项）  
解压后把 `images` / `labels` 按 8:2 放进：

```text
tools/cabin-train/dataset/images/{train,val}
tools/cabin-train/dataset/labels/{train,val}
```

**备选**：Export → JSON，再用项目 `.venv` 转换：

```powershell
.\.venv\Scripts\Activate.ps1
python tools\cabin-train\scripts\ls_json_to_yolo.py --input path\to\export.json --out tools\cabin-train\dataset --split 0.2
```

有一定数量（建议先 ≥50～100 张有框样本）再训练。
