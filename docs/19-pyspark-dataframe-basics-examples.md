# 19 - PySpark DataFrame Basics With Runnable AML/TM Examples

This is a step-by-step PySpark DataFrame learning guide for AML / Transaction Monitoring work.

It mirrors the Spark SQL query basics guide, but uses the PySpark DataFrame API. Every example is designed to be runnable after the setup step. The companion script runs top to bottom and includes assertions.

Companion runnable file:

- `examples/spark/aml_pyspark_dataframe_basics_examples.py`

Runnable contract:

- Run the companion Python file top to bottom in PySpark or an Azure Databricks Python notebook.
- It creates its own tiny DataFrames.
- It does not depend on private tables or paths.
- It validates expected counts, rows, and alert output with assertions.

Code Bootstrap:

```bash
spark-submit examples/spark/aml_pyspark_bootstrap.py
```

Use `examples/spark/aml_pyspark_bootstrap.py` as the shared setup for new PySpark sections. Use `examples/spark/aml_pyspark_dataframe_basics_examples.py` when you want the full setup plus all DataFrame examples.

---

## 1. Mental model

PySpark DataFrame code is table transformation code.

```text
DataFrame in -> DataFrame transformation -> DataFrame out
```

Most beginner confusion comes from forgetting three things:

1. A DataFrame is not local Python data.
2. Transformations are lazy until an action runs.
3. Each step should have an expected grain and expected count.

Example:

```text
transactions: one row per transaction
posted_wires: one row per posted wire transaction
with_customer: one row per transaction with matched customer
customer_totals: one row per customer
alerts: one row per alert
```

---

## 2. Step 0 - Create runnable tiny DataFrames

Standalone runnable in PySpark or Databricks.

```python
from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql import types as T

spark = SparkSession.builder.appName("aml-pyspark-dataframe-basics").getOrCreate()

transaction_schema = T.StructType([
    T.StructField("transaction_id", T.StringType(), False),
    T.StructField("account_id", T.StringType(), True),
    T.StructField("transaction_date", T.StringType(), False),
    T.StructField("amount_cad", T.StringType(), False),
    T.StructField("transaction_type", T.StringType(), False),
    T.StructField("status", T.StringType(), False),
    T.StructField("country_code", T.StringType(), True),
])

transactions_raw = spark.createDataFrame(
    [
        ("t1", "a1", "2022-06-01", "60.00", "WIRE", "POSTED", "IR"),
        ("t2", "a1", "2022-06-03", "50.00", "WIRE", "POSTED", "IR"),
        ("t3", "a1", "2022-06-05", "10.00", "CARD", "POSTED", "CA"),
        ("t4", "a2", "2022-06-02", "200.00", "WIRE", "POSTED", "CA"),
        ("t5", "a3", "2022-06-02", "20.00", "WIRE", "REVERSED", "IR"),
        ("t6", "a9", "2022-06-02", "80.00", "WIRE", "POSTED", "IR"),
        ("t7", "a2", "2022-07-01", "300.00", "WIRE", "POSTED", "IR"),
        ("t8", "a4", "2022-06-10", "100.00", "CASH", "POSTED", None),
    ],
    schema=transaction_schema,
)

accounts = spark.createDataFrame(
    [
        ("a1", "c1", "ACTIVE", "CHECKING"),
        ("a2", "c2", "ACTIVE", "CHECKING"),
        ("a3", "c3", "ACTIVE", "SAVINGS"),
        ("a4", "c4", "CLOSED", "CHECKING"),
    ],
    ["account_id", "customer_id", "account_status", "product_type"],
)

country_risk = spark.createDataFrame(
    [
        ("IR", "HIGH"),
        ("CA", "LOW"),
        ("US", "LOW"),
    ],
    ["country_code", "risk_level"],
)
```

Expected:

```text
transactions_raw count = 8
accounts count = 4
country_risk count = 3
```

---

## 3. Step 1 - Standardize types and keys

Runnable after Step 0.

```python
transactions = (
    transactions_raw
    .withColumn("transaction_date", F.to_date("transaction_date", "yyyy-MM-dd"))
    .withColumn("amount_cad", F.col("amount_cad").cast("decimal(18,2)"))
    .withColumn("account_id", F.upper(F.trim("account_id")))
    .withColumn("country_code", F.upper(F.trim("country_code")))
)
```

