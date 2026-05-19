# 07 — Annotated Bibliography and Source Map

This page lists the main sources used to shape the study pack. It is intentionally source-focused so the learning material can be checked and expanded.

Primary access dates for this pack: 2026-05-18 and 2026-05-19.

---

## 1. AML / financial crime standards and guidance

### FATF Recommendations

URL: https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html

Why it matters:

- FATF Recommendations are the global baseline for AML/CFT/CPF standards.
- Useful for understanding risk-based controls, preventive measures, beneficial ownership, international standards, and how country-level frameworks are evaluated.

How to use for study:

- Read for the overall control philosophy, not implementation code.
- Focus on risk-based approach, customer due diligence, suspicious transaction reporting, record keeping, and information sharing.

### FINTRAC — Reporting suspicious transactions to FINTRAC

URL: https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/str-dod/str-dod-eng

Why it matters:

- Authoritative Canadian guidance for suspicious transaction reporting.
- Explains reasonable grounds to suspect, no monetary threshold for suspicious transactions, facts/context/indicators, and timeliness.

How to use for study:

- Translate “facts, context, indicators” into data model fields.
- Practice explaining why a system trigger is not automatically the same as a reporting decision.

### FINTRAC — Risk assessment guidance

URL: https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/rba/rba-eng

Why it matters:

- Explains business-based and relationship-based risk assessment.
- Covers products, services, delivery channels, geography, clients, affiliates, and new technologies.

How to use for study:

- Map risk dimensions to data attributes and monitoring rules.
- Ask how each risk factor changes thresholds, segmentation, or review priority.

### FINTRAC — Compliance program requirements

URL: https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/Guide4/4-eng

Why it matters:

- Defines compliance program expectations such as written policies, risk assessment, training, review, KYC, record keeping, ongoing monitoring, and transaction reporting.

How to use for study:

- Convert compliance obligations into controls and artifacts: policies, procedures, rule specs, approvals, and evidence packs.

### FFIEC BSA/AML Manual — Suspicious Activity Reporting

URL: https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/04

Why it matters:

- U.S. banking examination guidance that discusses SAR timing, quality, supporting documentation, confidentiality, continuing activity, and board/management notification concepts.

How to use for study:

- Study the control themes: decision process, documentation, accuracy, timeliness, supporting evidence, and confidentiality.

---

## 2. Azure / data platform sources

### Microsoft Learn — Azure Data Lake Storage

URL: https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction

Why it matters:

- Explains Azure Data Lake Storage as a big-data analytics foundation, built on Blob Storage, with hierarchical namespace, security, scale, and HDFS-compatible access.

How to use for study:

- Understand why raw/bronze/silver/gold zones belong in a data lake/lakehouse.

### Microsoft Learn — Azure Data Factory

URL: https://learn.microsoft.com/en-us/azure/data-factory/introduction

Why it matters:

- Explains ADF as a managed ETL/ELT and orchestration platform for data movement and transformation.

How to use for study:

- Think of ADF/Fabric Data Factory as workflow control, not the only transformation engine.

### Microsoft Learn — Delta Lake in Azure Databricks

URL: https://learn.microsoft.com/en-us/azure/databricks/delta/

Why it matters:

- Explains Delta Lake as an optimized storage layer with ACID transactions, transaction log, schema enforcement, time travel/history, and incremental processing.

How to use for study:

- Connect Delta features to AML/TM requirements: reruns, selective overwrites, version history, and auditability.

### Microsoft Learn — Data engineering with Databricks

URL: https://learn.microsoft.com/en-us/azure/databricks/data-engineering/

Why it matters:

- Current Azure Databricks data-engineering overview.
- Explains Lakeflow as the Databricks solution for ingestion, transformation, and orchestration.
- Defines Lakeflow Connect, Lakeflow Spark Declarative Pipelines, Lakeflow Jobs, and Databricks Runtime for Apache Spark.

How to use for study:

- Use this as the first reference when interviewers ask where Lakeflow fits in Azure Databricks.
- Practice explaining the difference between ingestion, declarative pipeline transformation, and job orchestration.

### Microsoft Learn — Unity Catalog on Azure Databricks

URL: https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/

Why it matters:

