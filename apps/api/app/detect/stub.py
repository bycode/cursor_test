from pathlib import Path

from PIL import Image

from app.detect.base import Detection


class StubDetector:
    """Deterministic detector: returns a cabin covering the left half of the image."""

    def predict(self, image_path: Path) -> list[Detection]:
        with Image.open(image_path) as img:
            width, height = img.size
        return [
            Detection(
                label="cabin",
                confidence=0.91,
                x=0.0,
                y=0.0,
                w=width * 0.5,
                h=height * 1.0,
            )
        ]
