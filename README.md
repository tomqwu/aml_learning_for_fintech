# AML Learning for Fintech: Transaction Monitoring, Azure Data Engineering, and Make-It-Stick Study System

This repository is a public-safe study pack for learning how AML / Transaction Monitoring (TM) systems are built, migrated, validated, and governed in a fintech or banking data environment. It is shaped around a realistic **5-year historical lookback** and **legacy-rule-to-cloud modernization** case study, but it intentionally avoids internal names, private chat content, and confidential project wording.

The pack is designed for active learning, not passive reading. Every topic includes retrieval prompts, what-if scenarios, reverse-engineering exercises, interleaving drills, and spaced-repetition review sessions.

> Working thesis: a strong AML/TM data engineer does not only build ETL. They build evidence-producing, repeatable, governed data systems that can explain why an alert was produced, which data was used, which rule version ran, which defects were found, and how output was reconciled.

---

## Repository map

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
| [`templates/rule_spec_template.yaml`](templates/rule_spec_template.yaml) | YAML-style rule specification template. |
| [`templates/dq_check_template.sql`](templates/dq_check_template.sql) | SQL templates for DQ and reconciliation checks. |
| [`templates/retrieval_session_template.md`](templates/retrieval_session_template.md) | One-session active recall template. |
| [`templates/meeting_to_memory_converter.md`](templates/meeting_to_memory_converter.md) | Meeting-to-memory template for converting notes into application tests. |
| [`scripts/push_to_github.sh`](scripts/push_to_github.sh) | Helper script for pushing this pack into the target GitHub repository. |

---

## How to study this repository

Do not read it like documentation. Use it like a gym.

### Daily loop

1. **Prime:** Read one mental model from `00-research-map.md`.
2. **Study:** Read one section from the relevant topic file.
3. **Close the file:** Explain the section from memory in plain English.
4. **Retrieve:** Answer the active-recall prompts without looking.
5. **Interleave:** Do one what-if scenario from `06-practice-lab-retrieval-tests.md`.
6. **Track gaps:** Write what you got wrong and review only those gaps next time.

The guiding question before every session:

> Am I looking at the information, or can I explain and apply it with the notes closed?

---

## Five expert mental models

### 1. AML/TM is a risk-based control system, not just a detection engine

Transaction monitoring is part of a broader financial crime control environment. Rules, alerts, cases, risk ratings, KYC data, sanctions indicators, investigation outcomes, and reporting obligations all interact. A model or rule that detects unusual activity but cannot support review, explanation, and control evidence is incomplete.

### 2. A lookback project is historical replay plus proof

A 5-year lookback is not only “run five years of data.” It requires historical completeness, point-in-time reference data, replayable pipelines, documented assumptions, output reconciliation, defect resolution, and sign-off evidence.

### 3. Every alert is a data lineage problem

An alert is not just a row in an output table. It should be traceable to customer data, account data, transactions, reference data, rule version, threshold, aggregation window, batch run, and exception handling.

### 4. Legacy migration is an equivalence problem before it is a modernization problem

When old SAS/Oracle/IMS-style logic is moved to Azure, the first goal is usually to prove that the new output is equivalent to the legacy output. Only after that should the team tune, optimize, or modernize rule behavior.

### 5. Governance is executable

Good governance should not live only in slide decks. Rule specs, DQ checks, mappings, thresholds, approvals, test cases, evidence packs, and deployment controls can be represented as versioned artifacts.

---

## Three places experts disagree

### Debate 1: Rule-based monitoring vs ML/AI-assisted monitoring

**Rule-based side:** deterministic scenarios are explainable, auditable, easier to validate, and easier for investigators to understand. They fit regulated environments where reason codes, thresholds, and policy ownership matter.

**ML/AI side:** financial crime patterns evolve, rule-only systems can create large false-positive volumes, and graph/behavioral analytics can uncover patterns not captured by simple thresholds.

**Practical synthesis:** use deterministic rules as the controlled baseline; use analytics to profile, prioritize, tune, explain, and triage. Do not deploy opaque models where the control process cannot explain outcomes.

### Debate 2: Exact replication vs transformation during migration

**Exact replication side:** regulators, auditors, and business owners need confidence that the migrated system preserves prior behavior. Parallel-run comparison is simpler when outputs are expected to match.

**Modernization side:** copying old defects into a new platform wastes the opportunity to reduce false positives, improve data quality, and adopt better designs.

**Practical synthesis:** separate the phases: first prove equivalence, then introduce governed changes with impact analysis and approval.

### Debate 3: Centralized lakehouse vs specialized compliance platform

**Lakehouse side:** a unified data platform improves lineage, scale, replayability, analytics, and shared controls across domains.

**Specialized platform side:** AML vendors often include scenario libraries, case-management integration, model governance, investigator workflows, and regulatory reporting features.

**Practical synthesis:** use a governed data platform for ingestion, transformation, replay, and analytics; integrate with specialized AML/case platforms where workflow and reporting requirements demand it.

---

## Ten deep-understanding probes

Answer these with the files closed. A memorizer will give definitions; a practitioner will explain tradeoffs, failure modes, and evidence.

1. Why is a 5-year lookback harder than a normal monthly batch run?
2. What does “point-in-time correctness” mean, and how can a lookback fail without it?
3. Why is a generated alert a lineage problem?
4. What must be captured in a rule specification so that business, engineering, QA, and audit can all use it?
5. How would you prove that an Azure implementation of a legacy rule is equivalent to the old implementation?
6. When is an alert-count mismatch acceptable, and when is it a defect?
7. Why can data quality checks create a false sense of security if they only check row counts?
8. How should defects be classified so that root cause is clear?
9. What role should analytics play before rule execution and after alert generation?
10. Why is “we built the pipeline” not enough evidence in a regulated AML/TM project?

---

## Public-safety note

This repository is for compliance, data engineering, and detection-system learning. It describes AML/TM concepts from a defensive and governance perspective. It does not provide instructions for evading controls, hiding activity, or committing financial crime.
