# 02 — 5-Year Lookback and Azure Modernization Study Guide

## 1. What a 5-year lookback means

A 5-year lookback means the organization reprocesses historical data over a long period to identify, validate, or remediate monitoring outcomes. In a banking context, this often means replaying customer, account, transaction, and reference data through monitoring scenarios.

A lookback is difficult because historical replay must be:

- complete
- point-in-time correct
- repeatable
- performant
- auditable
- explainable
- reconciled
- signed off

The core question is not only:

> Did we run the data?

It is:

> Can we prove what data was run, which rules ran, why outputs were created, what exceptions occurred, and how defects were resolved?

---

## 2. Generic target architecture

```text
Legacy / Source Systems
  ├─ SAS jobs
  ├─ Oracle databases
  ├─ IMS / mainframe data
  ├─ files / extracts
  └─ reference sources
        ↓
Ingestion / Orchestration
  ├─ Azure Data Factory or Fabric Data Factory
  ├─ secure connectors
  ├─ batch schedules
  └─ landing controls
        ↓
Raw / Bronze Layer
  ├─ immutable source extracts
  ├─ source metadata
  ├─ ingestion batch ID
  └─ basic landing checks
        ↓
Cleaned / Silver Layer
  ├─ standard schemas
  ├─ deduplication
  ├─ normalization
  ├─ referential checks
  └─ exception tables
        ↓
Curated / Gold Layer
  ├─ customer/account/transaction stitched views
  ├─ point-in-time reference data
  ├─ rule-ready feature tables
  └─ DQ/reconciliation metrics
        ↓
Rule Execution Layer
  ├─ Spark SQL / PySpark / SQL
  ├─ rule specs
  ├─ rule versions
  ├─ threshold parameters
  └─ test harnesses
        ↓
Alert / Evidence Layer
  ├─ alert output
  ├─ supporting transactions
  ├─ reason codes
  ├─ run logs
  ├─ reconciliation reports
  └─ business sign-off evidence
        ↓
Analytics / Review Layer
  ├─ alert dashboards
  ├─ false-positive analysis
  ├─ tuning analysis
  ├─ defect dashboards
  └─ audit reporting
```

---

## 3. Azure components to understand

### Azure Data Lake Storage Gen2 / ADLS

Study focus:

- centralized storage
- raw and curated zones
- hierarchical namespace
- ACLs and RBAC
- large-scale storage for structured and unstructured data

Practical use:

```text
/adls/landing/source=oracle/table=transactions/batch_id=...
/adls/bronze/transactions/year=2022/month=01/
/adls/silver/transactions/year=2022/month=01/
/adls/gold/tm_rule_inputs/year=2022/month=01/
```

### Azure Data Factory / Fabric Data Factory

Study focus:

- orchestration
- data movement
- pipeline dependencies
- triggers
- monitoring
- CI/CD
- linked services and datasets

Practical use:

```text
Extract Oracle data -> land file -> validate file -> run Databricks job -> publish DQ report
```

### Azure Databricks / Spark

