import pytest

from app.detect.factory import get_detector
from app.detect.stub import StubDetector


def test_factory_stub():
    assert isinstance(get_detector("stub"), StubDetector)


def test_factory_unknown():
    with pytest.raises(ValueError):
        get_detector("nope")