- Official Azure Databricks overview for Unity Catalog.
- Explains centralized governance for data and AI assets, including access control, auditing, lineage, discovery, catalogs, schemas, tables, views, volumes, models, and functions.
- Clarifies the three-level namespace pattern: `catalog.schema.object`.
- Explains managed versus external tables and volumes.

How to use for study:

- Use this when preparing governance, security, and architecture interview answers.
- Map Unity Catalog concepts to AML/TM environments such as `aml_dev`, `aml_uat`, and `aml_prod`.
- Practice explaining how catalog permissions, lineage, and object ownership support auditability.

### Microsoft Learn — Lakeflow Declarative Pipelines

URL: https://learn.microsoft.com/en-us/azure/databricks/dlt/

Why it matters:

- Official Azure Databricks overview for Lakeflow Declarative Pipelines.
- Explains incremental batch and streaming transformations, streaming tables, materialized views, and pipeline development in SQL or Python.
- Useful for distinguishing declarative pipeline design from job orchestration.

How to use for study:

- Use it to explain how bronze-to-silver-to-gold transformations can be managed declaratively.
- Convert each pipeline concept into an AML/TM example: transaction ingestion, customer reference standardization, DQ expectations, and rule-ready feature tables.

### Databricks Docs — Lakeflow Jobs

URL: https://docs.databricks.com/data-engineering/jobs/index.html

Why it matters:

- Official Databricks documentation for Lakeflow Jobs.
- Explains workflow automation and orchestration for coordinating multiple Databricks tasks in production workloads.
- Useful for comparing Databricks-native orchestration with ADF or Fabric Data Factory.

How to use for study:

- Use it to design end-to-end AML/TM workflows with ingestion, DQ, transformations, rule execution, reconciliation, dashboard refresh, and failure handling.
- Practice explaining task dependencies, owners, monitoring, and job observability.

### Databricks Docs — Lakeflow Spark Declarative Pipelines best practices

URL: https://docs.databricks.com/aws/en/ldp/best-practices

Why it matters:

- Explains practical design choices for Lakeflow Spark Declarative Pipelines.
- Covers streaming tables, materialized views, temporary views, expectations, quarantine patterns, triggered versus continuous mode, CI/CD, and pipeline bundles.
- Useful for turning “I know Lakeflow” into operational interview answers.

How to use for study:

- Convert each best practice into an AML/TM example: required-key checks, reference-data quarantine, backfills, triggered monthly runs, and bundle-based promotion.
- Practice describing why a DQ failure should warn, quarantine, drop, or fail.

### Apache Spark — PySpark DataFrame API

URL: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html

Why it matters:

- Official API reference for PySpark DataFrames.
- Useful when preparing for Spark interview questions involving transformations, actions, joins, grouping, windows, schemas, and execution plans.

How to use for study:

- Pair the API reference with AML/TM examples such as rolling-window aggregation, point-in-time joins, deduplication, and reconciliation queries.
- Focus on explaining semantics and failure modes, not only function names.

### Apache Spark — Spark SQL and DataFrames guide

URL: https://spark.apache.org/docs/latest/sql-programming-guide.html

Why it matters:

- Official guide for Spark SQL and DataFrames.
- Explains how structured data APIs provide Spark with schema and computation information that can be optimized.
- Useful for understanding why Spark SQL and PySpark DataFrame code often share the same execution engine.

How to use for study:

- Use it as the conceptual base for [`spark/spark-sql-pyspark-deep-learning.md`](spark/spark-sql-pyspark-deep-learning.md).
- Practice translating between SQL and PySpark while preserving business logic.

### Apache Spark — Spark SQL performance tuning

URL: https://spark.apache.org/docs/latest/sql-performance-tuning.html

Why it matters:

- Official Spark performance guide for DataFrame and SQL workloads.
- Covers caching, partitioning, joins, query hints, adaptive query execution, shuffle partition behavior, and runtime optimization.

How to use for study:

- Use it for Spark interview prep on explain plans, shuffles, joins, skew, and AQE.
- Convert each tuning topic into an AML/TM example and always compare output before and after optimization.

### Delta Lake Documentation

URL: https://docs.delta.io/

Why it matters:

- Official Delta Lake documentation.
- Explains Delta Lake as adding ACID transactions, scalable metadata handling, streaming/batch unification, schema enforcement, and time travel on top of existing data lakes.