Why this matters:

```text
amount as string cannot safely support financial thresholds.
date as string can break date ranges.
keys with spaces or casing issues can break joins.
```

Validation:

```python
assert transactions.count() == 8
```

---

## 4. Step 2 - Select columns

Runnable after Step 1.

```python
selected = transactions.select("transaction_id", "account_id", "amount_cad")
selected.orderBy("transaction_id").show()
```

Expected grain:

```text
one row per transaction
```

Validation:

```python
assert selected.count() == 8
```

---

## 5. Step 3 - Rename columns

Runnable after Step 1.

```python
renamed = transactions.select(
    F.col("transaction_id").alias("txn_id"),
    F.col("account_id").alias("acct_id"),
    F.col("amount_cad").alias("amount"),
)
```

Use `alias` when selecting expressions. Use `withColumnRenamed` for simple renames.

```python
renamed_2 = transactions.withColumnRenamed("transaction_id", "txn_id")
```

---

## 6. Step 4 - Add columns with withColumn

Runnable after Step 1.

```python
with_buffer = transactions.withColumn("amount_with_buffer", F.col("amount_cad") * F.lit(1.13))
```

Constant columns:

```python
with_source = transactions.withColumn("source_label", F.lit("TM_TRAINING"))
```

Validation:

```python
assert "amount_with_buffer" in with_buffer.columns
assert "source_label" in with_source.columns
```

---

## 7. Step 5 - Distinct values

Runnable after Step 1.

```python
transaction_types = transactions.select("transaction_type").distinct()
transaction_types.show()
```

Expected:

```text
WIRE, CARD, CASH
```

Validation:

```python
actual_types = {row.transaction_type for row in transaction_types.collect()}
assert actual_types == {"WIRE", "CARD", "CASH"}
```

---

## 8. Step 6 - Filter rows

Runnable after Step 1.

```python
posted = transactions.filter(F.col("status") == "POSTED")
```

Expected:

```text
t1,t2,t3,t4,t6,t7,t8
```

Posted wires:

```python
posted_wires = (
    transactions
    .filter(F.col("status") == "POSTED")
    .filter(F.col("transaction_type") == "WIRE")
)
```

Expected:

```text
t1,t2,t4,t6,t7
```

Validation:

```python
assert posted.count() == 7
assert posted_wires.count() == 5
```

---

## 9. Step 7 - Date filters

Runnable after Step 1.

```python
june_transactions = transactions.filter(
    (F.col("transaction_date") >= F.lit("2022-06-01"))
    & (F.col("transaction_date") < F.lit("2022-07-01"))
)
```

Expected:

```text
all rows except t7
count = 7
```

Validation:

```python
assert june_transactions.count() == 7
```

Why use `< 2022-07-01` instead of `<= 2022-06-30`?

```text
It generalizes better when the field is a timestamp with times during the day.
```

---

## 10. Step 8 - Threshold filters

Runnable after Step 1.

```python
over_100 = transactions.filter(F.col("amount_cad") > F.lit(100))
at_least_100 = transactions.filter(F.col("amount_cad") >= F.lit(100))
```

Expected:

```text
over_100: t4,t7
at_least_100: t4,t7,t8
```

Validation:

```python
assert {r.transaction_id for r in over_100.select("transaction_id").collect()} == {"t4", "t7"}
assert {r.transaction_id for r in at_least_100.select("transaction_id").collect()} == {"t4", "t7", "t8"}
```

Boundary lesson:

```text
> and >= are different business rules.
```

---

## 11. Step 9 - Null handling

Runnable after Step 1.

```python
missing_country = transactions.filter(F.col("country_code").isNull())
non_missing_country = transactions.filter(F.col("country_code").isNotNull())
```

Expected:

```text
missing_country: t8
non_missing_country count: 7
```

Null trap:

```python
not_ca = transactions.filter(F.col("country_code") != "CA")
not_ca_or_missing = transactions.filter((F.col("country_code") != "CA") | F.col("country_code").isNull())
```

Expected:

```text
not_ca excludes t8 because null != "CA" is unknown.
not_ca_or_missing includes t8.
```

Validation:

```python
assert {r.transaction_id for r in missing_country.select("transaction_id").collect()} == {"t8"}
assert "t8" not in {r.transaction_id for r in not_ca.select("transaction_id").collect()}
assert "t8" in {r.transaction_id for r in not_ca_or_missing.select("transaction_id").collect()}
```

