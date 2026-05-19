"""Runnable PySpark DataFrame basics examples for AML/TM learning.

Run top to bottom with spark-submit or in an Azure Databricks Python notebook.
The script creates tiny in-memory data, performs basic DataFrame operations,
and validates expected results with assertions.
"""

from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql import types as T


spark = SparkSession.builder.appName("aml-pyspark-dataframe-basics").getOrCreate()


def assert_set(name, actual_rows, expected_rows):
    actual = set(actual_rows)
    expected = set(expected_rows)
    assert actual == expected, f"{name}: expected {expected}, got {actual}"


def assert_list(name, actual_rows, expected_rows):
    actual = list(actual_rows)
    expected = list(expected_rows)
    assert actual == expected, f"{name}: expected {expected}, got {actual}"


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

transactions = (
    transactions_raw.withColumn("transaction_date", F.to_date("transaction_date", "yyyy-MM-dd"))
    .withColumn("amount_cad", F.col("amount_cad").cast("decimal(18,2)"))
    .withColumn("account_id", F.upper(F.trim("account_id")))
    .withColumn("country_code", F.upper(F.trim("country_code")))
)

selected = transactions.select("transaction_id", "account_id", "amount_cad")
renamed = transactions.select(
    F.col("transaction_id").alias("txn_id"),
    F.col("account_id").alias("acct_id"),
    F.col("amount_cad").alias("amount"),
)
with_buffer = transactions.withColumn("amount_with_buffer", F.col("amount_cad") * F.lit(1.13))
with_source = transactions.withColumn("source_label", F.lit("TM_TRAINING"))
transaction_types = transactions.select("transaction_type").distinct()

posted = transactions.filter(F.col("status") == "POSTED")
posted_wires = transactions.filter(F.col("status") == "POSTED").filter(F.col("transaction_type") == "WIRE")
june_transactions = transactions.filter(
    (F.col("transaction_date") >= F.lit("2022-06-01"))
    & (F.col("transaction_date") < F.lit("2022-07-01"))
)

over_100 = transactions.filter(F.col("amount_cad") > F.lit(100))
at_least_100 = transactions.filter(F.col("amount_cad") >= F.lit(100))
missing_country = transactions.filter(F.col("country_code").isNull())
not_ca = transactions.filter(F.col("country_code") != "CA")
not_ca_or_missing = transactions.filter((F.col("country_code") != "CA") | F.col("country_code").isNull())

amount_bands = transactions.withColumn(
    "amount_band",
    F.when(F.col("amount_cad") >= 200, F.lit("LARGE"))
    .when(F.col("amount_cad") >= 100, F.lit("MEDIUM"))
    .otherwise(F.lit("SMALL")),
)

eligibility_debug = transactions.withColumn(
    "eligibility_reason",
    F.when(F.col("country_code").isNull(), F.lit("MISSING_COUNTRY"))
    .when(F.col("status") != "POSTED", F.lit("NOT_POSTED"))
    .when(F.col("transaction_type") != "WIRE", F.lit("NOT_WIRE"))
    .otherwise(F.lit("ELIGIBLE_CANDIDATE")),
)

top_3 = transactions.orderBy(F.col("amount_cad").desc(), F.col("transaction_id").asc()).limit(3)
count_by_type = transactions.groupBy("transaction_type").agg(F.count("*").alias("row_count"))
sum_by_account = transactions.groupBy("account_id").agg(F.sum("amount_cad").alias("total_amount_cad"))
account_metrics = transactions.groupBy("account_id").agg(
    F.count("*").alias("txn_count"),
    F.sum("amount_cad").alias("total_amount_cad"),
    F.avg("amount_cad").alias("avg_amount_cad"),
    F.max("amount_cad").alias("max_amount_cad"),
)
wire_metrics = transactions.groupBy("account_id").agg(
    F.sum(F.when(F.col("transaction_type") == "WIRE", F.col("amount_cad")).otherwise(F.lit(0))).alias(
        "wire_amount_cad"
    ),
    F.count(F.when(F.col("transaction_type") == "WIRE", True)).alias("wire_count"),
)
accounts_over_100 = sum_by_account.filter(F.col("total_amount_cad") > F.lit(100))

tx_with_accounts_inner = transactions.join(accounts, on="account_id", how="inner")
tx_with_accounts_left = transactions.join(accounts, on="account_id", how="left")
orphan_accounts = transactions.join(accounts, on="account_id", how="left_anti")
valid_account_transactions = transactions.join(accounts, on="account_id", how="left_semi")
tx_with_risk = transactions.join(country_risk, on="country_code", how="left")
high_risk_tx = tx_with_risk.filter(F.col("risk_level") == "HIGH")

account_sequence_window = Window.partitionBy("account_id").orderBy("transaction_date", "transaction_id")
with_sequence = transactions.withColumn("account_txn_sequence", F.row_number().over(account_sequence_window))

latest_window = Window.partitionBy("account_id").orderBy(
    F.col("transaction_date").desc(),
    F.col("transaction_id").desc(),
)
latest_by_account = transactions.withColumn("rn", F.row_number().over(latest_window)).filter(F.col("rn") == 1).drop("rn")

