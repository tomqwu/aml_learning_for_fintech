"""Tiny AML/TM Spark first-principles example.

Paste this into an Azure Databricks notebook or run in a PySpark environment.
It intentionally uses tiny in-memory data so the row movement is easy to inspect.
"""

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql import types as T


spark = SparkSession.builder.appName("aml-spark-first-principles").getOrCreate()


transaction_schema = T.StructType(
    [
        T.StructField("transaction_id", T.StringType(), False),
        T.StructField("account_id", T.StringType(), True),
        T.StructField("transaction_date", T.StringType(), False),
        T.StructField("amount_cad", T.StringType(), False),
        T.StructField("transaction_type", T.StringType(), False),
        T.StructField("status", T.StringType(), False),
        T.StructField("country_code", T.StringType(), True),
    ]
)

account_schema = T.StructType(
    [
        T.StructField("account_id", T.StringType(), False),
        T.StructField("customer_id", T.StringType(), False),
        T.StructField("effective_start_date", T.StringType(), False),
        T.StructField("effective_end_date", T.StringType(), False),
    ]
)

country_schema = T.StructType(
    [
        T.StructField("country_code", T.StringType(), False),
        T.StructField("risk_level", T.StringType(), False),
        T.StructField("effective_start_date", T.StringType(), False),
        T.StructField("effective_end_date", T.StringType(), False),
    ]
)


raw_transactions = spark.createDataFrame(
    [
        ("t1", "a1", "2022-06-01", "60.00", "WIRE", "POSTED", "IR"),
        ("t2", "a1", "2022-06-03", "50.00", "WIRE", "POSTED", "IR"),
        ("t3", "a1", "2022-06-05", "10.00", "CARD", "POSTED", "CA"),
        ("t4", "a2", "2022-06-02", "200.00", "WIRE", "POSTED", "CA"),
        ("t5", "a3", "2022-06-02", "20.00", "WIRE", "REVERSED", "IR"),
        ("t6", "a9", "2022-06-02", "80.00", "WIRE", "POSTED", "IR"),
    ],
    schema=transaction_schema,
)

account_history = spark.createDataFrame(
    [
        ("a1", "c1", "2020-01-01", "2023-01-01"),
        ("a2", "c2", "2020-01-01", "2023-01-01"),
        ("a3", "c3", "2020-01-01", "2023-01-01"),
    ],
    schema=account_schema,
)

country_risk = spark.createDataFrame(
    [
        ("IR", "HIGH", "2020-01-01", "2023-01-01"),
        ("CA", "LOW", "2020-01-01", "2023-01-01"),
    ],
    schema=country_schema,
)


tx = (
    raw_transactions.withColumn("transaction_date", F.to_date("transaction_date", "yyyy-MM-dd"))
    .withColumn("amount_cad", F.col("amount_cad").cast("decimal(18,2)"))
    .withColumn("account_id", F.upper(F.trim("account_id")))
    .withColumn("country_code", F.upper(F.trim("country_code")))
)

account_history = (
    account_history.withColumn("effective_start_date", F.to_date("effective_start_date", "yyyy-MM-dd"))
    .withColumn("effective_end_date", F.to_date("effective_end_date", "yyyy-MM-dd"))
    .withColumn("account_id", F.upper(F.trim("account_id")))
)

country_risk = (
    country_risk.withColumn("effective_start_date", F.to_date("effective_start_date", "yyyy-MM-dd"))
    .withColumn("effective_end_date", F.to_date("effective_end_date", "yyyy-MM-dd"))
    .withColumn("country_code", F.upper(F.trim("country_code")))
)


posted_wires = (
    tx.filter(F.col("status") == "POSTED")
    .filter(F.col("transaction_type") == "WIRE")
    .filter(F.col("transaction_date").between("2022-06-01", "2022-06-30"))
)

account_join_condition = (
    (F.col("t.account_id") == F.col("a.account_id"))
    & (F.col("t.transaction_date") >= F.col("a.effective_start_date"))
    & (F.col("t.transaction_date") < F.col("a.effective_end_date"))
)

