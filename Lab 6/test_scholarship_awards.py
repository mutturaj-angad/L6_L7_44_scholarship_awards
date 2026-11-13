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

# Example test cases:
def test_below_cutoff_marks():
    assert award_amount("merit", 70, "low", False) == 0

def test_is_eligible():
    assert is_eligible(90, 0, False) is True

# Write the rest of the test cases so that the code is 90-100% covered.
