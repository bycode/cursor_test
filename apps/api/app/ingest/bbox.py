import json
from typing import Any


class BBoxParseError(ValueError):
    pass


def parse_bbox_payload(raw: str | bytes) -> dict[str, Any]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BBoxParseError("bbox JSON is invalid") from exc
    if not isinstance(data, dict):
        raise BBoxParseError("bbox JSON must be an object")
    boxes = data.get("bboxes")
    if boxes is None:
        raise BBoxParseError("bbox JSON missing bboxes")
    if not isinstance(boxes, list):
        raise BBoxParseError("bboxes must be a list")
    for item in boxes:
        if not isinstance(item, dict):
            raise BBoxParseError("each bbox must be an object")
        for key in ("x", "y", "w", "h"):
            if key not in item:
                raise BBoxParseError(f"bbox missing field {key}")
    return data
