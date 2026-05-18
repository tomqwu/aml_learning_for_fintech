# 07 — Annotated Bibliography and Source Map

This page lists the main sources used to shape the study pack. It is intentionally source-focused so the learning material can be checked and expanded.

Access date for this pack: 2026-05-18.

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

## 5. Suggested expansion sources

Add these later if the repo grows:

- Wolfsberg Group publications on AML/KYC/sanctions/monitoring effectiveness.
- ACAMS educational materials for AML practitioner vocabulary.
- Cloud provider architecture guides for financial services data platforms.
- Databricks medallion architecture and performance tuning guidance.
- Academic work on graph analytics and AML alert optimization.
- Model risk management guidance if ML/AI is introduced into alert triage.

---

## 6. How to add a source to this repo

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
