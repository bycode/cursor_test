from app.services.cabin_rule import judge_alarm_bboxes


def test_center_in_cabin_is_false_alarm():
    alarms = [{"x": 10, "y": 10, "w": 20, "h": 20, "label": "no_helmet"}]
    cabins = [{"x": 0, "y": 0, "w": 100, "h": 100, "label": "cabin"}]
    v = judge_alarm_bboxes(alarms, cabins)
    assert v[0]["verdict"] == "false_alarm"
    assert v[0]["reason"] == "in_cabin"


def test_center_outside_cabin_is_confirm():
    alarms = [{"x": 80, "y": 10, "w": 20, "h": 20, "label": "no_helmet"}]
    cabins = [{"x": 0, "y": 0, "w": 50, "h": 50, "label": "cabin"}]
    v = judge_alarm_bboxes(alarms, cabins)
    assert v[0]["verdict"] == "confirm"
    assert v[0]["reason"] == "not_in_cabin"


def test_no_cabin_is_uncertain():
    alarms = [{"x": 10, "y": 10, "w": 20, "h": 20}]
    v = judge_alarm_bboxes(alarms, [])
    assert v[0]["verdict"] == "uncertain"
    assert v[0]["reason"] == "cabin_not_found"
