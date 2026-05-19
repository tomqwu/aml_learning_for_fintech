# AML Learning for Fintech: Transaction Monitoring, Azure Data Engineering, and Make-It-Stick Study System

This repository is a public-safe study pack for learning how AML / Transaction Monitoring (TM) systems are built, migrated, validated, and governed in a fintech or banking data environment. It is shaped around a realistic **5-year historical lookback** and **legacy-rule-to-cloud modernization** case study, but it intentionally avoids personal names, screenshots, private chat content, and confidential wording.

The pack is designed for active learning, not passive reading. Every topic should be converted into retrieval prompts, what-if scenarios, reverse-engineering exercises, interleaving drills, spaced-repetition review sessions, and executable artifacts.

> Working thesis: a strong AML/TM data engineer does not only build ETL. They build evidence-producing, repeatable, governed data systems that can explain why an alert was produced, which data was used, which rule version ran, which defects were found, and how output was reconciled.

---

# Codex continuation brief — read this first

This README deliberately contains the full session handoff so that Codex or another coding agent can continue the work without needing the original conversation.

## 1. User intent

The user wants a **deep research, Markdown-first learning repository** for AML / fintech / Transaction Monitoring work. The learning style must follow the principles from *Make It Stick* and related learning science:

- retrieval practice instead of passive rereading;
- spaced repetition instead of cramming;
- interleaving across domains instead of blocked study;
- elaboration and metaphor-building;
- desirable difficulty through puzzles, fill-in-the-blanks, and reverse engineering;
- mental-model-first study instead of shallow summaries;
- expert debates and deep-understanding probes;
- meeting-note-to-memory conversion.

The user explicitly corrected the direction once: they **do not want interview Q&A as the main format**. They want **study material / learning roadmap / active-recall training**.

## 2. Source context from the session

A Teams screenshot was provided. Do **not** commit the screenshot, names, or private identifiers. Use only this sanitized project context:

- Context keyword: **TD / TM CA 5-year lookback**.
- The note described an upcoming **5-year lookback project** for Transaction Monitoring.
- The team was looking to bring on **4 to 6 contractors**.
- Formal project work was expected to begin in **July**, while preliminary activities had already started.
- Contractors were desired within the next couple of months to allow onboarding and preparation.
- Main objective: **replicate TM SAS / Oracle / IMS rules on Azure**.
- Also required: **data stitching** to transform raw data.
- Additional emphasis: **data quality**, **defect management**, and a significant **analytics component** in both the preparatory phase and after alert generation.
- Desired skill mix: **data engineering** plus **data science / analytics**.
- Internal prep note also mentioned: read shared analysis, prepare for meeting, get **Microsoft Fabric certification readiness**, and learn **data engineering**.

Treat this as a **case-study seed**, not as an official client statement. Keep the public repo sanitized.

## 3. Repository status from this session

Target GitHub repo:

```text
https://github.com/tomqwu/aml_learning_for_fintech
```

Observed state during the session:

- Repo exists.
- Owner: `tomqwu`.
- Visibility: public.
- Default branch: `main`.
- Size: `0` at the time of inspection.
- The GitHub connector reported `admin: true` and `push: true` permissions.
- The repo was uninitialized at the time of inspection.

Important limitation: the available ChatGPT GitHub connector in this session exposed read/search/fetch/list operations, but no create/update/commit/write operation. Normal `git push` from the container also could not be completed. Therefore, artifacts were packaged locally and a helper push script was created.

GitHub REST supports creating or updating repository files through the repository contents API, but that requires appropriate token permissions, specifically contents write permission; workflow file edits require workflow write permission as well. See source ledger below.

## 4. Push instructions for a local or Codex environment

The artifact includes:

```text
scripts/push_to_github.sh
```

A local push can be done with:

```bash
unzip aml_learning_for_fintech_deep_research_codex_handoff.zip
cd aml_learning_for_fintech
bash scripts/push_to_github.sh .
```

If Codex has GitHub credentials in its environment, it should initialize the repo, add all files, commit, and push to `main`.

Suggested commit message:

```text
Initial AML fintech learning pack with Codex handoff
```

## 5. Public-safety and privacy constraints

This repo is for **defensive compliance, data engineering, and governance learning**.

Do:

- Use official / primary sources where possible.
- Keep all AML content defensive and compliance-oriented.
- Build learning artifacts: retrieval tests, study plans, rubrics, YAML specs, SQL DQ templates, synthetic examples.
- Sanitize client/project references.
- Emphasize auditability, lineage, controls, quality, and reproducibility.

Do not:

- Commit the original screenshot.
- Include personal names from the screenshot.
- Represent the internal note as an official TD statement.
- Provide evasion guidance, bypass techniques, or advice on hiding suspicious activity.
- Add real customer data, real bank data, production credentials, or proprietary rule logic.
- Overfocus on interview Q&A. Q&A can exist, but the repository should primarily be a **study and retrieval system**.

---

# Current repository map

| File | Purpose |
|---|---|
| [`docs/00-research-map.md`](docs/00-research-map.md) | Deep research map, field consensus, expert disagreements, and mental models. |
| [`docs/01-aml-transaction-monitoring-foundations.md`](docs/01-aml-transaction-monitoring-foundations.md) | AML/TM domain foundations: STR/SAR concepts, risk-based approach, alerts, KYC, scenarios, and case workflow. |
| [`docs/02-5year-lookback-azure-modernization.md`](docs/02-5year-lookback-azure-modernization.md) | Technical study guide for a 5-year TM lookback on Azure/Fabric/Databricks. |
| [`docs/03-rule-migration-spec-as-code.md`](docs/03-rule-migration-spec-as-code.md) | How to migrate legacy SAS/Oracle/IMS-style rules into governed specs, tests, and cloud pipelines. |
| [`docs/04-data-quality-reconciliation-defect-management.md`](docs/04-data-quality-reconciliation-defect-management.md) | Data quality, reconciliation, defect lifecycle, evidence packs, and control reporting. |
| [`docs/05-make-it-stick-study-system.md`](docs/05-make-it-stick-study-system.md) | Active recall, spaced repetition, interleaving, elaboration, desirable difficulty, and Feynman-style study plan. |
| [`docs/06-practice-lab-retrieval-tests.md`](docs/06-practice-lab-retrieval-tests.md) | Retrieval tests, what-if cases, reverse-engineering labs, and scoring rubrics. |
| [`docs/07-annotated-bibliography.md`](docs/07-annotated-bibliography.md) | Source list and why each source matters. |
| [`docs/08-interview-knowledge-by-role-and-tech-stack.md`](docs/08-interview-knowledge-by-role-and-tech-stack.md) | Interview-prep index by role and tech stack. |
| [`docs/09-role-data-engineer.md`](docs/09-role-data-engineer.md) | One-stop Data Engineer guide with theory, diagrams, stack knowledge, Q&A, and drills. |
| [`docs/10-role-data-analyst-bi.md`](docs/10-role-data-analyst-bi.md) | One-stop Data Analyst / BI guide with metric theory, dashboard diagrams, SQL reasoning, Q&A, and drills. |
| [`docs/ml/README.md`](docs/ml/README.md) | ML and Data Science learning track: regulated ML theory, feature engineering, leakage, explainability, MLflow/MLOps, Q&A, and drills. |
| [`docs/12-role-qa-dq-engineer.md`](docs/12-role-qa-dq-engineer.md) | One-stop QA / DQ Engineer guide with DQ theory, golden records, reconciliation, defects, diagrams, Q&A, and drills. |
| [`docs/13-role-solution-architect-lead.md`](docs/13-role-solution-architect-lead.md) | One-stop Solution Architect / Lead guide with reference architecture, roadmap, governance, NFRs, diagrams, Q&A, and drills. |
| [`docs/14-tech-stack-reference.md`](docs/14-tech-stack-reference.md) | One-stop tech-stack reference for Azure, Databricks, PySpark, Delta Lake, Lakeflow, BI, MLflow/MLOps, and legacy migration. |
| [`docs/spark/README.md`](docs/spark/README.md) | Spark learning track: Spark execution, PySpark, Spark SQL, first-principles examples, DQ, reconciliation, performance, and runnable examples. |
| [`docs/sql/README.md`](docs/sql/README.md) | SQL landing page that points to the canonical Spark SQL query-basics guide. |
| [`docs/code/README.md`](docs/code/README.md) | Runnable code standards and bootstrap pattern. |
| [`docs/code/databricks-connect-local-setup.md`](docs/code/databricks-connect-local-setup.md) | Local Databricks Connect setup for VS Code and notebook development. |
| [`examples/spark/`](examples/spark/) | Notebook-first Databricks-style PySpark and Spark SQL practice for the first-principles Spark guide. |
| [`examples/spark/notebooks/`](examples/spark/notebooks/) | First-class notebook examples, including the consolidated Databricks one-stop notebook. |
| [`templates/code_bootstrap_template.md`](templates/code_bootstrap_template.md) | Template for starting every code-heavy learning section with environment, setup, tiny data, expected output, and validation. |
| [`templates/rule_spec_template.yaml`](templates/rule_spec_template.yaml) | YAML-style rule specification template. |
| [`templates/dq_check_template.md`](templates/dq_check_template.md) | Markdown template with SQL blocks for DQ and reconciliation checks. |
| [`templates/retrieval_session_template.md`](templates/retrieval_session_template.md) | One-session active recall template. |
| [`templates/meeting_to_memory_converter.md`](templates/meeting_to_memory_converter.md) | Meeting-to-memory template for converting notes into application tests. |
| [`scripts/push_to_github.sh`](scripts/push_to_github.sh) | Helper script for pushing this pack into the target GitHub repository. |