running_window = (
    Window.partitionBy("account_id")
    .orderBy("transaction_date", "transaction_id")
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
)
with_running_total = transactions.withColumn("running_amount_cad", F.sum("amount_cad").over(running_window))

lag_window = Window.partitionBy("account_id").orderBy("transaction_date", "transaction_id")
with_previous = transactions.withColumn("previous_amount_cad", F.lag("amount_cad").over(lag_window))
with_change = with_previous.withColumn("amount_change", F.col("amount_cad") - F.col("previous_amount_cad"))

required_field_failures = transactions.filter(
    F.col("transaction_id").isNull()
    | F.col("account_id").isNull()
    | F.col("transaction_date").isNull()
    | F.col("amount_cad").isNull()
)
invalid_country = transactions.filter(F.col("country_code").isNotNull()).join(
    country_risk,
    on="country_code",
    how="left_anti",
)
duplicate_transaction_ids = (
    transactions.groupBy("transaction_id")
    .agg(F.count("*").alias("duplicate_count"))
    .filter(F.col("duplicate_count") > 1)
)

june_posted_wires = (
    transactions.filter(F.col("status") == "POSTED")
    .filter(F.col("transaction_type") == "WIRE")
    .filter((F.col("transaction_date") >= F.lit("2022-06-01")) & (F.col("transaction_date") < F.lit("2022-07-01")))
)
valid_customer_tx = june_posted_wires.join(accounts, on="account_id", how="inner")
high_risk_customer_tx = (
    valid_customer_tx.join(country_risk, on="country_code", how="inner").filter(F.col("risk_level") == "HIGH")
)
customer_totals = high_risk_customer_tx.groupBy("customer_id").agg(
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
supporting_transactions = high_risk_customer_tx.join(
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
        ("transactions", transactions.count()),
        ("posted_wires", posted_wires.count()),
        ("valid_account_transactions", valid_account_transactions.count()),
        ("orphan_accounts", orphan_accounts.count()),
        ("high_risk_tx", high_risk_tx.count()),
        ("alerts", alerts.count()),
    ],
    ["step_name", "row_count"],
)


assert transactions_raw.count() == 8
assert transactions.count() == 8
assert selected.count() == 8
assert "txn_id" in renamed.columns
assert "amount_with_buffer" in with_buffer.columns
assert "source_label" in with_source.columns

assert_set("transaction types", [r.transaction_type for r in transaction_types.collect()], ["WIRE", "CARD", "CASH"])
assert posted.count() == 7
assert posted_wires.count() == 5
assert june_transactions.count() == 7

assert_set("over_100", [r.transaction_id for r in over_100.select("transaction_id").collect()], ["t4", "t7"])
assert_set("at_least_100", [r.transaction_id for r in at_least_100.select("transaction_id").collect()], ["t4", "t7", "t8"])
assert_set("missing_country", [r.transaction_id for r in missing_country.select("transaction_id").collect()], ["t8"])
assert "t8" not in {r.transaction_id for r in not_ca.select("transaction_id").collect()}
assert "t8" in {r.transaction_id for r in not_ca_or_missing.select("transaction_id").collect()}

assert_list("top_3", [r.transaction_id for r in top_3.select("transaction_id").collect()], ["t7", "t4", "t8"])
assert tx_with_accounts_inner.count() == 7
assert tx_with_accounts_left.count() == 8
assert tx_with_accounts_left.filter((F.col("transaction_id") == "t6") & F.col("customer_id").isNull()).count() == 1
assert_set("orphan_accounts", [r.transaction_id for r in orphan_accounts.select("transaction_id").collect()], ["t6"])
assert valid_account_transactions.count() == 7
assert_set("high_risk_tx", [r.transaction_id for r in high_risk_tx.select("transaction_id").collect()], ["t1", "t2", "t5", "t6", "t7"])

latest_pairs = {(r.account_id, r.transaction_id) for r in latest_by_account.select("account_id", "transaction_id").collect()}
assert latest_pairs == {("a1", "t3"), ("a2", "t7"), ("a3", "t5"), ("a4", "t8"), ("a9", "t6")}

assert required_field_failures.count() == 0
assert invalid_country.count() == 0
assert duplicate_transaction_ids.count() == 0
assert accounts_over_100.select("account_id").count() == 2
assert_set("accounts_over_100", [r.account_id for r in accounts_over_100.select("account_id").collect()], ["a1", "a2"])

assert alerts.count() == 1
assert_set("alert customers", [r.customer_id for r in alerts.select("customer_id").collect()], ["c1"])
assert_set(
    "supporting transaction ids",
    [r.transaction_id for r in supporting_transactions.select("transaction_id").collect()],
    ["t1", "t2"],
)

print("All PySpark DataFrame basics validation checks passed.")
print("Alerts:")
alerts.select("alert_key", "customer_id", "observed_amount_cad", "supporting_transaction_count").show(truncate=False)
print("Supporting transactions:")
supporting_transactions.orderBy("transaction_id").show(truncate=False)
print("Reconciliation:")
reconciliation.show(truncate=False)
