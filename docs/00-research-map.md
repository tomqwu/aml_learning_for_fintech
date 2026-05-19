# 00 — Research Map: AML/TM Modernization Knowledge Landscape

## 1. What field are we studying?

This field sits at the intersection of:

1. **AML / financial crime compliance** — laws, regulatory expectations, suspicious transaction reporting, customer due diligence, sanctions indicators, and risk-based controls.
2. **Transaction monitoring operations** — scenarios/rules, alerts, case workflow, investigator review, false positive analysis, threshold tuning, and regulatory evidence.
3. **Data engineering** — ingestion, data lakes/lakehouses, batch processing, historical replay, rule execution, data quality, reconciliation, and monitoring.
4. **Governance and auditability** — lineage, versioning, approvals, defect management, evidence packs, reproducibility, and change control.
5. **Learning science** — retrieval practice, spaced repetition, interleaving, elaboration, and desirable difficulty.

The goal of this repository is not to memorize AML acronyms. The goal is to build the mental model needed to participate in a real compliance data modernization project.

---

## 2. Source hierarchy used in this research

For this topic, use sources in this order:

| Tier | Source type | Why |
|---|---|---|
| 1 | Regulators and government guidance | Highest authority for obligations and compliance expectations. |
| 2 | International standard setters | Useful for risk-based principles and global AML language. |
| 3 | Cloud/platform official docs | Best source for Azure/Fabric/Databricks architectural details. |
| 4 | Peer-reviewed learning science | Best source for study-system design. |
| 5 | Vendor/industry commentary | Useful, but verify against higher tiers. |

Key official sources used here include FATF, FINTRAC, FFIEC, Microsoft Learn, IBM, Oracle, and peer-reviewed learning-science papers.

---

## 3. Five core mental models every expert shares

### Mental Model 1 — Risk-based controls

AML programs do not try to treat every customer, product, geography, and transaction the same. They identify risk, assign controls proportionate to risk, monitor changes, and document decisions.

Implication for data engineers:

- Customer risk rating is not just a field; it can change rule thresholds, monitoring intensity, and investigation priority.
- Geography, products, channels, and customer behavior are risk dimensions.
- The pipeline must preserve enough context for a reviewer to understand why the activity was considered unusual.

### Mental Model 2 — The alert lifecycle

A transaction monitoring alert is not an endpoint. It is a handoff into a decision process.

```text
Raw event -> rule trigger -> alert -> review -> case/no-case -> possible report -> feedback -> tuning
```

Implication:

- A pipeline that generates alerts but cannot support downstream investigation is incomplete.
- Alert features should explain the trigger: aggregation window, threshold, customer segment, rule version, reference data version, and supporting transactions.

### Mental Model 3 — Entity-time graph

Financial crime monitoring is not only about single transactions. It is about relationships through time.

```text
Customer -> Account -> Transaction -> Counterparty -> Geography -> Reference list -> Alert -> Case
```

Implication:

- Data stitching is central.
- Point-in-time correctness matters: use the customer/account/reference state that applied at the time of the transaction, not only the latest state.
- Relationship changes over time can create or eliminate risk signals.

### Mental Model 4 — Equivalence before optimization

A legacy migration should first answer:

> Does the new platform reproduce the old output under the same inputs and assumptions?

Only after answering that should the team ask:

> Should we tune, modernize, or redesign the rule?

Implication:

- Rule migration needs parallel runs, golden records, field-level comparisons, and documented expected differences.
- Do not mix “we changed the logic intentionally” with “the migration is wrong.” Track these separately.

### Mental Model 5 — Evidence as a product

In regulated data systems, evidence is a deliverable.

Evidence can include:

- source-to-target mapping
- rule specification
- DQ checks
- reconciliation reports
- run logs
- defect tickets
- approvals
- rule version history
- sample records supporting the output

Implication:

- Build pipelines to emit evidence by design.
- Each production run should be traceable by batch ID, rule version, source period, and data version.

---

## 4. What experts broadly agree on

### Consensus 1 — AML/TM requires facts, context, and indicators

A suspicious transaction determination should not be treated as a simple single-field trigger. FINTRAC emphasizes facts, context, and indicators when establishing reasonable grounds to suspect. This maps directly into data engineering: data models must preserve both transactional facts and contextual customer/business information.

### Consensus 2 — Risk assessment is dynamic

Risk assessment is not one-time documentation. Products, geography, clients, delivery channels, technologies, and patterns can change. Monitoring programs and data pipelines must support reassessment.

### Consensus 3 — Historical replay needs repeatability

Lookbacks require a replayable pipeline. You must know exactly which records were processed, which rules were executed, and which outputs were generated.

### Consensus 4 — Data quality is part of the control, not just cleanup

Completeness, validity, uniqueness, referential integrity, reconciliation, timeliness, and point-in-time accuracy should be built into the pipeline and reported.

### Consensus 5 — Active learning beats passive reading

Retrieval practice and distributed practice are consistently stronger than rereading/highlighting for durable memory. Therefore this repo is structured around tests, scenarios, and repeated recall.

---

## 5. Three expert disagreements and strongest arguments

### Disagreement A — Should AML/TM stay rule-based or move toward ML/AI?

**Rule-based argument:**

