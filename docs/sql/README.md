# SQL Learning Track

Use this folder for SQL learning that supports AML/TM analytics, DQ validation, reconciliation, and BI trust.

The current runnable SQL path uses Spark SQL, so the deepest examples are in the Spark track and canonical notebook.

## Start Here

| Need | Link |
|---|---|
| Spark SQL query basics guide | [`../spark/spark-sql-query-basics-examples.md`](../spark/spark-sql-query-basics-examples.md) |
| Spark SQL plus PySpark deep guide | [`../spark/spark-sql-pyspark-deep-learning.md`](../spark/spark-sql-pyspark-deep-learning.md) |
| `WHERE` vs `HAVING` and PySpark filter placement | [`../spark/where-having-filter-placement.md`](../spark/where-having-filter-placement.md) |
| When to use Spark SQL vs PySpark, with key functions | [`../spark/spark-sql-vs-pyspark-usage-guide.md`](../spark/spark-sql-vs-pyspark-usage-guide.md) |
| Canonical runnable notebook | [`../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb) |
| Data Analyst / BI role guide | [`../10-role-data-analyst-bi.md`](../10-role-data-analyst-bi.md) |

## What To Practice

| SQL skill | AML/TM use |
|---|---|
| `SELECT`, aliases, derived columns | shape analyst-ready evidence rows |
| `WHERE`, date filters, null checks | choose the correct monitoring population |
| `CASE` | encode review buckets and reason codes |
| joins | stitch transactions, accounts, customers, and reference data |
| aggregations and `HAVING` | build threshold and control-total checks |
| CTEs | make rule logic reviewable |
| window functions | deduplicate, rank, and compute running or rolling behavior |
| anti joins | find orphan records and DQ exceptions |
| reconciliation queries | prove source-to-target and legacy-to-cloud agreement |

## Deep SQL Standard

SQL depth means you can:

- name the grain of every result
- predict which rows survive each filter
- explain null behavior
- prove whether a join is one-to-one, one-to-many, or many-to-many
- validate dashboard totals against governed source tables
- explain why a query result is audit-ready or not

Mental model:

```text
input rows -> joins and filters -> grouping/windowing -> output grain -> evidence
```

## Notebook-First Rule

Spark SQL and PySQL-style examples should be run from notebooks. Markdown should explain concepts, expected outputs, diagrams, failure modes, and where to run the cells.

Use the notebook first, then read the Markdown guide for explanation:

[`../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb)

## Expansion Rule

If a future topic is ANSI SQL, Databricks SQL, Power BI semantic-model SQL, or validation SQL that is not Spark-specific, add it here. If it is Spark execution or PySpark translation, keep it under [`../spark/`](../spark/).
