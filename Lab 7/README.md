# Lab 7: Hypothesis Fuzz Testing

The application in `scholarship_awards.py` defines `parse_applicant`, `marks_average`, and `payable_award`, plus the original interactive `main()` demonstration. The incomplete starter test file has been repaired and now contains Hypothesis property tests and a valid example test.

From this folder, run the demo and tests:

```powershell
python scholarship_awards.py
python -m pytest -v test_scholarship_awards.py
```

The tests exercise valid and malformed inputs, Unicode text, whitespace, long values, delimiter errors, `None`, booleans, nested collections, duplicated marks, numeric boundaries, and overflow. Wrong Python types raise `TypeError`; invalid text or values raise `ValueError`. The final suite passes 24 tests. Initial failures against the buggy implementation are recorded in `../submission/lab7/reports/initial_hypothesis_failures.txt`.
