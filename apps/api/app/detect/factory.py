from app.config import settings
from app.detect.base import Detector
from app.detect.stub import StubDetector
from app.detect.ultralytics_impl import UltralyticsDetector


def get_detector(backend: str | None = None) -> Detector:
    name = (backend or settings.detector_backend).lower()
    if name == "ultralytics":
        return UltralyticsDetector()
    if name == "stub":
        return StubDetector()
    raise ValueError(f"unsupported detector backend: {name}")