Runnable one-stop practice: [`../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb).

Study focus:

- PySpark
- Spark SQL
- joins and aggregations
- partitioning
- Delta Lake
- job clusters
- performance tuning

Practical use:

```text
Build scalable transformations and rule execution for multi-year transaction data.
```

### Databricks Lakeflow

Study focus:

- Lakeflow Connect for managed and standard ingestion connectors
- Lakeflow Spark Declarative Pipelines for SQL/Python batch and streaming pipelines
- streaming tables, materialized views, temporary views, and flows
- expectations for data quality checks
- Lakeflow Jobs for orchestration and production monitoring
- triggered versus continuous pipeline modes
- pipeline configuration, environment parameters, and CI/CD bundles

Practical use:

```text
Ingest source extracts -> validate required keys with expectations -> transform into curated Delta tables -> run reconciliation -> orchestrate rule execution and evidence publication.
```

### Delta Lake

Study focus:

- ACID transactions
- schema enforcement
- time travel/history
- merge/upsert
- selective overwrite
- batch and streaming compatibility
- medallion architecture

Practical use:

```text
Rebuild only the transaction_month partition after a defect fix.
Use version history to investigate what changed between runs.
```

### Microsoft Fabric Lakehouse / Warehouse

Study focus:

- OneLake
- Delta format
- Spark notebooks
- SQL analytics endpoint
- Power BI integration
- lakehouse vs warehouse tradeoffs

Practical use:

```text
Use Spark for transformation and SQL/Power BI for analyst-friendly reporting.
```

### Microsoft Purview / Data lineage

Study focus:

- data catalog
- lineage graph
- source-to-target traceability
- compliance and impact analysis
- operational metadata

Practical use:

```text
Trace alert output back to curated tables, transformations, source extracts, and source systems.
```

### Azure Synapse Analytics

Study focus:

- SQL analytics
- Spark integration
- pipelines
- data lake exploration
- warehousing and BI integration

Practical use:

```text
Expose curated monitoring outputs for SQL-based analysis and dashboards.
```

---

## 4. Historical replay design patterns

### Pattern 1 — Partition by business time

For transaction monitoring, partition by business date, transaction month, or processing month.

```text
transactions/year=2021/month=09/
rule_outputs/rule_id=TM001/year=2021/month=09/
```

Why it matters:

- easier reruns
- faster queries
- simpler reconciliation
- isolated defect remediation
- cheaper backfills

### Pattern 2 — Idempotent writes

A rerun should not duplicate records.

Bad design:

```text
Every rerun appends alerts again.
```

Better design:

```text
Delete or replace target partition for batch_id/rule_id/month, then write fresh output.
```

Even better design:

```text
Use deterministic keys:
alert_key = hash(rule_id, rule_version, customer_id, account_id, window_start, window_end, reason_code)
```

### Pattern 3 — Batch ID everywhere

Every table should carry run metadata.

```text
batch_id
source_system
extract_timestamp
processing_timestamp
rule_id
rule_version
source_period_start
source_period_end
```

Batch IDs make it possible to reconstruct a run.

### Pattern 4 — Point-in-time reference data

Lookback logic must use historical values where required.

Example:

```text
Transaction date: 2021-05-10
Customer risk rating today: Low
Customer risk rating on transaction date: High
Lookback rule should use: High
```

Common point-in-time fields:

```text
effective_start_date
effective_end_date
is_current
source_update_timestamp
```

### Pattern 5 — Parallel validation

Run selected periods through both legacy and new logic, then compare:

- row counts
- alert counts
- customer counts
- total amounts
- key fields
- reason codes
- sampled supporting transactions
- excluded populations

Differences must be classified:

```text
expected difference
source data mismatch
mapping defect
rule logic defect
reference data defect
timing/window defect
legacy defect exposed by migration
```

---

## 5. Data stitching for monitoring

Data stitching means converting fragmented source records into a rule-ready view.

A simple stitched rule input might include:

```text
customer_id
customer_type
risk_rating_at_transaction_date
account_id
product_type
transaction_id
transaction_date
amount_original
currency_original
amount_base_currency
transaction_type
channel
counterparty_id
counterparty_country
country_risk_level_at_transaction_date
```

### Common stitching failures

| Failure | Why it matters |
|---|---|
| Missing customer/account link | Rule may miss eligible activity or assign alert to wrong entity. |
| Duplicate transaction | Aggregations and thresholds become inflated. |
| Late arriving record | Historical output changes after rerun. |
| Current reference data used for old transaction | Lookback becomes point-in-time incorrect. |
| Wrong currency conversion date | Amount thresholds become unreliable. |
| Many-to-many ownership ignored | Risk can be assigned to the wrong relationship. |

---

## 6. Performance study checklist

Study these Spark/SQL topics:

- partition pruning
- broadcast joins
- skewed joins
- incremental processing
- caching only when useful
- file size optimization
- avoiding small files
- predicate pushdown
- data skipping / clustering
- selective overwrite
- explain plans
- window functions
- aggregation strategy

Typical bottlenecks:

```text
1. joining huge transaction table to large account/customer tables
2. missing partition filters
3. duplicate scans of the same historical data
4. poor file layout
5. skewed customer/account keys
6. repeated currency/reference lookup joins
7. writing too many small files
```

---

## 7. Evidence created by each run

A mature lookback pipeline should produce:

```text
run_manifest
  batch_id
  source periods
  source tables
  target tables
  rule versions
  parameter versions
  code commit hash
  execution status

reconciliation_report
  source row count
  target row count
  source amount total
  target amount total
  rejected row count
  alert count
  exception count

rule_output_report
  rule_id
  rule_version
  alert count by month
  alert count by customer segment
  alert count by geography
  top reason codes

dq_report
  completeness checks
  duplicate checks
  validity checks
  referential integrity checks
  point-in-time coverage checks

defect_log
  defect_id
  severity
  root cause
  owner
  fix version
  retest evidence
```

---

## 8. Role-based learning focus

### Data engineer

- ADF/Fabric pipelines
- ADLS/OneLake layout
- Databricks/Spark jobs
- Delta Lake tables
- backfill and rerun strategy
- data quality checks
- pipeline monitoring

### Data analyst

- SQL
- data profiling
- alert dashboards
- rule validation
- reconciliation reports
- mapping documents

### QA/DQ engineer

- test cases
- DQ checks
- defect workflow
- parallel output comparison
- regression testing
- evidence packs

### Data scientist / analytics

- feature engineering
- alert prioritization
- threshold sensitivity
- false-positive analysis
- segmentation
- graph-based thinking

### Lead / architect

- target architecture
- risk/control design
- platform governance
- delivery plan
- approval model
- sign-off criteria

---

## 9. Active recall questions

Model answers: [`16-model-answer-bank.md#2-domain-foundation-answers`](16-model-answer-bank.md#2-domain-foundation-answers)

1. What makes a 5-year lookback different from normal monthly monitoring?
2. Why does partitioning matter for backfill and rerun?
3. What does idempotence mean in a data pipeline?
4. Why is batch ID important?
5. What fields are needed for point-in-time reference data?
6. What are the common failure modes in data stitching?
7. What evidence should a lookback run automatically generate?
8. How would you explain the difference between ADLS, Databricks, Delta, Fabric, Synapse, and Purview?
