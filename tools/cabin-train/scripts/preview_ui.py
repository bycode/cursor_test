"""Local UI to smoke-test cabin weights. Use repo .venv only."""

from __future__ import annotations

from pathlib import Path

import gradio as gr
from ultralytics import YOLO

import os

ROOT = Path(__file__).resolve().parents[1]
_COTTON = ROOT / "runs" / "cottonhat" / "weights" / "best.pt"
_CABIN = ROOT / "runs" / "cabin" / "weights" / "best.pt"
DEFAULT_WEIGHTS = Path(os.environ.get("WEIGHTS_PATH") or (_COTTON if _COTTON.is_file() else _CABIN))
_model: YOLO | None = None
_loaded: str | None = None


def _get_model(weights: str) -> YOLO:
    global _model, _loaded
    path = Path(weights)
    if not path.is_file():
        raise FileNotFoundError(f"weights not found: {path}")
    key = str(path.resolve())
    if _model is None or _loaded != key:
        _model = YOLO(key)
        _loaded = key
    return _model


def predict(image, conf: float, weights: str):
    if image is None:
        return None, "请先上传图片"
    model = _get_model(weights)
    import torch

    device = 0 if torch.cuda.is_available() else "cpu"
    results = model.predict(source=image, conf=float(conf), device=device, verbose=False)
    r0 = results[0]
    plotted = r0.plot()  # BGR ndarray
    # Gradio Image expects RGB
    import cv2

    rgb = cv2.cvtColor(plotted, cv2.COLOR_BGR2RGB)
    n = 0 if r0.boxes is None else len(r0.boxes)
    lines = [f"检出框数: {n}", f"conf阈值: {conf}", f"weights: {weights}"]
    if n:
        for i, b in enumerate(r0.boxes[:20]):
            conf_v = float(b.conf)
            xyxy = [round(float(x), 1) for x in b.xyxy.cpu().tolist()[0]]
            lines.append(f"[{i}] conf={conf_v:.3f} xyxy={xyxy}")
        if n > 20:
            lines.append(f"... 另有 {n - 20} 个框未列出")
    return rgb, "\n".join(lines)


def main() -> None:
    print(f"weights={DEFAULT_WEIGHTS}", flush=True)
    with gr.Blocks(title="CottonHat 模型试跑") as demo:
        gr.Markdown(
            "## CottonHat YOLO 试跑\n"
            "上传现场图，调节置信度，查看安全帽检测框。"
        )
        with gr.Row():
            with gr.Column():
                image_in = gr.Image(type="numpy", label="输入图")
                weights = gr.Textbox(value=str(DEFAULT_WEIGHTS), label="权重路径")
                conf = gr.Slider(0.05, 0.95, value=0.25, step=0.05, label="confidence")
                btn = gr.Button("推理", variant="primary")
            with gr.Column():
                image_out = gr.Image(type="numpy", label="结果图")
                info = gr.Textbox(label="检出摘要", lines=12)
        btn.click(predict, inputs=[image_in, conf, weights], outputs=[image_out, info])

    print("launching Gradio on http://127.0.0.1:7860 ...", flush=True)
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=False, show_error=True)


if __name__ == "__main__":
    main()
