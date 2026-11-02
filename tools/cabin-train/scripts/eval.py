"""Evaluate cabin detector. Run via repo .venv only."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Eval YOLO cabin detector")
    parser.add_argument("--weights", type=Path, required=True)
    parser.add_argument(
        "--data",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data.yaml",
    )
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    from ultralytics import YOLO

    model = YOLO(str(args.weights))
    metrics = model.val(data=str(args.data.resolve()), imgsz=args.imgsz, device=args.device)
    print(metrics)


if __name__ == "__main__":
    main()
