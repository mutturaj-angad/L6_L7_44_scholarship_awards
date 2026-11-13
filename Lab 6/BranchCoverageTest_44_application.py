"""Branch-coverage tests for the assigned Lab 6 application."""

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
        ("merit", 70, "low", False, 0),
        ("merit", 70, "low", True, 0),
        ("sports", 60, "high", True, 0),
        ("merit", 76, "low", False, 100),
        ("merit", 76, "high", False, 60),
        ("merit", 91, "low", False, 2560),
        ("merit", 91, "high", False, 1600),
        ("arts", 65, "low", False, 0),
        ("arts", 66, "low", False, 100),
    ],
)
def test_award_amount_decision_branches(category, marks, income, renewal, expected):
    assert award_amount(category, marks, income, renewal) == expected


@pytest.mark.parametrize(
    ("attendance", "backlogs", "special", "expected"),
    [
        (90, 2, True, True),
        (0, 3, True, False),
        (74, 0, False, False),
        (75, 0, False, True),
        (75, 1, False, True),
        (75, 2, False, False),
    ],
)
def test_eligibility_decision_branches(attendance, backlogs, special, expected):
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
def test_status_decision_branches(days, renewal, paper, expected):
    assert application_status(days, renewal, paper) == expected


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        (("other", 90, "low", False), "unknown category"),
        (("merit", -1, "low", False), "invalid marks"),
    ],
)
def test_award_amount_validation_branches(arguments, message):
    with pytest.raises(ValueError, match=message):
        award_amount(*arguments)


def test_sports_renewal_short_circuits_category_comparison():
    assert award_amount("sports", 61, "low", True) == 100