How to use for study:

- Use it when explaining why Delta is more than plain Parquet.
- Connect transaction logs, time travel, schema controls, and history to AML/TM replay, audit evidence, and controlled reruns.

### Databricks Docs — PySpark on Databricks

URL: https://docs.databricks.com/en/pyspark/index.html

Why it matters:

- Current Databricks overview for using PySpark on the Databricks platform.
- Explains DataFrames, Spark SQL, structured data processing, and related PySpark learning resources in a Databricks context.

How to use for study:

- Use it to connect general Apache Spark concepts to Databricks implementation patterns.
- Pair it with the Spark deep guide when preparing for Azure Databricks data engineering interviews.

### Microsoft Learn — Databricks Connect usage requirements

URL: https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-connect/requirements

Why it matters:

- Official Azure Databricks requirements for Databricks Connect.
- Explains workspace requirements, authentication expectations, and Python version compatibility.
- States that the compute Databricks Runtime version must be greater than or equal to the Databricks Connect package version.

How to use for study:

- Use it when setting up VS Code, local notebooks, or IDE development against Databricks compute.
- Match the local Python version and `databricks-connect` package version before debugging Spark code.

### Microsoft Learn — Install Databricks Connect for Python

URL: https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-connect/python/install

Why it matters:

- Official Azure Databricks installation guide for Databricks Connect.
- Recommends using a virtual environment for Databricks Connect.
- Notes that standalone `pyspark` conflicts with the `databricks-connect` package.

How to use for study:

- Use it as the source of truth for local Databricks Connect installation.
- Pair it with [`code/databricks-connect-local-setup.md`](code/databricks-connect-local-setup.md) for this repo's setup workflow.

### Databricks Docs — PySpark basics

URL: https://docs.databricks.com/en/pyspark/basics.html

Why it matters:

- Practical Databricks guide for common PySpark transformations.
- Covers importing functions and types, creating DataFrames, column operations, row operations, joins, aggregations, chaining calls, and saving output.

How to use for study:

- Use it for hands-on practice after reading the Spark deep guide.
- Rebuild the examples using AML/TM-style transactions, accounts, and reference data.

### Microsoft Learn — Databricks SQL on Azure Databricks

URL: https://learn.microsoft.com/en-us/azure/databricks/sql/

Why it matters:

- Explains Databricks SQL as lakehouse-based data warehousing over lake data.
- Covers SQL warehouses, dashboards, alerts, metric views, ETL, query history, and query profiling.

How to use for study:

- Use this for Data Analyst / BI interview preparation.
- Practice explaining governed metrics, dashboard validation, query tuning, and alert/reporting use cases.

### Microsoft Learn — AI and machine learning on Azure Databricks

URL: https://learn.microsoft.com/en-us/azure/databricks/machine-learning/

Why it matters:

- Current Azure Databricks overview for ML, GenAI, MLflow, model serving, Unity Catalog governance, monitoring, and MLOps workflows.
- Useful for Data Scientist interviews where AML/TM analytics must be explainable and governed.

How to use for study:

- Use it to frame ML as controlled decision support: feature engineering, experiment tracking, model registry, serving, monitoring, and governance.
- Connect model lifecycle controls to alert prioritization and false-positive analysis.

### Microsoft Learn — Microsoft Fabric Lakehouse

URL: https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview

Why it matters:

- Explains Fabric lakehouse as combining data lake scale with warehouse-style querying, Delta tables, Spark, SQL endpoint, and Power BI integration.

How to use for study:

- Understand when engineers use notebooks/Spark and analysts use SQL/Power BI over curated datasets.

### Microsoft Learn — Azure Synapse Analytics

URL: https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is

Why it matters:

- Explains Synapse as an enterprise analytics service connecting SQL, Spark, data integration, data lake analysis, and BI integration.

How to use for study:

- Compare Synapse, Fabric, and Databricks roles in modern analytics architecture.

### Microsoft Learn — Microsoft Purview data lineage

URL: https://learn.microsoft.com/en-us/purview/concept-data-lineage

Why it matters:

- Explains lineage as the lifecycle of data origin, movement, transformation, troubleshooting, DQ analysis, compliance, and impact analysis.

How to use for study:

- Translate “auditability” into concrete lineage needs for alerts and rule outputs.

---