---

# Working case study

Use this case study throughout the repo:

> A large financial institution is running a 5-year historical lookback for Transaction Monitoring. Legacy TM rules currently exist across SAS, Oracle, IMS, batch jobs, SQL, and undocumented business logic. The target is to replicate or modernize those rules on Azure / Fabric / Databricks while preserving explainability, data lineage, reconciliation, defect management, and audit evidence. The project needs data engineering, data quality, analytics, and data science capability.

The core pipeline:

```text
Legacy TM Rules
SAS / Oracle / IMS / SQL / Batch
        ↓
Rule inventory and source-to-target mapping
        ↓
5-year raw data ingestion into Azure
        ↓
Customer + account + transaction + reference-data stitching
        ↓
DQ checks and historical completeness validation
        ↓
Azure / Fabric / Databricks rule implementation
        ↓
Alert generation
        ↓
Parallel run / reconciliation against legacy outputs
        ↓
Defect triage and remediation
        ↓
Post-alert analytics and evidence pack
        ↓
Business / audit / compliance sign-off
```

---

# Core study domains

## Domain 1 — AML / Transaction Monitoring foundations

Minimum concepts:

- AML: Anti-Money Laundering.
- CFT: Countering the Financing of Terrorism.
- CPF: Countering Proliferation Financing.
- TM: Transaction Monitoring.
- KYC / CDD / EDD.
- Customer risk rating.
- Beneficial ownership.
- Sanctions and high-risk jurisdictions.
- Scenario / rule.
- Threshold.
- Alert.
- Case.
- SAR / STR.
- False positive.
- Lookback.
- Risk-based approach.

Key learning point:

> AML/TM is a risk-based control system, not just a detection algorithm.

## Domain 2 — Legacy rule replication

The project context specifically says **replicate TM SAS / Oracle / IMS rules on Azure**.

Study workflow:

```text
1. Rule inventory
2. Source-system inventory
3. Rule logic extraction
4. Source-to-target mapping
5. Assumption log
6. Rule spec creation
7. Azure implementation
8. Unit testing
9. Parallel run
10. Reconciliation
11. Defect management
12. Sign-off evidence
```

For every rule, capture:

| Area | Example |
|---|---|
| Rule ID | `TM_HRC_WIRE_001` |
| Owner | Financial crime / compliance / analytics owner |
| Inputs | transactions, accounts, customers, country reference |
| Joins | customer-account-transaction relationships |
| Filters | active accounts, wire transactions, non-internal accounts |
| Time window | 7 days, 30 days, 90 days, 12 months |
| Aggregation | sum amount, count transactions, distinct counterparties |
| Threshold | amount > X, count > Y |
| Output | alert ID, customer ID, rule ID, trigger amount |
| Exceptions | test accounts, internal accounts, closed accounts |
| Validation | expected output, legacy comparison, tolerances |
| Evidence | batch ID, version, reconciliation, approvals |

## Domain 3 — Azure / Fabric data engineering

Target architecture:

