import json

import pytest

from app.detect.stub import StubDetector
from app.services.verify import VerifyError, VerifyService


def test_verify_success(db_session, sample_image):
    service = VerifyService(db_session, StubDetector())
    result = service.run(
        image_bytes=sample_image.read_bytes(),
        filename="sample.jpg",
        bbox_raw=json.dumps({"bboxes": [{"x": 1, "y": 2, "w": 3, "h": 4}]}),
        source="api",
    )
    assert result["status"] == "succeeded"
    assert result["detections"][0]["label"] == "cabin"
    assert result["bbox_verdicts"][0]["verdict"] == "false_alarm"
    assert result["task_id"]


def test_verify_bad_bbox(db_session, sample_image):
    service = VerifyService(db_session, StubDetector())
    with pytest.raises(VerifyError):
        service.run(
            image_bytes=sample_image.read_bytes(),
            filename="sample.jpg",
            bbox_raw="{not-json",
            source="api",
        )
