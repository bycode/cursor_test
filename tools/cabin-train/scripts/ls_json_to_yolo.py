"""Convert Label Studio JSON export to YOLO cabin dataset folders."""

from __future__ import annotations

import argparse
import json
import random
import shutil
from pathlib import Path


def _iter_results(task: dict) -> list[dict]:
    anns = task.get("annotations") or []
    if not anns:
        return []
    res = anns[-1].get("result") or []
    return [r for r in res if r.get("type") == "rectanglelabels"]


def convert(export_path: Path, out_dir: Path, split: float, seed: int) -> None:
    data = json.loads(export_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("expected Label Studio JSON list export")

    random.seed(seed)
    items: list[tuple[dict, list[dict], str]] = []
    for task in data:
        results = _iter_results(task)
        if not results:
            continue
        image = (task.get("data") or {}).get("image") or ""
        items.append((task, results, str(image)))

    random.shuffle(items)
    n_val = max(1, int(len(items) * split)) if len(items) >= 5 else (1 if items else 0)

    for split_name in ("train", "val"):
        (out_dir / "images" / split_name).mkdir(parents=True, exist_ok=True)
        (out_dir / "labels" / split_name).mkdir(parents=True, exist_ok=True)

    for i, (task, results, image_field) in enumerate(items):
        split_name = "val" if i < n_val else "train"
        src = Path(image_field.replace("/data/local-files/?d=", ""))
        stem = src.stem if src.suffix else f"task_{task.get('id', i)}"
        label_path = out_dir / "labels" / split_name / f"{stem}.txt"
        lines: list[str] = []
        for r in results:
            val = r.get("value") or {}
            x = float(val["x"]) / 100.0
            y = float(val["y"]) / 100.0
            w = float(val["width"]) / 100.0
            h = float(val["height"]) / 100.0
            cx, cy = x + w / 2.0, y + h / 2.0
            lines.append(f"0 {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")
        label_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        if src.is_file():
            shutil.copy2(src, out_dir / "images" / split_name / src.name)
        else:
            print(f"warn: image not found for task {task.get('id')}: {src}")

    print(f"converted={len(items)} val={n_val} out={out_dir}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--split", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    convert(args.input, args.out, args.split, args.seed)


if __name__ == "__main__":
    main()