---

## 12. Step 10 - CASE logic with when/otherwise

Runnable after Step 1.

```python
amount_bands = transactions.withColumn(
    "amount_band",
    F.when(F.col("amount_cad") >= 200, F.lit("LARGE"))
     .when(F.col("amount_cad") >= 100, F.lit("MEDIUM"))
     .otherwise(F.lit("SMALL"))
)
```

Eligibility reason:

```python
eligibility_debug = transactions.withColumn(
    "eligibility_reason",
    F.when(F.col("country_code").isNull(), F.lit("MISSING_COUNTRY"))
     .when(F.col("status") != "POSTED", F.lit("NOT_POSTED"))
     .when(F.col("transaction_type") != "WIRE", F.lit("NOT_WIRE"))
     .otherwise(F.lit("ELIGIBLE_CANDIDATE"))
)
```

Expected:

```text
t5 = NOT_POSTED
t3 = NOT_WIRE
t8 = MISSING_COUNTRY
```

---

## 13. Step 11 - Order and limit

Runnable after Step 1.

```python
top_3 = transactions.orderBy(F.col("amount_cad").desc(), F.col("transaction_id").asc()).limit(3)
```

Expected:

```text
t7, t4, t8
```

Validation:

```python
assert [r.transaction_id for r in top_3.select("transaction_id").collect()] == ["t7", "t4", "t8"]
```

Tie-breaker lesson:

```text
Use deterministic secondary ordering when output order matters.
```

---

## 14. Step 12 - groupBy and aggregation

Runnable after Step 1.

Count by transaction type:

```python
count_by_type = transactions.groupBy("transaction_type").agg(F.count("*").alias("row_count"))
```

Sum by account:

```python
sum_by_account = transactions.groupBy("account_id").agg(F.sum("amount_cad").alias("total_amount_cad"))
```

Multiple aggregations:

```python
account_metrics = transactions.groupBy("account_id").agg(
    F.count("*").alias("txn_count"),
    F.sum("amount_cad").alias("total_amount_cad"),
    F.avg("amount_cad").alias("avg_amount_cad"),
    F.max("amount_cad").alias("max_amount_cad"),
)
```

Conditional aggregation:

```python
wire_metrics = transactions.groupBy("account_id").agg(
    F.sum(F.when(F.col("transaction_type") == "WIRE", F.col("amount_cad")).otherwise(F.lit(0))).alias("wire_amount_cad"),
    F.count(F.when(F.col("transaction_type") == "WIRE", True)).alias("wire_count"),
)
```

Grain lesson:

```text
Before groupBy: one row per transaction.
After groupBy("account_id"): one row per account.
```

---

## 15. Step 13 - Filter groups

Runnable after Step 12.

PySpark does not use `HAVING`; it filters after aggregation.

```python
accounts_over_100 = sum_by_account.filter(F.col("total_amount_cad") > F.lit(100))
```

Expected:

```text
a1, a2
```

Validation:

```python
assert {r.account_id for r in accounts_over_100.select("account_id").collect()} == {"a1", "a2"}
```

---

## 16. Step 14 - Inner join

Runnable after Step 1.

```python
tx_with_accounts_inner = transactions.join(accounts, on="account_id", how="inner")
```

Expected:

```text
t6 drops because account_id a9 is missing from accounts.
count = 7
```

Validation:

```python
assert tx_with_accounts_inner.count() == 7
```

---

## 17. Step 15 - Left join

Runnable after Step 1.

```python
tx_with_accounts_left = transactions.join(accounts, on="account_id", how="left")
```

Expected:

```text
all 8 transactions remain.
t6 has customer_id = null.
```

Validation:

```python
assert tx_with_accounts_left.count() == 8
assert tx_with_accounts_left.filter((F.col("transaction_id") == "t6") & F.col("customer_id").isNull()).count() == 1
```

---

## 18. Step 16 - Left anti join for DQ

Runnable after Step 1.

```python
orphan_accounts = transactions.join(accounts, on="account_id", how="left_anti")
```

Expected:

```text
t6
```

Validation:

```python
assert {r.transaction_id for r in orphan_accounts.select("transaction_id").collect()} == {"t6"}
```

Why this matters:

```text
An inner join hides bad records.
A left anti join turns missing relationships into visible DQ evidence.
```

---

## 19. Step 17 - Left semi join

Runnable after Step 1.

```python
valid_account_transactions = transactions.join(accounts, on="account_id", how="left_semi")
```

Expected:

```text
all transactions except t6
```

Validation:

```python
assert valid_account_transactions.count() == 7
```

Left semi join keeps only columns from the left DataFrame.

---

## 20. Step 18 - Reference join

Runnable after Step 1.

```python
tx_with_risk = transactions.join(country_risk, on="country_code", how="left")
```

Expected:

```text
t8 has null risk_level because country_code is null.
```

High-risk rows:

```python
high_risk_tx = tx_with_risk.filter(F.col("risk_level") == "HIGH")
```

Expected:

```text
t1,t2,t5,t6,t7
```

Validation:

```python
assert {r.transaction_id for r in high_risk_tx.select("transaction_id").collect()} == {"t1", "t2", "t5", "t6", "t7"}
```

---

## 21. Step 19 - Window row_number

Runnable after Step 1.

```python
account_sequence_window = Window.partitionBy("account_id").orderBy("transaction_date", "transaction_id")

with_sequence = transactions.withColumn(
    "account_txn_sequence",
    F.row_number().over(account_sequence_window)
)
```

Latest transaction per account:

```python
latest_window = Window.partitionBy("account_id").orderBy(F.col("transaction_date").desc(), F.col("transaction_id").desc())

latest_by_account = (
    transactions
    .withColumn("rn", F.row_number().over(latest_window))
    .filter(F.col("rn") == 1)
    .drop("rn")
)
```

Expected latest rows:

```text
a1 -> t3
a2 -> t7
a3 -> t5
a4 -> t8
a9 -> t6
```

---

## 22. Step 20 - Running total window

Runnable after Step 1.

```python
running_window = (
    Window
    .partitionBy("account_id")
    .orderBy("transaction_date", "transaction_id")
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
)

with_running_total = transactions.withColumn(
    "running_amount_cad",
    F.sum("amount_cad").over(running_window)
)
```

Expected for `a1`:

```text
t1 running total = 60
t2 running total = 110
t3 running total = 120
```

---

## 23. Step 21 - Previous value with lag

Runnable after Step 1.

```python
lag_window = Window.partitionBy("account_id").orderBy("transaction_date", "transaction_id")

with_previous = transactions.withColumn(
    "previous_amount_cad",
    F.lag("amount_cad").over(lag_window)
)
```

Difference from previous:

```python
with_change = with_previous.withColumn(
    "amount_change",
    F.col("amount_cad") - F.col("previous_amount_cad")
)
```

---

## 24. Step 22 - DQ checks

Required fields:

```python
required_field_failures = transactions.filter(
    F.col("transaction_id").isNull()
    | F.col("account_id").isNull()
    | F.col("transaction_date").isNull()
    | F.col("amount_cad").isNull()
)
```

Invalid country reference:

```python
invalid_country = (
    transactions
    .filter(F.col("country_code").isNotNull())
    .join(country_risk, on="country_code", how="left_anti")
)
```

Duplicate transaction key:

```python
duplicate_transaction_ids = (
    transactions
    .groupBy("transaction_id")
    .agg(F.count("*").alias("duplicate_count"))
    .filter(F.col("duplicate_count") > 1)
)
```

Expected:

```text
required_field_failures count = 0
invalid_country count = 0
duplicate_transaction_ids count = 0
orphan_accounts count = 1
```

---

## 25. Step 23 - Reconciliation DataFrame

Runnable after prior steps.

```python
reconciliation = spark.createDataFrame(
    [
        ("transactions", transactions.count()),
        ("posted_wires", posted_wires.count()),
        ("valid_account_transactions", valid_account_transactions.count()),
        ("orphan_accounts", orphan_accounts.count()),
        ("high_risk_tx", high_risk_tx.count()),
    ],
    ["step_name", "row_count"],
)
```

Expected:

```text
transactions = 8
posted_wires = 5
valid_account_transactions = 7
orphan_accounts = 1
high_risk_tx = 5
```

---

## 26. Step 24 - Alert generation

Rule:

```text
For June 2022, alert customers with posted WIRE transactions to HIGH-risk countries totaling more than 100 CAD.
```

