# Spark Examples

These files are companion examples for [`../../docs/spark/first-principles-examples.md`](../../docs/spark/first-principles-examples.md) and [`../../docs/spark/spark-sql-query-basics-examples.md`](../../docs/spark/spark-sql-query-basics-examples.md).

They are written to be easy to paste into an Azure Databricks notebook or adapt into a PySpark project.

All examples follow [`../../docs/code/runnable-code-example-standards.md`](../../docs/code/runnable-code-example-standards.md):

- setup data is included
- run order is explicit
- expected output is described
- validation checks are included where practical
- no private tables, paths, or credentials are required

Files:

- `aml_pyspark_bootstrap.py` - Reusable PySpark bootstrap that creates tiny AML/TM DataFrames and validates them.
- `aml_sql_bootstrap.sql` - Reusable Spark SQL bootstrap that creates tiny AML/TM temp views and validates them.
- `aml_spark_first_principles_examples.py` - PySpark version of the tiny AML/TM rule.
- `aml_spark_first_principles_queries.sql` - Spark SQL version of the same logic.
- `aml_query_basics_examples.sql` - Runnable query-basics examples for SELECT, WHERE, joins, CTEs, windows, DQ, reconciliation, and alert queries.
- `aml_pyspark_dataframe_basics_examples.py` - Runnable PySpark DataFrame basics examples with assertions for transformations, joins, windows, DQ, and alert generation.

Expected learning flow:

1. Read the Markdown guide first.
2. Predict the output manually.
3. Run the PySpark or SQL examples.
4. Compare actual output to expected output.
5. Change one input row and predict the new result before rerunning.

## Run order

### Shared PySpark bootstrap

Run:

```bash
spark-submit examples/spark/aml_pyspark_bootstrap.py
```

Expected:

- all assertions pass
- `transactions` has 8 rows
- `accounts` has 4 rows
- `country_risk` has 3 rows

Use this file as the starting bootstrap for future PySpark learning sections.

### Shared Spark SQL bootstrap

Run `aml_sql_bootstrap.sql` top to bottom in Databricks SQL or a Spark SQL notebook.

Expected:

- `transactions`, `accounts`, and `country_risk` temp views are created
- validation query returns `PASS` rows

Use this file as the starting bootstrap for future Spark SQL learning sections.

### PySpark first-principles example

Run:

```bash
spark-submit examples/spark/aml_spark_first_principles_examples.py
```

Or paste the file into a Databricks Python notebook and run top to bottom.

Expected:

- one alert for customer `c1`
- supporting transactions `t1` and `t2`
- one orphan account exception for `t6`
- reconciliation counts: raw `6`, posted wires `4`, orphan `1`, valid account matches `3`, high-risk posted wires `2`, customer totals `1`, alerts `1`

### SQL first-principles example

Run `aml_spark_first_principles_queries.sql` top to bottom in Databricks SQL or a Spark SQL notebook.

Expected:

- `alerts` returns one row for `c1`
- `supporting_transactions` returns `t1` and `t2`
- `dq_orphan_accounts` returns `t6`

### SQL query-basics example

Run `aml_query_basics_examples.sql` top to bottom in Databricks SQL or a Spark SQL notebook.

Expected:

- setup creates `transactions`, `accounts`, and `country_risk` temp views
- each numbered query can be run independently after setup
- validation section at the end returns `PASS` rows for key expected outputs

### PySpark DataFrame basics example

Run:

```bash
spark-submit examples/spark/aml_pyspark_dataframe_basics_examples.py
```

Or paste the file into a Databricks Python notebook and run top to bottom.

Expected:

- all assertions pass
- one alert for customer `c1`
- supporting transactions `t1` and `t2`
- orphan account transaction `t6`
- printed reconciliation table shows expected row counts
