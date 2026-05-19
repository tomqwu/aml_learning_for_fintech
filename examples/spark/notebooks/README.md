# Spark Notebook Examples

These notebooks are first-class runnable examples for learners who prefer a notebook workflow.

Use them in Azure Databricks, Fabric notebooks with Spark, or any Jupyter environment that already has a working PySpark `SparkSession`.

Notebook examples:

- [`aml_pyspark_dataframe_basics.ipynb`](aml_pyspark_dataframe_basics.ipynb) - PySpark DataFrame basics with setup, filters, joins, DQ checks, alert generation, reconciliation, and assertions.
- [`aml_spark_sql_query_basics.ipynb`](aml_spark_sql_query_basics.ipynb) - Spark SQL query basics using `spark.sql`, temp views, validation checks, and an alert query.

Run order:

1. Open one notebook.
2. Run every cell from top to bottom.
3. Confirm the final validation cell passes.
4. Change one input row and predict the effect before rerunning.

Validation:

- The repository CI parses every checked-in `.ipynb` file.
- Python code cells are syntax checked.
- The notebooks avoid private tables, private paths, credentials, and hidden setup.
