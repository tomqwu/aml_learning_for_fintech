# Spark Notebook

This is the first-class runnable notebook for learners who prefer a notebook workflow.

Use it in Azure Databricks, Fabric notebooks with Spark, or any Jupyter environment that already has a working PySpark `SparkSession`.

Canonical notebook:

- [`aml_databricks_one_stop_learning.ipynb`](aml_databricks_one_stop_learning.ipynb) - Consolidated Databricks/Spark/PySpark/SQL learning path covering widgets, bronze/silver/gold, DQ, reconciliation, alert evidence, Delta-style persistence, Databricks SQL outputs, Lakeflow/Jobs thinking, feature readiness, the tech-stack Spark SQL versus PySpark micro-lab, focused PySpark DataFrame basics, and focused Spark SQL query basics.

Run order:

1. Open the notebook.
2. Run every cell from top to bottom.
3. Confirm the final validation cell passes.
4. Change one input row and predict the effect before rerunning.

Validation:

- The repository CI parses every checked-in `.ipynb` file.
- Python code cells are syntax checked.
- The notebook avoids private tables, private paths, credentials, and hidden setup.
