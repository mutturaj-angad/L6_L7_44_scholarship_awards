"""Line-coverage tests for the assigned Lab 6 application."""

import importlib.util
from pathlib import Path
import sys

import pytest

_APP_NAME = "lab6_scholarship_awards"
_APP_SPEC = importlib.util.spec_from_file_location(
    _APP_NAME, Path(__file__).with_name("scholarship_awards.py")
)
_APP = importlib.util.module_from_spec(_APP_SPEC)
sys.modules[_APP_NAME] = _APP
_APP_SPEC.loader.exec_module(_APP)
award_amount = _APP.award_amount
is_eligible = _APP.is_eligible
application_status = _APP.application_status


@pytest.mark.parametrize(
    ("category", "marks", "income", "renewal", "expected"),
    [
        ("merit", 74, "low", False, 0),
        ("merit", 75, "low", False, 0),
        ("merit", 76, "low", False, 100),
        ("sports", 61, "high", False, 60),
        ("arts", 61, "low", True, 100),
        ("merit", 96, "low", False, 3360),
        ("merit", 96, "high", False, 2100),
        ("sports", 80, "low", True, 3200),
    ],
)
def test_award_amount_categories_rates_and_cutoffs(
    category, marks, income, renewal, expected
):
    assert award_amount(category, marks, income, renewal) == expected


@pytest.mark.parametrize(
    ("category", "marks", "income", "renewal", "error"),
    [
        ("unknown", 90, "low", False, "unknown category"),
        ("merit", -1, "low", False, "invalid marks"),
    ],
)
def test_award_amount_rejects_invalid_category_and_negative_marks(
    category, marks, income, renewal, error
):
    with pytest.raises(ValueError, match=error):
        award_amount(category, marks, income, renewal)


@pytest.mark.parametrize(
    ("attendance", "backlogs", "special", "expected"),
    [
        (74, 0, False, False),
        (75, 0, False, True),
        (100, 1, False, True),
        (100, 2, False, False),
        (0, 2, True, True),
        (100, 3, True, False),
    ],
)
def test_is_eligible_paths(attendance, backlogs, special, expected):
    assert is_eligible(attendance, backlogs, special) is expected


@pytest.mark.parametrize(
    ("days", "renewal", "paper", "expected"),
    [
        (20, False, False, "open"),
        (19, False, False, "closing"),
        (4, False, False, "closed"),
        (30, True, False, "open"),
        (29, True, False, "closing"),
        (14, True, False, "closed"),
        (30, False, True, "open"),
        (29, False, True, "closing"),
        (14, False, True, "closed"),
        (40, True, True, "open"),
    ],
)
def test_application_status_boundaries(days, renewal, paper, expected):
    assert application_status(days, renewal, paper) == expected


def test_award_amount_wrong_marks_type_raises_type_error():
    with pytest.raises(TypeError):
        award_amount("merit", None, "low", False)


def test_eligibility_wrong_attendance_type_raises_type_error():
    with pytest.raises(TypeError):
        is_eligible(None, 0, False)