## 3. Legacy platform sources

### IBM IMS product overview

URL: https://www.ibm.com/products/ims

Why it matters:

- Describes IMS as a high-throughput hierarchical database and transaction manager on z/OS, with Transaction Manager and Database Manager components.

How to use for study:

- Understand why IMS/mainframe data extraction may involve hierarchical relationships, batch timing, and legacy layouts.

### Oracle SQL Language Reference

URL: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/

Why it matters:

- Official Oracle SQL reference.

How to use for study:

- Use as a reference when translating Oracle SQL/stored logic into Spark SQL or cloud SQL patterns.

### SAS documentation portal

URL: https://documentation.sas.com/

Why it matters:

- SAS is frequently used in legacy analytics, reporting, and rule implementation environments.

How to use for study:

- Focus on DATA steps, PROC SQL, macros, formats, merge behavior, and date handling when reverse-engineering legacy rules.

---

## 4. Learning science sources

### Roediger and Karpicke — Test-Enhanced Learning

URL: https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x

Why it matters:

- Shows that testing/retrieval improves long-term retention more than restudy on delayed tests.

How to use for study:

- Convert every reading session into closed-book recall.

### Dunlosky et al. — Improving Students’ Learning With Effective Learning Techniques

URL: https://journals.sagepub.com/doi/10.1177/1529100612453266

Why it matters:

- Reviews multiple study techniques and rates practice testing and distributed practice highly.

How to use for study:

- Prefer active recall and spaced repetition over rereading/highlighting.

### Bjork Learning and Forgetting Lab

URL: https://bjorklab.psych.ucla.edu/research/

Why it matters:

- Explains spacing, retrieval, generation, and desirable difficulty concepts.

How to use for study:

- Make practice hard but achievable: interleave topics, delay review, and generate answers before checking notes.

---

## 5. Documentation structure and README design sources

### GitHub Docs — About the repository README file

URL: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

Why it matters:

- Explains the README as the first surfaced project document and recommends covering what the project does, why it is useful, how to get started, where to get help, and who maintains it.
- Recommends relative links for repository navigation.
- Notes that longer documentation should live outside the README.

How to use for study:

- Keep the root README as a public front door.
- Use relative links to guide learners into the deeper docs and notebooks.

### Google Documentation Guide — READMEs

URL: https://google.github.io/styleguide/docguide/READMEs.html

Why it matters:

- Defines a README as a short summary of a directory's contents.
- Recommends that package-level README files explain what is in the directory, how it is used, and where relevant documentation lives.

How to use for study:

- Keep folder README files short and navigational.
- Move deep teaching material into durable guides instead of duplicating it in folder READMEs.

### Google Documentation Guide — Documentation Best Practices

URL: https://google.github.io/styleguide/docguide/best_practices.html

Why it matters:

- Emphasizes small, fresh, accurate docs over large stale documentation sets.
- Describes a good README as orienting users to a directory and pointing to deeper guides.
- Encourages deleting or trimming dead documentation.

How to use for study:

- Treat stale handoff notes, duplicate explanations, and oversized README sections as documentation debt.
- Add lint checks when a navigation rule can be automated.

### Diátaxis

URL: https://diataxis.fr/

Why it matters:

- Provides a widely used documentation architecture based on four needs: tutorials, how-to guides, reference, and explanation.
- Helps decide whether new material belongs in a runnable notebook, a playbook, a reference page, or a conceptual guide.

How to use for study:

- Keep runnable labs under `examples/`.
- Keep first-principles explanations in deep guides.
- Keep reference and source material in dedicated reference pages.

---

## 6. Suggested expansion sources

Add these later if the repo grows:

- Wolfsberg Group publications on AML/KYC/sanctions/monitoring effectiveness.
- ACAMS educational materials for AML practitioner vocabulary.
- Cloud provider architecture guides for financial services data platforms.
- Databricks medallion architecture and performance tuning guidance.
- Academic work on graph analytics and AML alert optimization.
- Model risk management guidance if ML/AI is introduced into alert triage.

---

## 7. How to add a source to this repo

When adding a source, capture:

```text
source title
source URL
publisher/authority
access date
key points
what it changes in our mental model
which repo file should be updated
```

Do not add a source just because it sounds useful. Add it because it changes or supports a study objective.
