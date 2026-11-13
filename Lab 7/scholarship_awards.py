"""Input parsing and award calculations used in the Lab 7 exercise.

The functions accept text records. Applicant categories are merit, sports, and
arts; marks are finite values from 0 through 100. Text with invalid content
raises ValueError, while non-string Python values raise TypeError.
"""

import math


_CATEGORIES = {"merit", "sports", "arts"}


def _require_text(value, field_name):
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")


def _parse_finite_nonnegative(value, field_name):
    try:
        number = float(value.strip())
    except (AttributeError, ValueError) as error:
        raise ValueError(f"{field_name} must be a number") from error
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{field_name} must be finite and non-negative")
    return number


def parse_applicant(text):
    """Parse ``category:marks`` into a title-cased category and float mark."""
    _require_text(text, "applicant record")
    if text.count(":") != 1:
        raise ValueError("applicant record must contain exactly one ':'")
    category_text, marks_text = text.split(":")
    category = category_text.strip().casefold()
    if category not in _CATEGORIES:
        raise ValueError("category must be merit, sports, or arts")
    marks = _parse_finite_nonnegative(marks_text, "marks")
    if marks > 100:
        raise ValueError("marks must be between 0 and 100")
    return category.title(), marks


def marks_average(marks_csv):
    """Return the floor average of a CSV sequence of integer exam marks."""
    _require_text(marks_csv, "marks list")
    entries = marks_csv.split(",")
    if not marks_csv.strip() or any(not entry.strip() for entry in entries):
        raise ValueError("marks list must contain one or more integer marks")
    try:
        values = [int(entry.strip()) for entry in entries]
    except ValueError as error:
        raise ValueError("marks list must contain only integer marks") from error
    if any(mark < 0 or mark > 100 for mark in values):
        raise ValueError("each mark must be between 0 and 100")
    return sum(values) // len(values)


def payable_award(text):
    """Apply the 18% multiplier, subtract a deduction, and floor at zero."""
    _require_text(text, "award record")
    if text.count("|") != 1:
        raise ValueError("award record must contain exactly one '|' character")
    award_text, deduction_text = text.split("|")
    award = _parse_finite_nonnegative(award_text, "award")
    deduction = _parse_finite_nonnegative(deduction_text, "deduction")
    payable = award * 1.18 - deduction
    if not math.isfinite(payable):
        raise ValueError("payable award is too large to represent")
    return max(payable, 0)


def main():
    """Run the original interactive examples for each Lab 7 function."""
    print("==== Running parse_applicant ====")
    result = parse_applicant(input("Enter category:marks (e.g. merit:82): "))
    print("Category and Marks:", result)

    print("\n==== Running marks_average ====")
    result = marks_average(input("Enter marks as CSV (e.g. 72,85,90): "))
    print("Average Marks:", result)

    print("\n==== Running payable_award ====")
    result = payable_award(input("Enter award|deduction (e.g. 5000|500): "))
    print("Payable Award:", result)


if __name__ == "__main__":
    main()
