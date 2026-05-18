# 06 — Practice Lab: Retrieval Tests and What-If Scenarios

Use this file with the notes closed. The goal is not to memorize answers. The goal is to diagnose, explain, and defend your reasoning.

---

## 1. Retrieval Test A — Core concepts

Answer in your own words.

1. Explain AML transaction monitoring in five sentences without using the word “compliance.”
2. What is the difference between a scenario, a rule, an alert, a case, and a report?
3. Why does a monitoring system need both facts and context?
4. Why is customer risk rating not just a dashboard field?
5. What does “risk-based approach” mean in a data pipeline?
6. Why is a false positive not automatically a bad alert?
7. What does “lineage” mean for an alert?
8. Why is historical replay more difficult than current-month processing?
9. What is point-in-time correctness?
10. What is an evidence pack?

### Scoring rubric

| Score | Standard |
|---|---|
| 1 | Definition only, no example. |
| 2 | Definition plus example, but no tradeoff. |
| 3 | Clear explanation with example and one failure mode. |
| 4 | Explanation includes business, technical, and control implications. |
| 5 | Explanation includes tradeoffs, evidence, and how to test it. |

---

## 2. Retrieval Test B — Azure modernization

1. Explain the difference between raw/bronze, silver, and gold layers.
2. What is ADF/Fabric Data Factory responsible for?
3. What is Databricks/Spark useful for in a 5-year lookback?
4. What does Delta Lake add beyond plain Parquet files?
5. Why does Purview or another catalog/lineage tool matter?
6. What is idempotence, and why does it matter for reruns?
7. What is a deterministic alert key?
8. Why should partitions align with business processing windows?
9. What metadata should every output table include?
10. What does a run manifest contain?

---

## 3. Retrieval Test C — Rule migration

1. Why is legacy migration an equivalence problem?
2. What can go wrong when translating SAS logic into Spark SQL?
3. What can go wrong when translating Oracle stored logic into a cloud pipeline?
4. What can go wrong when extracting IMS/mainframe data?
5. Why do rules need version numbers?
6. What is a golden record test?
7. What is source-to-target mapping?
8. What belongs in the eligibility section of a rule spec?
9. What belongs in the controls section of a rule spec?
10. What is the difference between expected difference and defect?

---

## 4. Retrieval Test D — DQ and defects

1. List ten DQ dimensions without looking.
2. Explain why row counts are necessary but insufficient.
3. What is referential integrity?
4. What is the difference between a DQ exception and a defect?
5. Why should exception records not be silently dropped?
6. What is a source data defect?
7. What is a mapping defect?
8. What is a rule logic defect?
9. What evidence should be attached to close a defect?
10. How would you triage an alert mismatch?

---

## 5. What-if scenarios

### Scenario 1 — Alert count doubles

A migrated rule produces 20,000 alerts in Azure for June 2022. The legacy system produced 10,000 alerts for the same period.

Answer:

1. What are five possible root causes?
2. Which reconciliation metrics would you check first?
3. How would you determine whether this is a data defect, mapping defect, rule defect, or expected difference?
4. What evidence would you show to business owners?
5. What would prevent you from signing off?

### Scenario 2 — Alert count drops to zero

A rule that normally produces alerts generates zero alerts for three months of historical data.

Answer:

1. Why is “zero alerts” not automatically good news?
2. Which input tables would you check?
3. Which DQ checks might reveal the issue?
4. What rule-spec assumptions should be reviewed?
5. How would you create a golden test to reproduce the issue?

### Scenario 3 — Reference data has no effective dates

The country risk reference table only has current values, but the lookback covers five years.

Answer:

1. What risk does this create?
2. What point-in-time data is missing?
3. What mitigation options exist?
4. How would you document the limitation?
5. What sign-off is required?

### Scenario 4 — Account ownership changed

An account belonged to Customer A in 2021 and Customer B in 2023. The lookback output assigns all alerts to Customer B.

Answer:

1. What is the likely defect?
2. Which table design would prevent this?
3. Which test case should have caught it?
4. What downstream impacts could occur?
5. What remediation plan would you propose?

### Scenario 5 — Business wants to tune threshold before validation