- Rules are easier to explain.
- Rules map to documented policy.
- Thresholds and conditions can be validated.
- Investigators can understand rule reason codes.
- Audit teams can trace decisions.

**ML/AI argument:**

- Rule-only systems often produce high false-positive volume.
- Patterns can evolve faster than static scenarios.
- Graph and behavioral analytics may detect relationship-based risk missed by simple thresholds.
- Alert triage models can help prioritize reviewer effort.

**Best synthesis:**

Use rule-based monitoring as the controlled baseline and add analytics as a transparent decision-support layer. Any model used in the workflow must be explainable, tested, monitored, and governed.

### Disagreement B — Should migration copy old behavior exactly?

**Exact-copy argument:**

- Establishes confidence quickly.
- Makes parallel-run comparison possible.
- Reduces ambiguity when differences are found.
- Supports sign-off from legacy rule owners.

**Modernize-now argument:**

- Legacy rules may include defects or obsolete assumptions.
- Cloud migration is an opportunity to improve maintainability and reduce noise.
- Old platforms may have hidden constraints that should not be preserved.

**Best synthesis:**

Split into two workstreams:

1. **Migration equivalence:** reproduce legacy behavior.
2. **Optimization:** governed changes with documented impact analysis.

### Disagreement C — Lakehouse platform or specialized AML platform?

**Lakehouse argument:**

- Better for large-scale historical replay.
- Better for analytics and shared data products.
- Better for lineage across many source systems.
- Better for reusable DQ/reconciliation controls.

**AML platform argument:**

- Better for scenario libraries, investigator workflow, case management, and regulatory reporting.
- Often includes domain accelerators.
- May reduce implementation burden for standard scenarios.

**Best synthesis:**

Treat the lakehouse as the controlled data and replay foundation. Use AML/case platforms for workflow where they add value. Avoid black-box dependencies that cannot explain alert generation.

---

## 6. Knowledge map

```text
AML / TM domain
  ├─ AML / CFT / sanctions concepts
  ├─ suspicious transaction reporting
  ├─ KYC / CDD / EDD
  ├─ customer risk rating
  ├─ typologies and indicators
  └─ alerts, cases, investigation outcomes

Data architecture
  ├─ source systems: SAS, Oracle, IMS, files, APIs
  ├─ raw / bronze data
  ├─ cleaned / silver data
  ├─ curated / gold data
  ├─ rule execution layer
  ├─ alert output layer
  └─ analytics and evidence layer

Rule migration
  ├─ inventory
  ├─ source-to-target mapping
  ├─ rule spec
  ├─ test data
  ├─ equivalence validation
  └─ change governance

Data quality and defects
  ├─ completeness
  ├─ validity
  ├─ uniqueness
  ├─ referential integrity
  ├─ reconciliation
  ├─ defect triage
  └─ closure evidence

Learning system
  ├─ active recall
  ├─ spaced repetition
  ├─ interleaving
  ├─ elaboration
  ├─ desirable difficulty
  └─ Feynman explanation

Interview readiness
  ├─ role lens: engineer, analyst, data scientist, QA/DQ, architect/lead
  ├─ stack lens: Azure, Databricks, PySpark, Delta Lake, Lakeflow, BI, ML/MLOps
  ├─ deep Spark SQL and PySpark execution model
  ├─ first-principles examples with tiny datasets and manual expected outputs
  ├─ query basics with lots of runnable Spark SQL examples
  ├─ runnable PySpark DataFrame basics with assertions
  ├─ notebook-first bootstraps for Spark SQL and PySpark sections
  ├─ runnable-code standards: setup, run order, expected output, validation
  ├─ one-stop role guides with theory, diagrams, Q&A, and drills
  ├─ project stories
  ├─ tradeoff explanations
  ├─ failure-mode diagnosis
  └─ evidence-first answers
```

---

## 7. Skill ladder

### Level 1 — Vocabulary learner

You can define AML, TM, STR/SAR, alert, case, KYC, DQ, reconciliation, and lineage.

### Level 2 — Pipeline contributor

You can build ingestion/transformation jobs, create DQ checks, and write SQL/Spark logic for a rule.

### Level 3 — Migration analyst

You can reverse-engineer legacy logic, write mapping documents, compare output, and classify mismatches.

### Level 4 — Control-minded engineer

You can design replayable pipelines with audit evidence, batch IDs, rule versions, lineage, and defect workflow.

### Level 5 — Solution lead

You can design the full target operating model: domain, architecture, rule governance, DQ framework, analytics, testing, and sign-off.

### Level 6 — Interview-ready practitioner

You can explain the same AML/TM modernization project from multiple job lenses: Data Engineer, Data Analyst/BI, Data Scientist, QA/DQ Engineer, and Solution Architect/Lead. You can also answer stack-specific questions about Azure Databricks, PySpark, Delta Lake, Lakeflow, BI, ML/MLOps, and legacy migration while tying each answer back to controls and evidence.

---

## 8. Retrieval check

Close the file and answer:

1. What are the five mental models in this field?
2. Why is “alert = lineage problem” more useful than “alert = output row”?
3. Why should migration equivalence and optimization be separated?
4. Which parts of AML/TM belong to business risk ownership, and which belong to engineering execution?
5. What evidence should a good production run create automatically?
6. How would your answer change for a Data Engineer interview versus a Solution Architect interview?
