# Spark Learning Track

Use this folder for Spark execution theory, Spark SQL, PySpark DataFrames, first-principles examples, DQ checks, reconciliation, and AML/TM alert-generation patterns.

---

## Read In This Order

| Step | Link | Use it for |
|---|---|---|
| 1 | [`spark-sql-pyspark-deep-learning.md`](spark-sql-pyspark-deep-learning.md) | execution model, DataFrames, SQL, joins, windows, dates, nulls, performance, testing, AML/TM rule patterns |
| 2 | [`first-principles-examples.md`](first-principles-examples.md) | tiny row-by-row reasoning for filters, joins, DQ exceptions, alert keys, supporting transactions, and shuffles |
| 3 | [`spark-sql-query-basics-examples.md`](spark-sql-query-basics-examples.md) | Spark SQL query basics and AML/TM validation patterns |
| 4 | [`pyspark-dataframe-basics-examples.md`](pyspark-dataframe-basics-examples.md) | PySpark DataFrame basics and API translation practice |
| 5 | [`../code/runnable-code-example-standards.md`](../code/runnable-code-example-standards.md) | bootstrap, expected output, validation, and notebook-first rules |

## Run The Examples

Use the canonical notebook for runnable Spark/PySpark/SQL practice:

[`../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb)

It contains the Databricks modernization flow, Spark SQL versus PySpark micro-lab, focused PySpark appendix, and focused Spark SQL appendix.

## Folder Rule

PySpark, Python, Spark SQL, and PySQL-style examples should run from notebooks. Markdown should explain concepts, expected outputs, diagrams, Q&A, failure modes, and which notebook section to run.

When editing older Spark Markdown pages, migrate runnable snippets into the notebook instead of adding more code blocks to `.md` files.

## Mental Model

```text
tiny data -> bootstrap -> one transformation -> expected output -> validation -> explanation
```

Do not skip the expected output step. Spark skill grows fastest when you can predict row counts and key rows before running the code.