```text
Source Systems
SAS / Oracle / IMS / Flat Files / Mainframe extracts
        ↓
Ingestion / Orchestration
Azure Data Factory / Fabric Data Factory / Databricks Workflows
        ↓
Raw / Bronze
ADLS Gen2 / OneLake / Delta
        ↓
Cleaned / Silver
Standardized customer, account, transaction, reference data
        ↓
Curated / Gold
Rule-ready views and stitched monitoring data model
        ↓
Rule Engine
Spark SQL / PySpark / SQL / Spec-as-code compiler
        ↓
Alert Outputs
Lakehouse / Warehouse / Case-system interface
        ↓
Analytics and Evidence
Power BI / notebooks / audit pack / lineage reports
```

Study Microsoft services:

- Azure Data Lake Storage Gen2.
- Azure Data Factory.
- Azure Databricks and Delta Lake.
- Microsoft Fabric Lakehouse.
- Synapse Analytics where relevant.
- Microsoft Purview lineage / catalog.
- Azure Monitor / Log Analytics.
- Azure DevOps / GitHub.
- Key Vault.

## Domain 4 — 5-year historical lookback

A lookback is hard because of:

- historical data volume;
- changing schemas;
- missing reference data;
- point-in-time customer/account relationships;
- changing customer risk ratings;
- late-arriving or corrected transactions;
- batch restart/replay requirements;
- performance tuning;
- reconciliation against legacy output;
- audit evidence.

Key concept:

> A 5-year lookback is historical replay plus proof.

Study patterns:

- partition by business date / transaction month;
- idempotent writes;
- checkpointed pipeline runs;
- backfill by month or quarter;
- point-in-time reference joins;
- control totals;
- exception tables;
- run manifests;
- output comparison reports;
- sign-off packs.

## Domain 5 — Data stitching

Data stitching means connecting raw records from multiple systems into a rule-ready monitoring model.

Example entities:

```text
Customer
  customer_id
  risk_rating
  KYC attributes
  beneficial owner relationships

Account
  account_id
  customer_id
  product_type
  status
  open_date
  close_date

Transaction
  transaction_id
  account_id
  amount
  currency
  transaction_date
  counterparty
  country

Reference data
  country risk list
  currency table
  product table
  transaction type table
  sanctions/high-risk indicators

Alert
  alert_id
  rule_id
  customer_id
  trigger_date
  trigger_amount
  batch_id
```

Critical issue:

> Point-in-time correctness means using the customer/account/reference-data state that was true at the transaction date, not only the latest state.

## Domain 6 — Data quality, reconciliation, and defect management

DQ categories:

| Category | Meaning | Example |
|---|---|---|
| Completeness | Required values exist | missing customer ID |
| Validity | Values follow rules | invalid country code |
| Accuracy | Target matches source | amount mismatch |
| Consistency | Data agrees across systems | account exists but customer missing |
| Uniqueness | No duplicate business keys | duplicate transaction ID |
| Timeliness | Data arrives when expected | late batch file |
| Referential integrity | Parent records exist | transaction account not in account table |
| Reconciliation | Totals match between layers | row count / amount mismatch |

Defect categories:

- source data issue;
- mapping issue;
- transformation issue;
- rule logic issue;
- reference data issue;
- environment/access issue;
- performance issue;
- reconciliation issue;
- documentation/assumption issue.

Defect lifecycle:

```text
Detected → Logged → Triaged → Assigned → Root cause identified → Fixed → Retested → Evidence attached → Closed
```

## Domain 7 — Analytics and data science

Preparatory analytics:

- profile 5 years of transaction data;
- measure missingness and coverage;
- identify outliers;
- estimate alert volumes;
- evaluate threshold sensitivity;
- understand rule input availability;
- compare historical distributions by year/month/customer segment.

Post-alert analytics:

- alert counts by rule, month, segment, product, country;
- false-positive analysis;
- rule overlap;
- high-volume customers;
- scenario effectiveness;
- alert aging;
- investigator outcome analysis;
- precision/recall style evaluation where labeled outcomes exist;
- graph/relationship features where appropriate.

Practical position:

> Deterministic rules are the controlled baseline. Analytics and ML can help profile, prioritize, tune, and triage, but must remain explainable and governed.

## Domain 8 — Controls, governance, and spec-as-code

Governance should be executable:

- rule specs in YAML or structured metadata;
- source-to-target mappings in version control;
- DQ checks as SQL/tests;
- rule thresholds versioned and approved;
- evidence packs generated from pipeline logs;
- output lineage traceable from alert back to source records;
- CI/CD and promotion controls;
- batch IDs and run manifests;
- audit-friendly documentation.

