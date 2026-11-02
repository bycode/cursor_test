from app.detect.stub import StubDetector


def test_stub_detector_returns_label_and_confidence(sample_image):
    dets = StubDetector().predict(sample_image)
    assert len(dets) == 1
    assert dets[0].label == "cabin"
    assert 0 <= dets[0].confidence <= 1
    assert dets[0].w is not None
