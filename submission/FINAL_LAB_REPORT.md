# Final Lab Report: Code Coverage and Hypothesis Fuzz Testing

**Student:** Mutturaj Angadi

**SRN:** PES1UG24AM439

## Introduction

The repository contains Lab 6 and Lab 7 implementations of scholarship-award functionality. The supplied handouts require separate measurement of line and branch coverage in Lab 6 and Hypothesis-based input fuzzing followed by fixes in Lab 7. This report records the actual functions, observed failures, remediation, and measured results in the assigned Windows repository.

## Objectives

- Preserve the original Lab 6 award, eligibility, and status behavior while testing its meaningful paths.
- Reach and measure at least 90% line and branch coverage using coverage.py.
- Repair the Lab 7 starter test's syntax error and fuzz the three functions already present in the application.
- Fix genuine validation defects without replacing the scholarship logic.
- Preserve reproducible logs and HTML coverage reports.

## Applications and functions

Lab 6's `scholarship_awards.py` defines `award_amount`, `is_eligible`, and `application_status`. Lab 7's `scholarship_awards.py` defines `parse_applicant`, `marks_average`, `payable_award`, and the interactive `main` entry point. The Lab 7 application file already has `main`; no alternate application or invented function names were introduced.

## Lab 6 methodology and results

The dedicated line suite tests all three functions, cutoffs, rates, renewals, exceptional categories, eligibility quota paths, status transitions, validation errors, and type errors. The separate branch suite runs coverage.py with the `--branch` option and explicitly tests both outcomes of the application's conditional decisions.

| Measure | Line run | Branch run |
| --- | ---: | ---: |
| Dedicated tests passed | 28 | 28 |
| Application statements | 37 | 37 |
| Missing application statements | 0 | 0 |
| Application branches | n/a | 26 |
| Partial application branches | n/a | 0 |
| Measured application coverage | 100% line | 100% branch |

The line report totals 68 statements, 0 missing. The branch report totals 64 statements and 26 branches, with 0 missing statements and 0 partial branches. Independent raw data, command logs, text reports, and HTML reports are under `submission/lab6/reports/`.

## Lab 7 syntax repair and test methodology

The initial `test_scholarship_awards.py` contained three function definitions with no bodies. Running `py_compile` on the original Git version reproduced `IndentationError: expected an indented block after function definition on line 5 (line 7)`. This original compile output and original test source are preserved in `submission/lab7/reports/`. The actual test file was replaced with executable Hypothesis properties and a valid example test; the syntax error was fixed rather than bypassed.

Hypothesis strategies cover Unicode/arbitrary text, sampled categories, integer marks, lists, booleans, dictionaries, `None`, nested collections, boundary values, and long whitespace. Properties check expected return values and explicit validation exceptions instead of accepting arbitrary exceptions.

## Initial fuzz findings and root causes

Running the completed suite against the original application produced **14 failing tests and 10 passing tests**. Hypothesis minimized several defects:

- `parse_applicant` accepted unsupported categories and scores outside the expected 0..100 exam scale. It also returned non-finite marks such as NaN.
- The three functions called `.split()` without checking input types. `None`, lists, dictionaries, and other non-string inputs leaked `AttributeError` rather than a clear type error.
- `marks_average` accepted negative marks, values greater than 100, and non-finite-style malformed records without appropriate validation; conversion and empty entries had weak handling.
- `payable_award` accepted negative, NaN, or infinite monetary values and could overflow a finite input during its 1.18 multiplication.
- Delimiter counts were not checked explicitly, allowing low-level unpacking exceptions.

The initial failures and full original-code test output are saved in `submission/lab7/reports/initial_hypothesis_failures.txt`.

## Fixes and expected Lab 7 behavior

All three functions now require text inputs and use `TypeError` for wrong Python types. Malformed records and invalid values raise `ValueError` with field-specific messages.

1. `parse_applicant` requires exactly one colon, a category in merit/sports/arts, and finite marks in the inclusive 0..100 range. It preserves title casing and float output.
2. `marks_average` requires one or more comma-separated integer marks, disallows blank entries, and enforces the 0..100 range. It preserves duplicates and the original floor-average result.
3. `payable_award` requires exactly one pipe and finite non-negative award/deduction amounts. It preserves `max(award * 1.18 - deduction, 0)` and rejects an unrepresentable overflow result.

The application's original interactive demo remains available through `python scholarship_awards.py`.

## Final verification

- Lab 6 line-coverage suite: 28 passed; 100% line coverage (37/37 application statements).
- Lab 6 branch-coverage suite: 28 passed; 100% branch coverage (26/26 application branches).
- Lab 7 Hypothesis and example suite: 24 passed.
- Full repository `python -m pytest -v`: 26 passed.
- Lab 7 interactive application launched with the handout examples and returned the expected category, average, and payable-award outputs.
- Tests used the repository's Windows `venv` with Python 3.13.5, pytest 9.2.0, coverage.py 7.17.3, and Hypothesis 6.170.15.

The full test run and standalone Lab 7 run are recorded in `submission/lab7/reports/`. The initial and final application transcripts are also preserved there.

## Screenshots and limitations

Five supplied terminal screenshots are preserved in `submission/lab6/screenshots/`: full-suite test output, the successful Lab 7 interactive demo, a line-coverage report with the start of the branch command, and a branch-coverage report. The standalone line-coverage test execution is not shown in this screenshot set; its actual terminal output is in `submission/lab6/reports/code_coverage_execution.txt`. The separate branch test execution output is in `branch_coverage_execution.txt`. No screenshot or result was fabricated.

## Conclusion

The Lab 6 thresholds are met with separately measured 100% line and branch coverage. The original Lab 7 test syntax error is reproduced and fixed. Hypothesis exposed validation defects in the original application, the original scholarship calculations were retained, and the fixed implementation passes its property and full-repository test suites.
