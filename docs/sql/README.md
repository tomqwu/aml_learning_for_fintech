# SQL Learning Track

Use this folder as the SQL landing page for AML/TM analytics and validation.

Right now, the canonical SQL guide lives in the Spark track because the runnable examples use Spark SQL:

- [`../spark/spark-sql-query-basics-examples.md`](../spark/spark-sql-query-basics-examples.md)

It contains runnable Spark SQL examples for:

- `SELECT`
- `WHERE`
- null handling
- `CASE`
- string and date functions
- aggregation and `HAVING`
- joins
- CTEs
- subqueries
- window functions
- DQ checks
- reconciliation
- alert queries
- supporting transaction queries

Runnable companion notebook:

- [`../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb)

---

## What Deep SQL Learning Means Here

SQL depth is not memorizing syntax. For this repo, SQL depth means you can:

- name the grain of every query result
- predict which rows survive each filter
- explain null behavior
- explain why `WHERE` and `HAVING` are different
- prove whether a join is one-to-one, one-to-many, or many-to-many
- build DQ and reconciliation queries
- validate dashboard totals against governed tables
- explain why a query result is audit-ready or not

First-principles mental model:

```text
input rows -> joins and filters -> grouping/windowing -> output grain -> evidence
```

AML/TM example:

```text
For a high-risk wire rule, SQL is used to filter eligible transactions, join
account/customer/reference data, aggregate by customer and period, produce alert
candidates, and reconcile supporting transactions back to source rows.
```

Failure modes to practice:

- filtering on the wrong date field
- joining to latest reference data instead of point-in-time data
- multiplying rows with a many-to-many join
- counting supporting transactions as alerts
- letting null country or account keys disappear silently
- using dashboard filters that do not match the reconciliation scope

Evidence expected from SQL work:

- row counts before and after joins
- unmatched key counts
- duplicate key checks
- control totals
- expected alert keys
- supporting transaction detail
- dashboard-to-source tie-out

---

## Notebook-First Rule

Spark SQL and PySQL-style examples should be run from notebooks. Markdown should
explain concepts, expected outputs, diagrams, failure modes, and where to run the
cells.

Use the notebook first, then read the Markdown guide for explanation:

[`../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb)

---

## Future Rule

If a future non-Spark SQL topic is added, add it here instead of creating another scattered top-level document.
