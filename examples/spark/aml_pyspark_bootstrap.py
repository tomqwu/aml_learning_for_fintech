"""Reusable PySpark bootstrap for AML/TM learning examples.

Run directly with spark-submit to verify the tiny learning data:

    spark-submit examples/spark/aml_pyspark_bootstrap.py

In a Databricks notebook, paste or import this file first, then call:

    data = create_aml_tm_dataframes(spark)
    transactions = data["transactions"]
    accounts = data["accounts"]
    country_risk = data["country_risk"]
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T


def create_spark(app_name="aml-pyspark-bootstrap"):
    return SparkSession.builder.appName(app_name).getOrCreate()


def assert_count(name, df, expected):
    actual = df.count()
    assert actual == expected, f"{name}: expected {expected}, got {actual}"


def assert_set(name, actual_rows, expected_rows):
    actual = set(actual_rows)
    expected = set(expected_rows)
    assert actual == expected, f"{name}: expected {expected}, got {actual}"


def create_aml_tm_dataframes(spark):
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

    transactions = (
        transactions_raw.withColumn("transaction_date", F.to_date("transaction_date", "yyyy-MM-dd"))
        .withColumn("amount_cad", F.col("amount_cad").cast("decimal(18,2)"))
        .withColumn("account_id", F.upper(F.trim("account_id")))
        .withColumn("country_code", F.upper(F.trim("country_code")))
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

    return {
        "transactions_raw": transactions_raw,
        "transactions": transactions,
        "accounts": accounts,
        "country_risk": country_risk,
    }


def validate_bootstrap(data):
    assert_count("transactions_raw", data["transactions_raw"], 8)
    assert_count("transactions", data["transactions"], 8)
    assert_count("accounts", data["accounts"], 4)
    assert_count("country_risk", data["country_risk"], 3)
    assert_set(
        "transaction_ids",
        [row.transaction_id for row in data["transactions"].select("transaction_id").collect()],
        ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"],
    )
    assert_set(
        "account_ids",
        [row.account_id for row in data["accounts"].select("account_id").collect()],
        ["a1", "a2", "a3", "a4"],
    )


if __name__ == "__main__":
    spark = create_spark()
    data = create_aml_tm_dataframes(spark)
    validate_bootstrap(data)
    print("AML/TM PySpark bootstrap validation passed.")
    data["transactions"].orderBy("transaction_id").show(truncate=False)