Spec-as-code mental model:

```yaml
rule_id: TM_HRC_WIRE_001
rule_name: High Risk Country Wire Transfer
owner: Financial Crime Risk
version: 1.0

input_tables:
  - transactions
  - accounts
  - customers
  - country_risk_reference

logic:
  transaction_type: WIRE
  country_risk_level: HIGH
  aggregation_key: customer_id
  lookback_window_days: 30
  threshold_amount: 10000

output:
  - customer_id
  - account_id
  - total_amount
  - transaction_count
  - rule_id
  - alert_date

controls:
  dq_checks:
    - customer_id_not_null
    - account_id_not_null
    - transaction_amount_positive
    - valid_country_code
  reconciliation:
    - source_target_row_count
    - source_target_amount_total
    - legacy_vs_azure_alert_count
```

---

# Five expert mental models

## 1. AML/TM is a risk-based control system, not just a detection engine

Transaction monitoring is part of a broader financial crime control environment. Rules, alerts, cases, risk ratings, KYC data, sanctions indicators, investigation outcomes, and reporting obligations all interact. A rule that detects unusual activity but cannot support review, explanation, and control evidence is incomplete.

## 2. A lookback project is historical replay plus proof

A 5-year lookback is not only “run five years of data.” It requires historical completeness, point-in-time reference data, replayable pipelines, documented assumptions, output reconciliation, defect resolution, and sign-off evidence.

## 3. Every alert is a data lineage problem

An alert is not just a row in an output table. It should be traceable to customer data, account data, transactions, reference data, rule version, threshold, aggregation window, batch run, and exception handling.

## 4. Legacy migration is an equivalence problem before it is a modernization problem

When old SAS/Oracle/IMS-style logic is moved to Azure, the first goal is usually to prove that the new output is equivalent to the legacy output. Only after that should the team tune, optimize, or modernize rule behavior.

## 5. Governance is executable

Good governance should not live only in slide decks. Rule specs, DQ checks, mappings, thresholds, approvals, test cases, evidence packs, and deployment controls can be represented as versioned artifacts.

---

# Three places experts disagree

## Debate 1 — Rule-based monitoring vs ML/AI-assisted monitoring

**Rule-based side:** deterministic scenarios are explainable, auditable, easier to validate, and easier for investigators to understand. They fit regulated environments where reason codes, thresholds, and policy ownership matter.

**ML/AI side:** financial crime patterns evolve, rule-only systems can create large false-positive volumes, and graph/behavioral analytics can uncover patterns not captured by simple thresholds.

**Practical synthesis:** use deterministic rules as the controlled baseline; use analytics to profile, prioritize, tune, explain, and triage. Avoid opaque models where the control process cannot explain outcomes.

## Debate 2 — Exact replication vs transformation during migration

**Exact replication side:** regulators, auditors, and business owners need confidence that the migrated system preserves prior behavior. Parallel-run comparison is simpler when outputs are expected to match.

**Modernization side:** copying old defects into a new platform wastes the opportunity to reduce false positives, improve data quality, and adopt better designs.

**Practical synthesis:** separate phases. First prove equivalence; then introduce governed changes with impact analysis and approval.

## Debate 3 — Centralized lakehouse vs specialized compliance platform

**Lakehouse side:** a unified data platform improves lineage, scale, replayability, analytics, and shared controls across domains.

**Specialized platform side:** AML vendors often include scenario libraries, case-management integration, model governance, investigator workflows, and regulatory reporting features.

**Practical synthesis:** use a governed data platform for ingestion, transformation, replay, and analytics; integrate with specialized AML/case platforms where workflow and reporting requirements demand it.

---

# Ten deep-understanding probes

Answer these with the files closed. A memorizer will give definitions; a practitioner will explain tradeoffs, failure modes, and evidence.

1. Why is a 5-year lookback harder than a normal monthly batch run?
2. What does point-in-time correctness mean, and how can a lookback fail without it?
3. Why is a generated alert a lineage problem?
4. What must be captured in a rule specification so that business, engineering, QA, and audit can all use it?
5. How would you prove that an Azure implementation of a legacy rule is equivalent to the old implementation?
6. When is an alert-count mismatch acceptable, and when is it a defect?
7. Why can data quality checks create a false sense of security if they only check row counts?
8. How should defects be classified so that root cause is clear?
9. What role should analytics play before rule execution and after alert generation?
10. Why is “we built the pipeline” not enough evidence in a regulated AML/TM project?