The business team wants to reduce alert volume by increasing a threshold before the migration equivalence test is complete.

Answer:

1. Why is this risky?
2. How should equivalence and optimization be separated?
3. What analysis is needed before changing the threshold?
4. What governance artifacts must be updated?
5. What would you recommend as the next step?

### Scenario 6 — DQ exception table grows unexpectedly

A source extract has a sudden increase in missing account IDs.

Answer:

1. What questions do you ask the source-system team?
2. How do you assess impact on rule output?
3. Which severity would you assign and why?
4. What evidence belongs in the defect ticket?
5. Can the batch continue? Under what conditions?

### Scenario 7 — Rerun creates duplicate alerts

A pipeline rerun creates duplicate alerts for the same period.

Answer:

1. What design flaw likely exists?
2. How would deterministic alert keys help?
3. How should partition overwrite work?
4. What reconciliation metric catches this?
5. What code or process change would prevent recurrence?

### Scenario 8 — Legacy output cannot be reproduced

The old system has missing documentation and inconsistent outputs for the same input period.

Answer:

1. How do you proceed without guessing?
2. What assumptions must be documented?
3. What stakeholder decisions are required?
4. How do golden records help?
5. What evidence should be retained?

### Scenario 9 — Performance misses SLA

A rule cannot complete within the required processing window.

Answer:

1. Which Spark/SQL performance areas would you inspect?
2. How would partitioning help?
3. How could skewed joins affect runtime?
4. What tradeoff exists between performance optimization and equivalence validation?
5. What monitoring metrics should be captured?

### Scenario 10 — Audit asks why an alert triggered

An auditor selects one alert and asks for proof of why it exists.

Answer:

1. What fields do you show?
2. What supporting transactions do you show?
3. What rule version and parameter evidence do you show?
4. What DQ/reconciliation evidence do you show?
5. What would be a weak or unacceptable answer?

---

## 6. Reverse-engineering labs

### Lab 1 — Infer rule behavior from output

Output summary:

```text
rule_id: TM002
window: 7 days
alerts: 1,250
alert count increased most for high-risk customers
supporting transactions are mostly international wires
```

Infer:

1. What might the rule be aggregating?
2. What input tables are likely required?
3. What reference data may be involved?
4. Which DQ checks are critical?
5. What boundary tests should exist?

### Lab 2 — Infer defect from reconciliation

```text
Bronze transaction count: 5,000,000
Silver transaction count: 5,000,000
Gold rule input count: 3,200,000
Legacy eligible population: 4,900,000
Azure eligible population: 3,200,000
```

Infer:

1. Which stage likely introduced the problem?
2. Which filters or joins should be inspected?
3. What defect categories are possible?
4. What sample records would you request?
5. How would you summarize impact?

### Lab 3 — Infer governance gap

```text
Rule changed in production.
Alert volume dropped by 40%.
No rule-spec version changed.
No approval record is available.
```

Infer:

1. What governance failure occurred?
2. What evidence is missing?
3. How could version control prevent this?
4. What emergency review should happen?
5. What preventive control should be added?

---

## 7. Explain-it-back drills

Explain each in plain English:

1. “A lookback is a controlled historical replay.”
2. “An alert is a lineage object.”
3. “Rule migration is an equivalence problem.”
4. “Data quality is a control.”
5. “Spec-as-code turns governance into executable artifacts.”
6. “Point-in-time reference data protects historical truth.”
7. “False positives should be measured, not blindly eliminated.”
8. “A defect is not closed until it has evidence.”
9. “A rerunnable pipeline must be idempotent.”
10. “Analytics supports both preparation and post-alert review.”

---

## 8. Final capstone exercise

Design a mini solution for this case:

```text
A bank needs to replay 5 years of transaction monitoring data.
Legacy rules exist in SAS and Oracle.
Customer/account data comes from separate systems.
Some reference data changes over time.
The bank wants the new implementation on Azure/Fabric/Databricks.
The output must be auditable.
```

Your answer must include:

1. Target architecture
2. Data model
3. Rule migration approach
4. DQ/reconciliation framework
5. Defect management workflow
6. Evidence pack
7. Analytics plan
8. 30-day learning plan for a new team member

Do this closed-book first. Then compare with the other docs.
