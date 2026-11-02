from pathlib import Path

from app.config import settings
from app.detect.base import Detection


class UltralyticsDetector:
    def __init__(
        self,
        weights_path: str | None = None,
        device: str | None = None,
        conf_threshold: float | None = None,
    ) -> None:
        self.weights_path = weights_path or settings.weights_path
        self.device = device or settings.device
        self.conf_threshold = conf_threshold if conf_threshold is not None else settings.conf_threshold
        self._model = None

    def _load(self):
        if self._model is not None:
            return self._model
        from ultralytics import YOLO

        self._model = YOLO(self.weights_path)
        return self._model

    def predict(self, image_path: Path) -> list[Detection]:
        model = self._load()
        results = model.predict(
            source=str(image_path),
            conf=self.conf_threshold,
            device=self.device,
            verbose=False,
        )
        detections: list[Detection] = []
        for result in results:
            names = result.names or {}
            boxes = getattr(result, "boxes", None)
            if boxes is None:
                continue
            for box in boxes:
                cls_id = int(box.cls.item())
                conf = float(box.conf.item())
                xywh = box.xywh.cpu().numpy().tolist()[0]
                detections.append(
                    Detection(
                        label=str(names.get(cls_id, cls_id)),
                        confidence=conf,
                        x=float(xywh[0] - xywh[2] / 2),
                        y=float(xywh[1] - xywh[3] / 2),
                        w=float(xywh[2]),
                        h=float(xywh[3]),
                    )
                )
        return detections