orphan_accounts = posted_wires.alias("t").join(
    account_history.alias("a"),
    account_join_condition,
    "left_anti",
)

dq_orphan_accounts = orphan_accounts.withColumn("exception_type", F.lit("ORPHAN_ACCOUNT"))

valid_tx = (
    posted_wires.alias("t")
    .join(
        account_history.alias("a"),
        account_join_condition,
        "inner",
    )
    .select(
        F.col("t.transaction_id"),
        F.col("t.account_id"),
        F.col("t.transaction_date"),
        F.col("t.amount_cad"),
        F.col("t.transaction_type"),
        F.col("t.status"),
        F.col("t.country_code"),
        F.col("a.customer_id"),
    )
)

country_join_condition = (
    (F.col("t.country_code") == F.col("r.country_code"))
    & (F.col("t.transaction_date") >= F.col("r.effective_start_date"))
    & (F.col("t.transaction_date") < F.col("r.effective_end_date"))
)

high_risk_tx = (
    valid_tx.alias("t")
    .join(country_risk.alias("r"), country_join_condition, "inner")
    .filter(F.col("r.risk_level") == "HIGH")
    .select(
        F.col("t.transaction_id"),
        F.col("t.account_id"),
        F.col("t.transaction_date"),
        F.col("t.amount_cad"),
        F.col("t.country_code"),
        F.col("t.customer_id"),
        F.col("r.risk_level"),
    )
)

customer_totals = high_risk_tx.groupBy("customer_id").agg(
    F.sum("amount_cad").alias("observed_amount_cad"),
    F.count("*").alias("supporting_transaction_count"),
)

alerts = (
    customer_totals.filter(F.col("observed_amount_cad") > F.lit(100))
    .withColumn("rule_id", F.lit("TM_HIGH_RISK_WIRE_001"))
    .withColumn("rule_version", F.lit("1.0.0"))
    .withColumn("processing_month", F.lit("2022-06"))
    .withColumn(
        "alert_key",
        F.sha2(
            F.concat_ws(
                "|",
                F.col("rule_id"),
                F.col("rule_version"),
                F.col("processing_month"),
                F.col("customer_id"),
            ),
            256,
        ),
    )
)

supporting_transactions = high_risk_tx.join(
    alerts.select("alert_key", "customer_id"),
    on="customer_id",
    how="inner",
).select(
    "alert_key",
    "transaction_id",
    "customer_id",
    "account_id",
    "transaction_date",
    "amount_cad",
    "country_code",
    "risk_level",
)


reconciliation = spark.createDataFrame(
    [
        ("raw_transactions", raw_transactions.count()),
        ("posted_wires", posted_wires.count()),
        ("orphan_account_exceptions", dq_orphan_accounts.count()),
        ("valid_account_matched_posted_wires", valid_tx.count()),
        ("high_risk_posted_wires", high_risk_tx.count()),
        ("customer_totals", customer_totals.count()),
        ("alerts", alerts.count()),
    ],
    ["step_name", "row_count"],
)


print("Expected: one alert for customer c1 with observed_amount_cad = 110.00")
alerts.select(
    "alert_key",
    "rule_id",
    "rule_version",
    "processing_month",
    "customer_id",
    "observed_amount_cad",
    "supporting_transaction_count",
).show(truncate=False)

print("Expected: supporting transactions t1 and t2")
supporting_transactions.orderBy("transaction_id").show(truncate=False)

print("Expected: orphan account exception for t6")
dq_orphan_accounts.select("exception_type", "transaction_id", "account_id").show(truncate=False)

print("Expected counts: raw=6, posted_wires=4, orphan=1, valid=3, high_risk=2, totals=1, alerts=1")
reconciliation.show(truncate=False)


def latest_record_by_key(df, key_cols, order_col):
    """Example deterministic dedup helper for later experiments."""
    window = Window.partitionBy(*key_cols).orderBy(F.col(order_col).desc())
    return df.withColumn("rn", F.row_number().over(window)).filter(F.col("rn") == 1).drop("rn")