---

# Make-It-Stick learning system to preserve

The user provided seven reusable prompt patterns. Preserve them as templates and use them to generate future study artifacts.

## 1. Active Recall Architect

Convert any article or text into open-ended self-testing prompts. Do not provide answers first. After the learner answers, grade the response and explain gaps.

Repository use:

- turn each section into 5 challenging questions;
- create `retrieval_tests/*.md` if expanding the repo;
- include scoring rubrics.

## 2. Spaced Repetition Strategist

Create a 30-day review schedule for a skill or concept. Each session should include a 3-minute quick-fire retrieval drill.

Repository use:

- create `study_plans/30_day_tm_lookback_schedule.md`;
- include review days such as Day 1, 2, 4, 7, 14, 21, 30;
- combine flashcard-style and scenario-style retrieval.

## 3. Interleaving Engine

Mix topics to build tool-selection skill. For this repo, interleave:

- AML/TM domain logic;
- Azure data engineering;
- data quality / reconciliation;
- analytics / data science;
- governance / audit evidence.

Repository use:

- create practice sessions where the learner must switch between SQL, architecture, rule interpretation, DQ triage, and analytics.

## 4. Elaboration Specialist

Force the learner to connect new concepts to what they already understand.

Repository use:

- metaphors: rule engine as a factory, data lineage as a receipt chain, DQ as quality control, alert as a legal/audit claim, lookback as a time-machine replay.

## 5. Desirable Difficulty Designer

Make study harder in productive ways.

Repository use:

- fill-in-the-blank YAML specs;
- broken SQL DQ checks;
- reverse-engineer a rule from output;
- find defects in a fake reconciliation report;
- compare two rule specs and identify hidden differences.

## 6. Mental Model Refiner

Use Feynman-style explanations. Explain complex ideas in simple language, then ask the learner to explain back. If the answer is too jargon-heavy, force simplification.

Repository use:

- create simple explanations for point-in-time correctness, reconciliation, rule equivalence, and lineage.

## 7. Meeting-to-Memory Converter

Turn meeting notes into retrieval tests, especially what-if scenarios.

Repository use:

- every meeting summary should become 5 application scenarios;
- avoid passive summaries.

---

# Daily study loop

Do not read this repository like documentation. Use it like a gym.

1. **Prime:** Read one mental model from `docs/00-research-map.md`.
2. **Study:** Read one small section from the relevant topic file.
3. **Close the file:** Explain the section from memory in plain English.
4. **Retrieve:** Answer the active-recall prompts without looking.
5. **Interleave:** Do one scenario from `docs/06-practice-lab-retrieval-tests.md`.
6. **Track gaps:** Write what was wrong, missing, or vague.
7. **Return later:** Review only the gaps, not the whole chapter.

Before every session, ask:

```text
Am I just looking at this information,
or could I explain it if the book was closed?

How does this new idea connect to something I already know?
```

---

# Suggested 30-day study calendar

Use this as the first spaced repetition plan. Codex can expand this into a full file.

| Day | Focus | Retrieval drill |
|---:|---|---|
| 1 | AML/TM foundations | Explain alert vs case vs SAR/STR without notes. |
| 2 | Legacy rule replication | List the fields needed in a rule inventory. |
| 4 | Azure architecture | Draw bronze/silver/gold flow from memory. |
| 7 | 5-year lookback | Explain why point-in-time reference data matters. |
| 10 | Data stitching | Describe customer-account-transaction joins and failure modes. |
| 14 | DQ/reconciliation | Design 5 checks for a transaction table. |
| 18 | Defect management | Classify 6 defects by root cause. |
| 21 | Analytics | Explain preparatory vs post-alert analytics. |
| 25 | Spec-as-code | Write a rule spec from memory. |
| 30 | End-to-end synthesis | Explain the whole project as a governed replay-and-proof system. |

---

# What Codex should build next

High-value next additions:

## A. Synthetic mini-project

Create a `labs/` directory with a small synthetic dataset and tasks:

