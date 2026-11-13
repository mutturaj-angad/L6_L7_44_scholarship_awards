# L6_L7_44 Scholarship Awards

This repository contains two Python labs using the scholarship-awards example. Lab 6 measures line and branch coverage of its award, eligibility, and application-status functions. Lab 7 fuzzes the three existing record-processing functions with Hypothesis and hardens their input validation.

## Repository structure

| Path | Purpose |
| --- | --- |
| `Lab 6/scholarship_awards.py` | Lab 6 application |
| `Lab 6/test_scholarship_awards.py` | Original Lab 6 example tests |
| `Lab 6/CodeCoverageTest_44_application.py` | Dedicated line-coverage tests |
| `Lab 6/BranchCoverageTest_44_application.py` | Dedicated branch-coverage tests |
| `Lab 7/scholarship_awards.py` | Hardened Lab 7 application and interactive demo |
| `Lab 7/test_scholarship_awards.py` | Hypothesis fuzz tests and valid examples |
| `submission/lab6/reports/` | Coverage data, command logs, and HTML reports |
| `submission/lab6/screenshots/` | Supplied terminal captures and screenshot notes |
| `submission/lab7/reports/` | Initial failures, original source, and final run logs |
| `submission/lab7/screenshots/` | Screenshot checklist |
| `submission/FINAL_LAB_REPORT.md` | Methodology, defects, and verified results |

## Setup

Use the repository's Windows virtual environment or create a new one. Dependencies are listed in `requirements.txt`.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Verified environment: Windows, Python 3.13.5, pytest 9.2.0, coverage.py 7.17.3, and Hypothesis 6.170.15.

## Run the applications

Lab 6 is a library module, so running it defines the functions and exits without prompting:

```powershell
python 'Lab 6\scholarship_awards.py'
```

Lab 7 includes the original interactive demonstration. Run it from its folder and enter a category/marks record, a CSV marks list, and an award/deduction pair:

```powershell
Set-Location 'Lab 7'
python scholarship_awards.py
```

Example values: `merit:82`, `72,85,90`, `5000|500`.

## Test the project

Run the complete pytest suite from the repository root:

```powershell
python -m pytest -v
```

This passes **26 tests**: two original Lab 6 examples and 24 Lab 7 property/example tests. `pytest.ini` selects pytest's `importlib` mode so the two lab folders can retain the same starter test filename without an import collision.

Run just Lab 7 Hypothesis tests:

```powershell
Set-Location 'Lab 7'
python -m pytest -v test_scholarship_awards.py
```

The Lab 7 suite passes **24 tests**. It checks valid and malformed records, Unicode/arbitrary text, wrong Python types including `None`, nested collections, boundaries, whitespace, duplicates, extreme values, and numeric overflow. Hypothesis found **14 failures and 10 passes** against the original implementation; its initial minimized failures are saved in `submission/lab7/reports/initial_hypothesis_failures.txt`.

## Lab 6 line coverage

Run from `Lab 6/`. Separate coverage data paths preserve independent measurements and leave any pre-existing `.coverage` file untouched.

```powershell
$env:COVERAGE_FILE = '..\submission\lab6\reports\.coverage.line'
python -m coverage erase
python -m coverage run -m pytest -v CodeCoverageTest_44_application.py
python -m coverage report -m
python -m coverage html -d ..\submission\lab6\reports\html-code-coverage
Remove-Item Env:\COVERAGE_FILE
```

Result: **100% line coverage**. The application has 37 statements, 0 missing. The coverage report total, including the test module, is 68 statements, 0 missing.

## Lab 6 branch coverage

Run separately from `Lab 6/`:

```powershell
$env:COVERAGE_FILE = '..\submission\lab6\reports\.coverage.branch'
python -m coverage erase
python -m coverage run --branch -m pytest -v BranchCoverageTest_44_application.py
python -m coverage report -m
python -m coverage html -d ..\submission\lab6\reports\html-branch-coverage
Remove-Item Env:\COVERAGE_FILE
```

Result: **100% branch coverage**: all 26 application branches are covered, with 0 partial branches. Coverage percentages are measured using `--branch`, not inferred from line coverage.

## Lab 7 application behavior

- `parse_applicant(text)` accepts exactly one colon, a category of merit/sports/arts, and finite marks from 0 to 100 inclusive. It returns the title-cased category and a float mark.
- `marks_average(marks_csv)` accepts a non-empty CSV sequence of integer marks from 0 to 100 inclusive. It preserves duplicates and returns the floor of the average, matching the original calculation.
- `payable_award(text)` accepts exactly one pipe and finite non-negative award and deduction values. It preserves the original 18% multiplier and zero floor, and rejects a result that overflows to infinity.

Malformed textual values raise `ValueError`; non-string inputs raise `TypeError`. See `submission/FINAL_LAB_REPORT.md` for the root-cause analysis and fixes.

## Reports and screenshots

Coverage logs and HTML reports are in `submission/lab6/reports/`. Initial and final Lab 7 execution logs and the original source are in `submission/lab7/reports/`. Five supplied terminal captures are stored in `submission/lab6/screenshots/` and described in its README. The screenshot set does not include a completed dedicated Lab 6 line-coverage test run; the authentic test log is available in the reports folder.

## Submission checklist

- [x] Separate Lab 6 line- and branch-coverage suites; both exceed 90%.
- [x] Separate raw coverage data and readable HTML reports.
- [x] Lab 7 Hypothesis tests exercise all three existing functions.
- [x] Initial fuzz failures and minimized cases recorded.
- [x] Lab 7 validation fixes and expected behavior documented.
- [x] Root requirements, README, final lab report, and execution logs included.
- [x] Three local commits created in order: line coverage, branch coverage, Lab 7.
- [x] Supplied screenshots included and described; dedicated line-coverage execution screenshot remains outstanding.
