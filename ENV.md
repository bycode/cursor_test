# Python 环境约定

## 现状说明

早期脚手架曾用过 Anaconda **base**（`D:\bin\anaconda3\python.exe`）装过部分 API 包。从现在起**停止往 base 装本项目依赖**。

## 本项目只用这些环境

| 环境 | 路径/名字 | 用途 |
|------|-----------|------|
| 项目 venv | `D:\dev\my_workspace\cursor_test\.venv` | API、pytest、cabin 训练（ultralytics） |
| conda `label-studio` | 已有 named env | 只跑 Label Studio 标注 |
| 禁止 | conda `base`、WindowsApps Python | 不往这里 `pip install` 本项目包 |

## 常用命令

```powershell
cd D:\dev\my_workspace\cursor_test
.\.venv\Scripts\Activate.ps1

# API
python -m pip install -e "apps\api[dev]"
python -m pytest apps\api\tests -q

# 训练依赖
python -m pip install -r tools\cabin-train\requirements.txt
```

Label Studio：

```powershell
conda activate label-studio
label-studio
```
