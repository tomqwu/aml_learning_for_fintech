# Spark Examples

This folder is notebook-first.

The old duplicated root-level `.py` and `.sql` learning examples were consolidated into notebooks so a learner can run the material directly from the learning flow.

Start here:

- [`notebooks/aml_databricks_one_stop_learning.ipynb`](notebooks/aml_databricks_one_stop_learning.ipynb) - consolidated Databricks learning path for AML/TM modernization.

Inside the canonical notebook:

- Main flow: Databricks modernization, DQ, reconciliation, alerts, Delta-style persistence, BI views, Lakeflow/Jobs thinking, and ML feature readiness.
- Step 14: Spark SQL versus PySpark tech-stack micro-lab.
- Appendix A: focused PySpark DataFrame basics.
- Appendix B: focused Spark SQL query basics through `spark.sql`.

Expected learning flow:

1. Read the related Markdown guide.
2. Open the notebook.
3. Predict the output before running each section.
4. Run all cells top to bottom.
5. Confirm the final validation cell passes.
6. Change one input row and predict the new result before rerunning.

Repo rule:

```text
Learning examples live in notebooks unless a standalone source file is truly needed.
```