Runnable after prior setup.

```python
june_posted_wires = (
    transactions
    .filter(F.col("status") == "POSTED")
    .filter(F.col("transaction_type") == "WIRE")
    .filter((F.col("transaction_date") >= F.lit("2022-06-01")) & (F.col("transaction_date") < F.lit("2022-07-01")))
)

valid_customer_tx = june_posted_wires.join(accounts, on="account_id", how="inner")

high_risk_customer_tx = (
    valid_customer_tx
    .join(country_risk, on="country_code", how="inner")
    .filter(F.col("risk_level") == "HIGH")
)

customer_totals = high_risk_customer_tx.groupBy("customer_id").agg(
    F.sum("amount_cad").alias("observed_amount_cad"),
    F.count("*").alias("supporting_transaction_count"),
)

alerts = (
    customer_totals
    .filter(F.col("observed_amount_cad") > F.lit(100))
    .withColumn("rule_id", F.lit("TM_HIGH_RISK_WIRE_001"))
    .withColumn("rule_version", F.lit("1.0.0"))
    .withColumn("processing_month", F.lit("2022-06"))
    .withColumn(
        "alert_key",
        F.sha2(F.concat_ws("|", "rule_id", "rule_version", "processing_month", "customer_id"), 256)
    )
)
```

Expected:

```text
one alert for c1 with observed_amount_cad = 110.00
```

---

## 27. Step 25 - Supporting transactions

Runnable after Step 24.

```python
supporting_transactions = (
    high_risk_customer_tx
    .join(alerts.select("alert_key", "customer_id"), on="customer_id", how="inner")
    .select(
        "alert_key",
        "transaction_id",
        "customer_id",
        "account_id",
        "transaction_date",
        "amount_cad",
        "country_code",
        "risk_level",
    )
)
```

Expected:

```text
t1 and t2
```

---

## 28. Step 26 - Validations

Runnable after all prior steps.

```python
assert transactions.count() == 8
assert posted_wires.count() == 5
assert orphan_accounts.count() == 1
assert alerts.count() == 1

alert_customers = {row.customer_id for row in alerts.select("customer_id").collect()}
assert alert_customers == {"c1"}

supporting_ids = {row.transaction_id for row in supporting_transactions.select("transaction_id").collect()}
assert supporting_ids == {"t1", "t2"}
```

If any assertion fails, do not move on. The learning value is in explaining exactly why expected output and actual output differ.

---

## 29. Translation map from SQL to PySpark

| SQL | PySpark |
|---|---|
| `SELECT a, b` | `df.select("a", "b")` |
| `WHERE a = 1` | `df.filter(F.col("a") == 1)` |
| `CASE WHEN` | `F.when(...).otherwise(...)` |
| `GROUP BY` | `df.groupBy(...)` |
| `SUM(x)` | `F.sum("x")` |
| `COUNT(*)` | `F.count("*")` |
| `JOIN` | `df.join(other, on=..., how=...)` |
| `LEFT ANTI JOIN` | `df.join(other, on=..., how="left_anti")` |
| `ROW_NUMBER() OVER` | `F.row_number().over(Window...)` |
| `ORDER BY` | `df.orderBy(...)` |
| `LIMIT` | `df.limit(...)` |

---

## 30. Closed-book drills

Answer and code without looking:

1. Create the tiny `transactions`, `accounts`, and `country_risk` DataFrames.
2. Cast `transaction_date` to date and `amount_cad` to decimal.
3. Select only `transaction_id`, `account_id`, and `amount_cad`.
4. Filter posted WIRE transactions.
5. Filter June 2022 rows using a half-open date range.
6. Find rows where `country_code` is null.
7. Show why `country_code != "CA"` excludes nulls.
8. Create an `amount_band` column.
9. Count transactions by `transaction_type`.
10. Sum transaction amount by `account_id`.
11. Filter grouped account totals above 100.
12. Inner join transactions to accounts and explain which row drops.
13. Left join transactions to accounts and show t6 remains.
14. Use left anti join to find orphan accounts.
15. Join country risk and find high-risk transactions.
16. Use `row_number` to find latest transaction per account.
17. Create DQ checks for orphan accounts and duplicate transaction IDs.
18. Build the high-risk June posted-wire alert.
19. Build supporting transactions for that alert.
20. Write assertions for every expected count and key output.