```text
labs/
  synthetic_data/
    customers.csv
    accounts.csv
    transactions.csv
    country_risk_reference.csv
    legacy_alerts.csv
  tasks/
    01_profile_data.md
    02_build_stitched_view.md
    03_implement_rule.md
    04_reconcile_legacy_vs_azure.md
    05_create_evidence_pack.md
```

Keep all data fake.

## B. Rule-spec compiler concept

Create a conceptual `specs/` directory:

```text
specs/
  TM_HRC_WIRE_001.yaml
  TM_STRUCTURING_001.yaml
  TM_RAPID_MOVEMENT_001.yaml
```

Do not use proprietary bank rules. Use generic educational rules only.

## C. SQL and PySpark practice

Create:

```text
exercises/sql/
exercises/pyspark/
```

Include:

- data profiling queries;
- null/duplicate/reference checks;
- reconciliation queries;
- rule implementation skeletons;
- broken queries for debugging.

## D. Fabric certification bridge

Create:

```text
docs/08-fabric-cert-bridge.md
```

Focus on how Fabric skills map to this TM project:

- Lakehouse;
- Data Factory;
- notebooks;
- OneLake;
- warehouse;
- semantic models;
- governance / lineage.

## E. Codex task backlog

Create:

```text
CODEx_TASKS.md
```

Suggested backlog:

1. Add synthetic dataset.
2. Add SQL DQ exercises.
3. Add notebook-first PySpark and Spark SQL learning examples.
4. Add 30-day spaced repetition schedule.
5. Add Fabric cert bridge.
6. Add retrieval tests for every doc.
7. Add rule-spec examples.
8. Add evidence-pack template.
9. Add glossary.
10. Add README badges only after repo is initialized.

---

# Glossary for Codex and learners

| Term | Meaning in this repo |
|---|---|
| AML | Anti-Money Laundering. |
| CFT | Countering the Financing of Terrorism. |
| CPF | Countering Proliferation Financing. |
| TM | Transaction Monitoring. |
| Lookback | Reprocessing historical data to detect missed issues or validate monitoring. |
| Scenario | A monitoring rule or pattern. |
| Alert | Output triggered by a scenario. |
| Case | Investigation object created from one or more alerts. |
| SAR / STR | Suspicious activity/transaction report, depending on jurisdiction. |
| KYC | Know Your Customer. |
| CDD / EDD | Customer due diligence / enhanced due diligence. |
| Rule inventory | Catalog of all legacy rules and their logic. |
| Source-to-target mapping | Field-level mapping from source systems to target model. |
| Data stitching | Joining fragmented data across systems into a coherent model. |
| Point-in-time correctness | Using data values valid at the historical event date. |
| DQ | Data quality. |
| Reconciliation | Comparing counts/totals/outputs across systems or layers. |
| Defect | A tracked issue with root cause, owner, fix, retest, and evidence. |
| Evidence pack | Audit-ready bundle proving what ran, what passed/failed, and who approved. |
| Spec-as-code | Representing rules, checks, mappings, and controls as versioned executable specs. |
| Fabric | Microsoft Fabric analytics platform. |
| ADLS | Azure Data Lake Storage. |
| ADF | Azure Data Factory. |
| Delta Lake | Storage/table format commonly used for reliable lakehouse processing. |

---

# Source ledger and references

Use primary/official sources where possible. These are the references already used or identified during the session.

## AML / compliance sources

### FATF Recommendations

URL:

```text
https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html
```

Why it matters:

- Global reference point for AML/CFT/CPF standards.
- Use for risk-based approach, international AML framework, beneficial ownership, information sharing, and overall compliance context.
- The page notes that the FATF Recommendations set a comprehensive and consistent framework for countries to combat money laundering, terrorist financing, and proliferation financing, with adaptation to local circumstances.

### FINTRAC suspicious transaction reporting guidance

URL:

```text
https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/Guide2/2-eng
```

Why it matters:

- Canadian suspicious transaction reporting context.
- Useful for facts/context/indicators thinking.
- Use carefully and verify the live page before quoting because regulatory guidance can change.

### FFIEC BSA/AML Manual

URLs:

```text
https://bsaaml.ffiec.gov/manual/InvestigationsAndSARFiling/01
https://bsaaml.ffiec.gov/manual/AssessingComplianceWithBSARegulatoryRequirements/05
```

Why it matters:

- US bank examination view of BSA/AML processes.
- Useful for SAR process, monitoring, documentation, investigation, and controls.
- Use as a control-oriented reference even when the case study is not US-specific.

