# Code Bootstrap Template

Use this template for every code-heavy notebook section.

---

## Code Bootstrap

Purpose:

```text
What this code section proves.
```

Environment:

```text
Where it runs: Databricks SQL, Spark SQL, PySpark, local shell, etc.
```

Run order:

```text
1. Run Step 0 bootstrap.
2. Run each example step in order.
3. Run validation checks.
4. Compare actual output to expected output.
```

Setup:

```text
List all tables, DataFrames, imports, files, environment variables, and assumptions.
```

Expected output:

```text
State exact counts, keys, rows, or PASS/FAIL checks.
```

Failure meaning:

```text
Explain what it means when expected output does not match actual output.
```

Runnable notebook cells:

- Cell 0: imports, SparkSession, helper assertions, and display helper.
- Cell 1: tiny public-safe input rows and explicit schemas.
- Cell 2: transformation or query being taught.
- Cell 3: deterministic display ordered by business key.
- Cell 4: validation assertions or PASS/FAIL checks.

Validation notes:

- State the exact expected count, keys, rows, and totals.
- State what failure means.
- Link the Markdown learning guide to the notebook section instead of duplicating
  runnable PySpark, Python, Spark SQL, or PySQL code in Markdown.
