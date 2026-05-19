# Spark Learning Track

Use this folder for all Spark learning: Spark execution theory, Spark SQL, PySpark DataFrames, runnable bootstrap code, first-principles examples, DQ checks, reconciliation, and AML/TM alert-generation examples.

The point of this folder is to keep Spark in one place.

---

## Recommended Order

1. [`spark-sql-pyspark-deep-learning.md`](spark-sql-pyspark-deep-learning.md)
   - The main Spark guide: execution model, DataFrames, SQL, joins, windows, null/date pitfalls, performance, AQE, testing, and AML/TM rule patterns.

2. [`first-principles-examples.md`](first-principles-examples.md)
   - Tiny row-by-row examples showing filters, joins, DQ exceptions, groupBy, alert keys, supporting transactions, and shuffles.

3. [`spark-sql-query-basics-examples.md`](spark-sql-query-basics-examples.md)
   - Query basics for Spark SQL: `SELECT`, `WHERE`, joins, CTEs, windows, DQ, reconciliation, and alert queries.

4. [`pyspark-dataframe-basics-examples.md`](pyspark-dataframe-basics-examples.md)
   - PySpark DataFrame basics: `select`, `withColumn`, `filter`, joins, windows, DQ checks, alert generation, and assertions.

5. [`../code/runnable-code-example-standards.md`](../code/runnable-code-example-standards.md)
   - Standards for runnable code examples and required bootstraps.

---

## Runnable Code

Use [`../../examples/spark/`](../../examples/spark/) for runnable companion examples.

If you want one runnable Databricks path, start here:

- Databricks one-stop notebook: [`../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb)

Start with these bootstraps:

- PySpark: [`../../examples/spark/aml_pyspark_bootstrap.py`](../../examples/spark/aml_pyspark_bootstrap.py)
- Spark SQL: [`../../examples/spark/aml_sql_bootstrap.sql`](../../examples/spark/aml_sql_bootstrap.sql)

Then run the full examples:

- PySpark first-principles rule: [`../../examples/spark/aml_spark_first_principles_examples.py`](../../examples/spark/aml_spark_first_principles_examples.py)
- Spark SQL first-principles rule: [`../../examples/spark/aml_spark_first_principles_queries.sql`](../../examples/spark/aml_spark_first_principles_queries.sql)
- Spark SQL query basics: [`../../examples/spark/aml_query_basics_examples.sql`](../../examples/spark/aml_query_basics_examples.sql)
- PySpark DataFrame basics: [`../../examples/spark/aml_pyspark_dataframe_basics_examples.py`](../../examples/spark/aml_pyspark_dataframe_basics_examples.py)

Notebook versions:

- Databricks one-stop notebook: [`../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb)
- PySpark DataFrame notebook: [`../../examples/spark/notebooks/aml_pyspark_dataframe_basics.ipynb`](../../examples/spark/notebooks/aml_pyspark_dataframe_basics.ipynb)
- Spark SQL notebook: [`../../examples/spark/notebooks/aml_spark_sql_query_basics.ipynb`](../../examples/spark/notebooks/aml_spark_sql_query_basics.ipynb)

---

## Mental Model

```text
tiny data -> bootstrap -> one transformation -> expected output -> validation -> explanation
```

Do not skip the expected output step. Spark skill grows fastest when you can predict row counts and key rows before running the code.