## Azure / Microsoft data platform sources

### Azure Data Lake Storage Gen2

URL:

```text
https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction
```

Why it matters:

- Official Microsoft description of ADLS as enterprise data lake capabilities built on Blob Storage.
- Supports the repo's raw/bronze/silver/gold data lake architecture.

### Azure Data Factory

URL:

```text
https://learn.microsoft.com/en-us/azure/data-factory/introduction
```

Why it matters:

- Official Microsoft reference for ADF as cloud ETL/ELT and data integration/orchestration service.
- Supports ingestion, pipeline orchestration, monitoring, scheduling, and hybrid integration study.

### Azure Databricks Delta Lake

URL:

```text
https://learn.microsoft.com/en-us/azure/databricks/delta/
```

Why it matters:

- Official Microsoft/Databricks reference for Delta Lake on Azure Databricks.
- Supports reliable table processing, large historical data, and lakehouse design.

### Microsoft Fabric Lakehouse

URL:

```text
https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview
```

Why it matters:

- Official Microsoft Fabric Lakehouse reference.
- Supports the user's note to get Fabric certification ready.

### Microsoft Purview data lineage

URL:

```text
https://learn.microsoft.com/en-us/purview/concept-data-lineage
```

or redirected classic page:

```text
https://learn.microsoft.com/en-us/purview/data-gov-classic-lineage
```

Why it matters:

- Official Microsoft reference for lineage concepts.
- Supports the repo's “every alert is a lineage problem” mental model.

## Learning science sources

### Bjork Learning and Forgetting Lab

URL:

```text
https://bjorklab.psych.ucla.edu/research/
```

Why it matters:

- Supports retrieval practice, testing effect, spacing, desirable difficulty, interleaving, and generation.
- The page explains that tests can be learning events, not only assessment events, and describes desirable difficulties as harder training conditions that can improve long-term learning.

### Roediger & Karpicke testing effect paper

URL:

```text
https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x
```

Why it matters:

- Research basis for retrieval practice.
- Use for the claim that recalling information strengthens long-term retention more effectively than passive review in many settings.

### Dunlosky et al. learning techniques review

URL:

```text
https://journals.sagepub.com/doi/10.1177/1529100612453266
```

Why it matters:

- Broad review of effective learning techniques.
- Useful for ranking retrieval practice and distributed practice highly relative to rereading/highlighting.

## GitHub operations source

### GitHub REST repository contents API

URL:

```text
https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents
```

Why it matters:

- Explains how a write-capable environment can create or update files in a GitHub repo.
- Requires commit message, base64-encoded content, and appropriate permissions.
- Fine-grained tokens need contents write permission; workflow edits also need workflow write permission.

---

# Model answer style for future content

Write future docs in this style:

- Direct and practical.
- Markdown-first.
- Study-oriented, not resume/interview-oriented.
- Use mental models and failure modes.
- Include retrieval prompts.
- Include what-if scenarios.
- Include small executable examples where possible.
- Avoid overclaiming. Mark assumptions clearly.
- Prefer public, official sources.
- Keep content public-safe and defensive.

Bad style:

```text
Here is a generic summary of AML.
```

Good style:

```text
You are given a legacy rule that produces 10,000 alerts per month. The Azure version produces 9,800. List five possible root causes, classify each as source/mapping/transformation/rule/reference issue, and propose evidence needed to close the defect.
```

---

# Final one-page mental model

Memorize this:

```text
This project is about rebuilding legacy Transaction Monitoring rules from SAS/Oracle/IMS onto Azure/Fabric for a 5-year historical lookback.

The critical workstreams are:

1. Rule discovery and documentation
2. Source data ingestion
3. Customer/account/transaction/reference data stitching
4. Point-in-time historical correctness
5. Data quality and reconciliation
6. Rule implementation on Azure/Fabric/Databricks
7. Parallel validation against legacy output
8. Defect management
9. Preparatory and post-alert analytics
10. Audit evidence and governance

The key success factor is not only whether the pipeline runs, but whether the bank can prove that the outputs are complete, accurate, reproducible, explainable, and approved.
```

---

# Public-safety note

This repository is for compliance, data engineering, and detection-system learning. It describes AML/TM concepts from a defensive and governance perspective. It does not provide instructions for evading controls, hiding activity, or committing financial crime.
