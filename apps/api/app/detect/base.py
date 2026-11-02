from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class Detection:
    label: str
    confidence: float
    x: float | None = None
    y: float | None = None
    w: float | None = None
    h: float | None = None

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "label": self.label,
            "confidence": self.confidence,
        }
        if self.x is not None:
            payload["x"] = self.x
            payload["y"] = self.y
            payload["w"] = self.w
            payload["h"] = self.h
        return payload


class Detector(Protocol):
    def predict(self, image_path: Path) -> list[Detection]:
        ...
