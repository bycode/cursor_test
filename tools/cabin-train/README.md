# cabin-train — 驾驶室 YOLO 训练工具

用 Ultralytics 微调 `cabin` 检测模型，供 `apps/api` 二次校验使用。

## Python 环境（重要）

本仓库约定：

| 用途 | 环境 | 说明 |
|------|------|------|
| API + 本训练工具 | 仓库根目录 `.venv` | **唯一**安装 ultralytics / fastapi 等的地方 |
| Label Studio | 已有 conda env `label-studio` | 只跑标注服务，不往 base 装包 |
| 禁止 | conda `base` / 系统 Python | 避免把默认环境搞乱 |

激活训练环境（PowerShell）：

```powershell
cd D:\dev\my_workspace\cursor_test
.\.venv\Scripts\Activate.ps1
python -m pip install -r tools\cabin-train\requirements.txt
```

## 目录约定（YOLO）

```text
tools/cabin-train/
  dataset/
    images/{train,val}/
    labels/{train,val}/   # YOLO txt：class x_center y_center w h（归一化）
  data.yaml
  runs/                   # 训练输出（gitignore）
```

`data.yaml` 中 `names: [cabin]`，`nc: 1`。

## Label Studio

1. 启动（使用你已有环境，**不要**装进 base）：

```powershell
conda activate label-studio
label-studio
```

2. 项目标签建议只要一个矩形：`cabin`
3. 导出选择 **YOLO**（或 JSON 后用转换脚本）
4. 将导出的 `images` / `labels` 放进上面的 `dataset/` 并按 train/val 拆分（建议 8:2）

若导出为 LS JSON，可用：

```powershell
python tools\cabin-train\scripts\ls_json_to_yolo.py --input path\to\export.json --out tools\cabin-train\dataset --split 0.2
```

## 训练

```powershell
.\.venv\Scripts\Activate.ps1
python tools\cabin-train\scripts\train.py --data tools\cabin-train\data.yaml --epochs 50 --model yolov8n.pt
```

权重默认写到：`tools/cabin-train/runs/cabin/weights/best.pt`

## 接到 API

```powershell
$env:DETECTOR_BACKEND="ultralytics"
$env:WEIGHTS_PATH="D:\dev\my_workspace\cursor_test\tools\cabin-train\runs\cabin\weights\best.pt"
# 用 .venv 启动 API
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir apps\api --reload --host 127.0.0.1 --port 8000
```

## 评估

```powershell
python tools\cabin-train\scripts\eval.py --weights tools\cabin-train\runs\cabin\weights\best.pt --data tools\cabin-train\data.yaml
```

## 试跑 UI（看框）

```powershell
.\.venv\Scripts\Activate.ps1
python tools\cabin-train\scripts\preview_ui.py
```

浏览器打开：http://127.0.0.1:7860/  
可上传图、调 conf、看 cabin 框（小样本权重建议 conf≥0.5）。
