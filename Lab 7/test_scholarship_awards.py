"""Hypothesis properties and examples for the three Lab 7 functions."""

import importlib.util
import math
from pathlib import Path
import sys

import pytest
from hypothesis import given, settings, strategies as st

_APP_NAME = "lab7_scholarship_awards"
_APP_SPEC = importlib.util.spec_from_file_location(
    _APP_NAME, Path(__file__).with_name("scholarship_awards.py")
)
_APP = importlib.util.module_from_spec(_APP_SPEC)
sys.modules[_APP_NAME] = _APP
_APP_SPEC.loader.exec_module(_APP)
parse_applicant = _APP.parse_applicant
marks_average = _APP.marks_average
payable_award = _APP.payable_award

settings.register_profile("lab", max_examples=40, deadline=None)
settings.load_profile("lab")

CATEGORY = st.sampled_from(("merit", "sports", "arts"))
MARK = st.integers(min_value=0, max_value=100)


def _finite_mark_in_range(value):
    try:
        number = float(value.strip())
    except (AttributeError, ValueError):
        return False
    return math.isfinite(number) and 0 <= number <= 100


@given(CATEGORY, MARK, st.text(alphabet=" \t", max_size=5), st.text(alphabet=" \t", max_size=5))
def test_parse_applicant_valid_records_are_normalized(category, marks, left, right):
    assert parse_applicant(f"{left}{category}{right}:{marks}") == (
        category.title(), float(marks)
    )


@given(st.text().filter(lambda text: text.count(":") != 1))
def test_parse_applicant_rejects_wrong_delimiter_count(text):
    with pytest.raises(ValueError):
        parse_applicant(text)


@given(st.text().filter(lambda category: category.strip().casefold() not in {"merit", "sports", "arts"}), MARK)
def test_parse_applicant_rejects_unknown_categories(category, marks):
    with pytest.raises(ValueError):
        parse_applicant(f"{category}:{marks}")


@given(st.text().filter(lambda value: not _finite_mark_in_range(value)))
def test_parse_applicant_rejects_bad_or_out_of_range_marks(marks):
    with pytest.raises(ValueError):
        parse_applicant(f"merit:{marks}")


@pytest.mark.parametrize("marks", ("-1", "101", "nan", "inf", ""))
def test_parse_applicant_rejects_mark_boundaries(marks):
    with pytest.raises(ValueError):
        parse_applicant(f"merit:{marks}")


@given(st.text(alphabet=" \t", min_size=1, max_size=4096))
def test_parse_applicant_accepts_long_surrounding_whitespace(whitespace):
    assert parse_applicant(f"{whitespace}merit:{whitespace}100{whitespace}") == (
        "Merit", 100.0
    )


@given(st.one_of(st.none(), st.integers(), st.booleans(), st.lists(st.text()), st.dictionaries(st.text(), st.integers())))
def test_parse_applicant_rejects_non_text_values(value):
    with pytest.raises(TypeError):
        parse_applicant(value)


@given(st.lists(MARK, min_size=1, max_size=30), st.lists(st.text(alphabet=" \t", max_size=3), min_size=1, max_size=30))
def test_marks_average_matches_floor_average_and_preserves_duplicates(marks, spaces):
    spaces = (spaces + [""] * len(marks))[: len(marks)]
    csv = ",".join(f"{space}{mark}{space}" for mark, space in zip(marks, spaces))
    assert marks_average(csv) == sum(marks) // len(marks)


@given(st.text().filter(lambda text: not text.strip() or any(not item.strip().lstrip("+-").isdigit() for item in text.split(","))))
def test_marks_average_rejects_empty_or_non_integer_entries(text):
    with pytest.raises(ValueError):
        marks_average(text)


@given(st.lists(st.integers(min_value=101), min_size=1, max_size=20))
def test_marks_average_rejects_marks_above_100(marks):
    with pytest.raises(ValueError):
        marks_average(",".join(map(str, marks)))


@given(st.lists(st.integers(max_value=-1), min_size=1, max_size=20))
def test_marks_average_rejects_negative_marks(marks):
    with pytest.raises(ValueError):
        marks_average(",".join(map(str, marks)))


@given(st.one_of(st.none(), st.integers(), st.booleans(), st.lists(st.integers())))
def test_marks_average_rejects_non_text_values(value):
    with pytest.raises(TypeError):
        marks_average(value)


@given(st.integers(min_value=0, max_value=10**9), st.integers(min_value=0, max_value=10**9))
def test_payable_award_applies_multiplier_and_zero_floor(award, deduction):
    assert payable_award(f"{award}|{deduction}") == max(float(award) * 1.18 - float(deduction), 0)


@given(st.text().filter(lambda text: text.count("|") != 1))
def test_payable_award_rejects_wrong_delimiter_count(text):
    with pytest.raises(ValueError):
        payable_award(text)


@given(st.one_of(st.none(), st.integers(), st.booleans(), st.lists(st.text())))
def test_payable_award_rejects_non_text_values(value):
    with pytest.raises(TypeError):
        payable_award(value)


@given(st.sampled_from(("nan", "inf", "-inf", "-1", "1e309", "", "abc")), st.text())
def test_payable_award_rejects_invalid_award_values(award, deduction):
    with pytest.raises(ValueError):
        payable_award(f"{award}|{deduction}")


@given(st.integers(min_value=0, max_value=10**9), st.sampled_from(("nan", "inf", "-inf", "-1", "", "abc")))
def test_payable_award_rejects_invalid_deductions(award, deduction):
    with pytest.raises(ValueError):
        payable_award(f"{award}|{deduction}")


def test_payable_award_rejects_finite_amount_that_overflows_result():
    with pytest.raises(ValueError):
        payable_award("1.7e308|0")


@given(st.lists(st.lists(st.one_of(st.none(), st.integers(), st.text()), max_size=5), max_size=5))
def test_nested_collections_are_rejected_as_applicant_records(value):
    with pytest.raises(TypeError):
        parse_applicant(value)


def test_examples_from_application_readme():
    assert parse_applicant("merit:82") == ("Merit", 82.0)
    assert marks_average("72,85,90") == 82
    assert payable_award("5000|500") == 5400.0
