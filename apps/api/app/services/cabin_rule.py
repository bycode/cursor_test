from __future__ import annotations

from typing import Any


def bbox_center(box: dict[str, Any]) -> tuple[float, float]:
    return float(box["x"]) + float(box["w"]) / 2.0, float(box["y"]) + float(box["h"]) / 2.0


def point_in_xywh(cx: float, cy: float, box: dict[str, Any]) -> bool:
    x, y, w, h = float(box["x"]), float(box["y"]), float(box["w"]), float(box["h"])
    return x <= cx <= x + w and y <= cy <= y + h


def judge_alarm_bboxes(
    alarm_bboxes: list[dict[str, Any]] | None,
    cabin_boxes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Center-in-cabin rule for no-helmet false-alarm exemption."""
    verdicts: list[dict[str, Any]] = []
    for index, alarm in enumerate(alarm_bboxes or []):
        cx, cy = bbox_center(alarm)
        base = {
            "index": index,
            "alarm_bbox": {
                "x": alarm.get("x"),
                "y": alarm.get("y"),
                "w": alarm.get("w"),
                "h": alarm.get("h"),
                "label": alarm.get("label"),
            },
            "center": {"x": cx, "y": cy},
        }
        if not cabin_boxes:
            verdicts.append({**base, "verdict": "uncertain", "reason": "cabin_not_found"})
            continue
        if any(point_in_xywh(cx, cy, cabin) for cabin in cabin_boxes):
            verdicts.append({**base, "verdict": "false_alarm", "reason": "in_cabin"})
        else:
            verdicts.append({**base, "verdict": "confirm", "reason": "not_in_cabin"})
    return verdicts
