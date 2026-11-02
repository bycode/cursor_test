"""Train cabin detector with Ultralytics. Run via repo .venv only."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path


def _absolute_data_yaml(src: Path) -> Path:
    """Ultralytics resolves relative `path` against its global datasets_dir; force absolute."""
    import yaml

    raw = yaml.safe_load(src.read_text(encoding="utf-8"))
    root = src.parent
    dataset_path = Path(raw.get("path", "dataset"))
    if not dataset_path.is_absolute():
        dataset_path = (root / dataset_path).resolve()
    raw["path"] = dataset_path.as_posix()
    tmp = Path(tempfile.gettempdir()) / f"cabin-data-{src.stem}.yaml"
    tmp.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    return tmp


def main() -> None:
    parser = argparse.ArgumentParser(description="Train YOLO cabin detector")
    parser.add_argument(
        "--data",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data.yaml",
    )
    parser.add_argument("--model", default="yolov8n.pt", help="base weights")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1] / "runs")
    parser.add_argument("--name", default="cabin")
    args = parser.parse_args()

    from ultralytics import YOLO

    data_yaml = _absolute_data_yaml(args.data.resolve())
    print(f"data_yaml={data_yaml}")
    model = YOLO(args.model)
    model.train(
        data=str(data_yaml),
        epochs=args.epochs,
        imgsz=args.imgsz,
        device=args.device,
        batch=args.batch,
        project=str(args.project),
        name=args.name,
        exist_ok=True,
    )
    best = args.project / args.name / "weights" / "best.pt"
    print(f"best_weights={best}")


if __name__ == "__main__":
    main()
