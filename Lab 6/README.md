# Lab 6: Code and Branch Coverage

The Lab 6 application is `scholarship_awards.py`; it calculates award amounts, determines eligibility, and reports application status.

The coverage suites are deliberately separate:

- `CodeCoverageTest_44_application.py` measures line coverage.
- `BranchCoverageTest_44_application.py` measures decision outcomes with coverage.py's branch instrumentation.
- `test_scholarship_awards.py` retains two original deterministic examples.

Run each suite from this folder. Use a separate `COVERAGE_FILE` for each report so the measurements stay independent and any existing `.coverage` file is preserved. Commands and HTML output paths appear in the repository root README. Current verified result is 100% line and 100% branch coverage; each dedicated suite passes 28 tests.
