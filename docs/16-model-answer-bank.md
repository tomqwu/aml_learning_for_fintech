# 16 - Model Answer Bank

Use this file after attempting the questions closed-book. The answers are intentionally concise model answers, not the only possible wording. A strong answer should explain the concept, give an AML/TM modernization example, name a failure mode, and mention evidence.

---

## 1. Core Research Map Answers

### `00-research-map.md` retrieval check

1. The five mental models are risk-based controls, alert lifecycle, entity-time graph, equivalence before optimization, and evidence as a product.
2. “Alert = lineage problem” is stronger because an alert must be traceable to source records, rule version, parameters, DQ status, and run metadata. An output row without lineage cannot support investigation, reconciliation, or audit.
3. Equivalence and optimization should be separated because migration first proves the cloud implementation preserves approved legacy behavior. Optimization changes behavior or performance characteristics and needs a separate impact analysis and approval.
4. Business risk ownership covers policy, thresholds, scenarios, tuning decisions, acceptable differences, and sign-off. Engineering owns ingestion, transformations, repeatable execution, DQ checks, reconciliation tables, metadata, and evidence generation.
5. A good production run creates run manifest, input counts, DQ exceptions, reconciliation metrics, rule version, parameter snapshot, alert outputs, supporting transactions, defects, and approvals.
6. A Data Engineer answer emphasizes pipeline design, grain, Spark/Delta implementation, reruns, and reconciliation. A Solution Architect answer emphasizes operating model, governance, controls, security, NFRs, roadmap, and sign-off.

---

## 2. Domain Foundation Answers

### `01-aml-transaction-monitoring-foundations.md` active recall

1. Facts are observed data such as amount, date, counterparty, and account. Context is surrounding meaning such as customer risk, product, geography, and history. Indicators are patterns that may suggest suspicious activity when facts and context are combined.
2. An alert is a system-generated item for review. A report such as an STR/SAR is a formal regulatory filing decision made after investigation and judgment.
3. Most scenarios need customers, accounts, transactions, reference data, rule parameters, customer risk, account ownership, and sometimes case/outcome history.
4. Point-in-time data matters because historical monitoring must use the customer/account/reference state that was true at the transaction date, not today’s state.
5. Ungoverned tuning can suppress or inflate alerts without approval, break auditability, and hide whether differences came from migration defects or intentional policy changes.
6. False positives are expected in risk controls because rules are designed to escalate uncertainty. The goal is to measure, tune, and govern them, not eliminate every non-case alert blindly.
7. Transaction monitoring is a system that watches financial activity for patterns that deserve review. It combines transaction facts with customer and account context. When a pattern triggers, the system creates an alert with evidence for a reviewer.
8. An alert should include source transactions, customer/account context, rule ID and version, parameters, trigger metrics, time window, DQ/reconciliation status, batch ID, and supporting lineage.

### `02-5year-lookback-azure-modernization.md` active recall

1. A 5-year lookback is a controlled historical replay across changing data, schemas, rules, and reference values. It requires proof that each period was processed completely and correctly.
2. Partitioning matters because backfills and reruns need to isolate business periods, overwrite safely, and avoid scanning the entire history for every run.
3. Idempotence means the same run can be repeated without creating duplicates or inconsistent output.
4. Batch ID ties inputs, transformations, DQ checks, outputs, reconciliation, and evidence to a specific run.
5. Point-in-time reference data needs business key, effective start, effective end, status/version, source, load timestamp, and ownership or approval metadata.
6. Common stitching failures include missing keys, many-to-many joins, current-state joins, invalid effective dates, orphan accounts, duplicate transactions, and inconsistent product/customer mappings.
7. A lookback should generate run manifests, row counts, control totals, DQ exceptions, reconciliation metrics, alert counts, supporting transaction evidence, defects, and approvals.
8. ADLS stores lake data; ADF/Fabric Data Factory orchestrates movement; Databricks/Spark transforms and computes; Delta provides ACID tables and history; Fabric supports lakehouse/warehouse/BI integration; Synapse is an analytics platform option; Purview provides catalog and lineage.

### `03-rule-migration-spec-as-code.md` active recall

1. Rule migration is behavior reconstruction, not syntax translation, because legacy behavior may live in code, parameter tables, scheduler assumptions, data quirks, and undocumented exclusions.
2. A rule inventory contains rule ID, owner, purpose, source systems, input tables, parameters, thresholds, exclusions, schedule, outputs, dependencies, known defects, and sign-off status.
3. Source-to-target mapping defines how each legacy field maps to a cloud field, including type, transformation, business meaning, validation, and unresolved assumptions.
4. A useful rule specification is readable by business and executable or testable by engineering. It states inputs, eligibility, joins, windows, thresholds, outputs, edge cases, and controls.
5. A golden record is a tiny curated input case with known expected output used to prove rule behavior, boundary logic, and defect fixes.
6. An expected difference is approved and explained. A defect is an unapproved mismatch or failure requiring root cause, fix, retest, and closure evidence.
7. Thresholds should be parameterized and versioned so behavior can be reproduced for a historical run and changes can be approved, compared, and audited.
8. Spec-as-code improves governance by turning approved rule logic, parameters, tests, and controls into versioned artifacts that can drive implementation and validation.

### Rule spec exercise answer shape

1. Required input tables: transactions, accounts, customers, ownership history, risk ratings, country/product/reference data, rule parameters, and legacy comparison output.
2. Point-in-time checks: account ownership, customer risk, product status, country risk, and rule parameter version effective on the transaction or processing date.
3. Exclusions to clarify: internal/test accounts, closed accounts, reversals, declined transactions, same-customer transfers, missing country, and product-specific exclusions.
4. Boundary tests: exact threshold, one cent below/above threshold, start/end date, null key, duplicate transaction, ownership change, and effective-date edge.
5. Reconciliation metrics: input counts, eligible counts, excluded counts, alert counts, total trigger amount, distinct customers, orphan counts, duplicate counts, and legacy/cloud matched/unmatched keys.
6. Alert output fields: alert key, rule ID/version, customer/account ID, trigger date, window, trigger metric, supporting transaction IDs, batch ID, DQ status, and lineage metadata.

### `04-data-quality-reconciliation-defect-management.md` active recall

1. DQ is part of AML/TM controls because bad data can suppress, inflate, or misassign alerts. A monitoring result is only defensible if input quality and exceptions are visible.
2. Completeness asks whether required records/fields exist. Reconciliation asks whether totals and records agree across systems or processing layers.
3. Point-in-time correctness is a DQ dimension because historically valid results depend on effective-dated customer, account, risk, and reference data.
4. An exception table should include record key, source, failed check, severity, reason, affected rule/output, batch ID, detected timestamp, owner, and resolution status.
5. Classify a legacy/cloud mismatch by checking data, mapping, rule logic, reference data, parameters, timing, environment, and whether the difference is approved.
6. Defect closure evidence includes root cause, impacted records/periods, fix description, retest results, reconciliation before/after, sample evidence, approval, and closure date.
7. Row counts are insufficient because the same count can hide amount mismatches, missing keys, wrong joins, duplicate alerts, incorrect segmentation, or wrong supporting transactions.
8. Root cause analysis means tracing a symptom back through source data, mapping, transformations, rule logic, parameters, and outputs until the owner and fix are clear.
9. Conservation of amount: an amount is never silently changed between layers - it is dropped, duplicated, transformed, or reclassified, each with a signature and required evidence, so the investigation becomes accounting, not guessing.
10. A gold total that rises with row counts and no new transactions is join explosion; prove it with pre/post join counts and business keys whose copy count exceeds one.
11. Count-preserving total differences come from casting-to-null, zero/null defaulting, FX conversion, or sign/unit errors.
12. FX differences are acceptable when registered as expected differences and each converted row carries rate, rate date, and source amount.

---

## 3. Practice Lab Answers

### Retrieval Test A - core concepts

1. Transaction monitoring examines financial activity for patterns that deserve review, using customer/account/transaction context. It creates alerts when scenarios trigger. Reviewers decide whether activity needs escalation. Good monitoring keeps lineage and evidence. It balances risk coverage with operational burden.
2. Scenario is the risk pattern, rule is the implemented logic, alert is the generated item, case is the investigation workflow, and report is the regulatory filing decision.
3. Facts show what happened; context explains whether it is unusual or risky.
4. Risk rating changes eligibility, threshold, priority, segmentation, and review context.
5. Risk-based pipeline design means controls, thresholds, data quality, evidence, and review depth are stronger where risk is higher.
6. A false positive can still show that the control is working as an escalation mechanism; it becomes a problem when rates are unmanaged or unexplainable.
7. Alert lineage is the trace from alert back to source rows, rule version, parameters, transformations, DQ status, and run metadata.
8. Historical replay is harder because data, ownership, schemas, risk ratings, and reference values changed over time.
9. Point-in-time correctness means using the data state valid at the historical event time or run policy time.
10. Evidence pack is the set of artifacts proving what ran, what data was used, what output was produced, what differences exist, and who approved it.

### Retrieval Test B - Azure modernization

1. Bronze/raw preserves landed data; silver standardizes and validates; gold curates rule-ready and reporting-ready outputs.
2. ADF/Fabric Data Factory orchestrates movement, scheduling, dependencies, parameters, and external system integration.
3. Databricks/Spark handles distributed transformations, joins, windows, aggregations, replay, DQ checks, and rule execution.
4. Delta adds transaction log, ACID behavior, schema controls, history, time travel, and safer reruns.
5. Catalog/lineage matters because AML outputs must be discoverable, governed, permissioned, and traceable.
6. Idempotence prevents duplicate or inconsistent outputs during retries and backfills.
7. Deterministic alert key is a stable key generated from rule, customer, period, and trigger grain so reruns match prior outputs.
8. Business-period partitions make backfills, SLA windows, reconciliation, and selective overwrites manageable.
9. Output tables need batch ID, source system, processing period, rule version, load timestamp, DQ status, lineage, and approval or run metadata.
10. A run manifest contains run ID, inputs, parameters, code/rule version, time range, counts, DQ results, output locations, reconciliation status, and owner.

### Retrieval Test C - rule migration

1. It is an equivalence problem because the target must reproduce approved behavior before changing or improving it.
2. SAS migration risks include merge semantics, formats, macros, missing-value behavior, date logic, implicit retain behavior, and sort assumptions.
3. Oracle migration risks include stored procedure side effects, date/time semantics, null behavior, optimizer-dependent assumptions, and parameter tables.
4. IMS/mainframe risks include hierarchical relationships, copybook layouts, encoding, batch timing, and extraction completeness.
5. Rule versions preserve which logic and parameters were active for each run.
6. Golden record tests prove known inputs produce expected outputs, including edge cases.
7. Source-to-target mapping documents field meaning, transformation, type, quality rule, and owner.
8. Eligibility includes population, statuses, product scope, geography, time window, exclusions, and required joins.
9. Controls include DQ checks, reconciliation metrics, exception routing, sign-off gates, and evidence requirements.
10. Expected difference is approved and documented; defect is unresolved or unapproved mismatch.

### Retrieval Test D - DQ and defects

1. Completeness, validity, accuracy, consistency, uniqueness, timeliness, referential integrity, point-in-time correctness, conformity, and reconciliation.
2. Row counts do not prove values, keys, amounts, joins, alert grain, or lineage are correct.
3. Referential integrity means child records reference valid parent records, such as transactions pointing to known accounts.
4. DQ exception is a detected data-quality failure; defect is a confirmed issue requiring remediation and closure evidence.
5. Silent drops hide control impact and make outputs unreproducible.
6. Source data defect originates in upstream extract or source system values.
7. Mapping defect comes from incorrect field mapping or transformation between source and target.
8. Rule logic defect comes from implemented behavior differing from the approved spec.
9. Closure evidence includes root cause, impact, fix, retest, reconciled result, and approval.
10. Triage alert mismatch by checking scope, counts, eligibility, joins, parameters, rule version, sample records, and approved differences.

### What-if scenarios

1. Alert count doubles: likely causes include duplicated input, wider eligibility, many-to-many join, threshold/parameter mismatch, missing exclusion, reference mismatch, or wrong period filter. Check eligible counts, distinct customers/accounts, duplicate keys, total amounts, join cardinality, and matched/unmatched legacy keys. Do not sign off while root cause, impact, and approval are missing.
2. Alert count drops to zero: zero can mean broken ingestion, empty eligibility, bad join, missing parameters, wrong date filter, or failed reference data. Check transactions, accounts, customers, parameters, country/product references, and golden records that should trigger.
3. Reference data has no effective dates: current-state lookup can rewrite history. Mitigate by sourcing historical reference snapshots, reconstructing from audit logs, limiting scope, documenting assumption, and getting risk/control-owner sign-off.
4. Account ownership changed: likely current-state join defect. Use effective-dated account ownership and point-in-time join tests around ownership-change dates. Remediate by rebuilding affected periods and reconciling reassigned alerts.
5. Threshold tuning before validation: risky because it mixes migration defects with intentional change. First prove equivalence, then run impact analysis, update rule spec/parameters, obtain approval, and compare before/after volumes.
6. DQ exception spike: ask source team about extract changes, outages, schema changes, late feeds, and upstream incidents. Assess affected rules, records, customers, and periods. Continue only if severity, quarantine, and sign-off allow.
7. Duplicate alerts on rerun: likely append-only writes without deterministic keys or partition overwrite. Use stable alert keys, delete/replace target period, reconcile duplicate keys, and add idempotent write tests.
8. Legacy output cannot be reproduced: stop guessing. Document unknowns, collect evidence, create golden records, classify assumptions, get owner decisions, and preserve legacy extracts, comparison outputs, and approved limitation notes.
9. Performance misses SLA: inspect scan size, partitions, file layout, shuffles, skew, join strategy, caching, and AQE. Tune only after correctness baseline is locked, then prove row/amount/key outputs are unchanged.
10. Audit asks why an alert triggered: show alert key, rule version, parameters, trigger metrics, supporting transactions, customer/account context, source lineage, DQ status, reconciliation status, and run manifest. “The code generated it” is unacceptable.

### Reverse-engineering labs

1. Lab 1: The rule likely aggregates international wire activity over 7 days, segmented by customer risk. Inputs include transactions, customers, accounts, ownership, country risk, and parameters. Critical DQ checks include missing accounts, invalid countries, duplicate transactions, effective dates, and boundary windows.
2. Lab 2: The problem likely appears between silver and gold eligibility. Inspect eligibility filters, account/customer joins, status filters, date filters, and reference joins. Possible defects are mapping, join, reference, or rule eligibility defects. Request samples dropped from gold but present in legacy.
3. Lab 3: A production rule changed without version or approval. Missing evidence includes change request, rule spec version, parameter version, test results, approval, and deployment record. Add version control, promotion gates, and emergency review.

### Explain-it-back drills

1. A lookback is controlled historical replay because the system reprocesses past periods with repeatable logic and proof.
2. An alert is a lineage object because it must explain which data, rule, parameters, and run produced it.
3. Rule migration is equivalence because the first target is approved behavior preservation.
4. Data quality is a control because bad data directly changes monitoring outcomes.
5. Spec-as-code makes governance executable by turning approved rules into versioned parameters, tests, and deployable logic.
6. Point-in-time reference data protects historical truth by using the value valid at the event time.
7. False positives should be measured because they are operational cost and control-sensitivity signals.
8. A defect needs evidence because closure without proof does not reduce risk.
9. Idempotent reruns prevent duplicate or inconsistent outputs after retry.
10. Analytics supports preparation through profiling and supports post-alert review through performance, workload, and effectiveness analysis.

### Interview role drills

1. Data Engineer owns reliable pipelines, Spark/Delta implementation, DQ, reruns, and reconciliation evidence.
2. Analyst/BI owns metric definitions, dashboards, drill-through, trends, and dashboard-to-source tie-out.
3. Data Scientist owns features, labels, leakage prevention, explainability, model tracking, and drift monitoring.
4. QA/DQ Engineer owns test strategy, golden records, DQ checks, defect classification, retest proof, and sign-off evidence.
5. Architect/Lead owns target architecture, governance, delivery sequencing, operating model, NFRs, and stakeholder sign-off.

### Stack flashcards

1. ADF/Fabric Data Factory orchestrates and moves data across systems; Databricks does distributed processing and analytics logic.
2. Delta supports replay and auditability through transaction log, ACID writes, schema controls, and history.
3. Lazy execution means transformations build a plan; actions trigger work, so debugging needs counts, explain plans, and careful action placement.
4. Lakeflow adds managed ingestion, declarative pipelines, expectations, jobs, monitoring, and production workflow structure.
5. Jobs orchestrate tasks; Declarative Pipelines define managed tables/views and transformations.
6. Streaming table for incrementally ingested data, materialized view for maintained derived results, temporary view for intermediate logic.
7. DQ expectations validate data during processing; reconciliation compares totals/records across layers or systems.
8. Unity Catalog or lineage supports governance by controlling access, ownership, discovery, and traceability.
9. Lock metric grain, time period, filters, numerator/denominator, exclusions, refresh logic, and source table.
10. Safe ML prioritization needs point-in-time features, explainability, human review, monitoring, MLflow evidence, and governance approval.

### Spark SQL and PySpark drills

1. SQL-to-PySpark: filter WIRE and month, group by customer, aggregate count/sum, filter total over threshold. Transformations are filter/group/agg/filter; `show`, `count`, or write triggers execution; groupBy causes shuffle; tests should assert expected customer keys, counts, sums, and no duplicate grain.
2. Join diagnosis: likely inner join or incorrect point-in-time join. Left anti join finds dropped transactions. Reconcile pre/post join counts, unmatched accounts, effective-date misses, and sample dropped records.
3. Performance triage: long-tail tasks suggest skew. Confirm in Spark UI stage/task metrics. Inspect hot keys and partition sizes. Use salting, broadcast, repartitioning, skew hints/AQE, or data model changes, then compare output keys/counts/amounts.
4. Null/date boundaries: null country should be routed to DQ or handled explicitly; blank account should become DQ exception; start date usually inclusive; end date usually exclusive; exact threshold depends on `>` versus `>=` in spec.
5. Tiny rule: posted WIRE rows are the posted wire transactions in the sample, orphan row is the transaction whose account is missing, high-risk filter keeps transactions with high-risk country, customer `c1` alerts because aggregate exceeds threshold, and supporting rows must tie to that alert.
6. Query basics: use half-open June filter, `IS NULL`, explicit null handling, `GROUP BY`, `LEFT ANTI JOIN`, CTEs, `ROW_NUMBER`, deterministic key expression, and supporting transaction selection from the same eligible set.
7. PySpark basics: create explicit schemas, cast dates/decimals, use `filter`, `select`, `withColumn`, `groupBy`, `left_anti`, `Window.partitionBy().orderBy()`, deterministic key construction, and assertions for `c1`, `t1`, and `t2`.

### Final capstone answer shape

A strong capstone proposes ADLS/OneLake bronze ingestion, silver standardized customer/account/transaction/reference tables, gold rule-ready views, Spark/Databricks rule execution, Delta outputs, DQ exception tables, legacy/cloud reconciliation, defect workflow, BI/analytics views, and evidence packs. It explains point-in-time joins, deterministic alert keys, run manifests, rule/version governance, access control, sign-off gates, and a learning plan that starts with domain foundations, then Spark/SQL labs, then DQ/reconciliation and role-specific practice.

Detailed model answer: [`06-practice-lab-retrieval-tests.md#1212-final-capstone-model-answer`](06-practice-lab-retrieval-tests.md#1212-final-capstone-model-answer).

---

## 4. Role Guide Drill Answers

### Data Engineer closed-book drills

1. Bronze preserves landed data, silver standardizes/validates, gold creates rule-ready curated data, and evidence stores run proof and supporting details.
2. Build alert keys from stable fields such as rule ID/version, customer/account, monitoring period, trigger grain, and normalized business keys.
3. Current customer tables are dangerous because they overwrite historical ownership, risk rating, status, and segmentation.
4. Reconcile row count, distinct keys, amount totals, debit/credit totals, eligible count, excluded count, orphan count, duplicate count, alert count, and matched/unmatched legacy keys.
5. Differences can come from source extract, mapping, nulls, dates, thresholds, joins, reference data, duplicates, time zones, or write/rerun behavior.
6. Use Lakeflow expectations for required keys, valid values, reference coverage, quarantine, warning, drop, or fail policies.
7. Rerun one rule/month by parameterizing period/rule, reading immutable inputs, replacing the target partition, using deterministic keys, and reconciling before/after.
8. Debug performance by confirming correctness, checking explain plan, Spark UI, scan size, shuffles, skew, join strategy, partitions, file layout, and then proving unchanged output.
9. Run manifest needs run ID, batch ID, source versions, rule version, parameters, period, code version, counts, DQ results, output locations, status, and owner.
10. A rule is sign-off ready when spec, implementation, golden tests, DQ checks, reconciliation, expected differences, defects, evidence, and approvals are complete.

### Data Analyst / BI closed-book drills

1. Alert count counts generated alerts; eligible population counts records/customers considered; exception rate measures DQ failures; case conversion measures alerts becoming cases or filings depending on definition.
2. Slice by rule, month, customer risk, product, geography, source system, segment, status, investigator outcome, and defect category.
3. Validate by matching metric definition, grain, filters, period, source table, refresh time, row-level security, and reconciliation totals.
4. Investigate a spike by checking rule version, inputs, population, thresholds, reference data, DQ exceptions, duplicates, join changes, and source events.
5. Executive dashboard shows volume, trends, sign-off status, critical DQ/defects, reconciliation status, aging, and high-risk segments.
6. DQ/defect dashboard shows failed checks, severity, affected outputs, owner, SLA, root cause, retest status, and trend.
7. Metric grain is the level represented by each row or number; mixing alert grain with transaction grain creates wrong totals.
8. False-positive rate can mislead when labels are incomplete, reviewer behavior changes, or denominator/exclusions are inconsistent.
9. Audit-ready dashboard shows metric definitions, source lineage, refresh time, filters, rule version, reconciliation status, and drill-through evidence.
10. Delta stores governed tables, Databricks SQL queries them, semantic models define reusable metrics, and Power BI presents controlled visuals.

### QA / DQ Engineer closed-book drills

1. Completeness, validity, accuracy, consistency, uniqueness, timeliness, referential integrity, point-in-time correctness, conformity, and reconciliation.
2. DQ exception is a failed data rule; defect is a confirmed issue requiring ownership, fix, retest, and closure evidence.
3. Golden record is a small known input case with expected output for rule and edge-case validation.
4. Rule test matrix includes eligibility, exclusions, thresholds, windows, joins, nulls, boundaries, duplicates, point-in-time cases, expected alerts, and expected non-alerts.
5. Row counts can pass while amounts, keys, joins, risk ratings, supporting transactions, or alert grain are wrong.
6. Classify mismatches as data, mapping, rule, reference, parameter, environment, timing, expected difference, or unresolved defect.
7. Defect closure needs root cause, impact, fix, retest, reconciliation, samples, approval, and closure note.
8. A run should fail for critical missing inputs, broken referential integrity, invalid parameters, severe completeness gaps, or unapproved output-impacting DQ issues.
9. Lakeflow expectations help QA by making DQ rules executable, observable, and tied to warn/drop/fail/quarantine behavior.
10. QA sign-off requires test coverage, pass/fail evidence, defect closure, reconciliation, expected-difference approval, and release readiness.

### Solution Architect / Lead closed-book drills

1. Architecture flows from sources to ingestion, bronze, silver, gold, rule execution, alerts, evidence, BI, governance, and audit.
2. Bronze preserves, silver standardizes, gold curates, rule execution applies scenarios, and evidence proves why outputs exist.
3. Equivalence proves migration correctness; optimization intentionally changes performance or behavior and needs separate approval.
4. Evidence pack includes spec, inputs, versions, manifests, DQ, reconciliation, alerts, supporting records, defects, approvals, and limitations.
5. Main components include ADLS/OneLake, Data Factory, Databricks, Spark, Delta, Unity Catalog/Purview, Databricks SQL, Power BI, Key Vault, and CI/CD.
6. Readiness checks: data, DQ, reconciliation, security, performance, monitoring, recovery, cost, documentation, and sign-off.
7. Security concerns include least privilege, sensitive data, secrets, workspace access, catalog permissions, row-level access, audit logs, and data exfiltration.
8. Handle mismatch by freezing scope, classifying root cause, sampling records, assigning owner, fixing/retesting or approving difference, and documenting impact.
9. Manage cost with partitioned replay, right-sized compute, autoscaling, job clusters, efficient file layout, scheduling, monitoring, and avoiding unnecessary reruns.
10. Architecture is an operating model when it defines ownership, controls, runbooks, monitoring, sign-off, support, cost, and change governance.

### Business Analyst closed-book drills

1. Ambiguity is a compliance defect (prevents silent unapproved decisions in code); a requirement is done when provable, not when built (prevents acceptance without evidence).
2. A complete rule spec defines population, eligibility, grain, threshold and operator, window and date basis, boundaries, exclusions, effective-dating, outputs, and edge cases.
3. Data literacy floor: grain, the two filter gates, split amounts caught only in aggregate, matching counts can hide wrong evidence, every alert traces to inputs/version/run.
4. The structuring question - "if the customer splits the amount, does this still alert?" - tests gate placement without code.
5. Differences are either expected (rationale, impact, approval, register) or defects (record, root cause, retest, closure); nothing stays unclassified.
6. Acceptance golden records: split-amounts must-alert, ineligible-row contamination, threshold boundaries, mid-period reference change, duplicate and reversal.
7. An approvable sign-off package is a narrative - specified, built, proved, differing, approved - not a folder of files.
8. Compliance owns threshold values; the BA owns making them explicit, versioned, boundary-tested, and traceable.
9. BI reports and validates outcomes; the BA defines required behavior testably and proves the build matches approval.
10. With open requirements: build stable sections, assign owners and dates to open questions, refuse silent policy decisions, escalate timeline pressure as a logged risk decision.

### Data Scientist / ML closed-book drills

1. AML labels are imperfect because investigations are subjective, delayed, policy-dependent, and affected by reviewer capacity.
2. Temporal leakage happens when a feature uses information not available at score time.
3. Observation window builds features, score time is when decision is made, and outcome window captures later result.
4. Accuracy is weak for imbalanced alert data because predicting the majority class can look good while missing useful prioritization.
5. Lift at top K measures how much better the top-ranked alerts are than random selection for reviewer capacity.
6. Features include high-risk country amount/count, distinct countries, recent change in geography, customer baseline deviation, counterparty risk, and velocity windows.
7. Explain score with top contributing factors, historical context, comparable behavior, data freshness, and limitations.
8. MLflow should track data version, feature code, parameters, metrics, model artifacts, explainability outputs, environment, approvals, and lineage.
9. Monitor data drift, feature drift, score distribution, outcome drift, segment performance, reviewer feedback, and pipeline freshness.
10. ML should support rules first because deterministic controls, explainability, governance, and human review remain central in AML/TM.

---

## 5. Spark And SQL Drill Answers

### Spark first-principles drills

1. Expected output before coding prevents accidental implementation-driven definitions.
2. The posted WIRE filter keeps transactions that are both posted and WIRE in the sample dataset.
3. `t6` is a DQ exception because its account key does not resolve to a valid account.
4. `c2` does not alert if its eligible high-risk posted-wire total does not meet the threshold or eligibility conditions.
5. `c1` alerts because its eligible supporting transactions aggregate above the rule threshold.
6. `groupBy` changes grain from transaction rows to group rows such as customer-period.
7. Left anti join returns records with no match, which is ideal for orphan detection.
8. Inner joins can hide defects by dropping unmatched records silently.
9. `country_code <> 'CA'` excludes nulls because SQL three-valued logic treats comparison with null as unknown; adding `OR country_code IS NULL` includes them.
10. `< effective_end_date` avoids double-counting boundary records when adjacent effective periods meet.
11. Deterministic dedupe needs stable partition keys and stable tie-breakers.
12. Supporting transactions should be separate because alert grain differs from transaction grain.
13. Joins, groupBy, distinct, repartition, orderBy, and window operations often cause shuffles.
14. Prove optimization preserved meaning by comparing row counts, keys, sums, samples, and reconciliation before/after.
15. Evidence includes tiny inputs, expected outputs, assertions, DQ exceptions, supporting records, and reconciliation counts.

### PySpark DataFrame basics drills

1. Create DataFrames with explicit schemas for transactions, accounts, and country risk.
2. Use `F.to_date` for transaction date and cast amount to `decimal`.
3. Use `select("transaction_id", "account_id", "amount_cad")`.
4. Use `filter((F.col("status") == "POSTED") & (F.col("transaction_type") == "WIRE"))`.
5. Use `>= "2022-06-01"` and `< "2022-07-01"`.
6. Use `filter(F.col("country_code").isNull())`.
7. Use `.filter(F.col("country_code") != "CA")` and explain null rows are not returned.
8. Use `F.when` / `otherwise` for amount bands.
9. Use `groupBy("transaction_type").count()`.
10. Use `groupBy("account_id").agg(F.sum("amount_cad"))`.
11. Filter the aggregated DataFrame by total amount.
12. Inner join drops transactions whose account is missing.
13. Left join keeps unmatched transactions with null account fields.
14. Left anti join identifies orphan account transactions.
15. Join country risk and filter high-risk reference rows.
16. Use `Window.partitionBy("account_id").orderBy(F.col("transaction_date").desc(), F.col("transaction_id"))`.
17. DQ checks should produce orphan-account and duplicate-transaction exception rows.
18. High-risk June posted-wire alert should aggregate at customer/rule/period grain.
19. Supporting transactions are the eligible transaction rows that explain the alert.
20. Assertions should check counts, alert customer, supporting transaction IDs, orphan rows, and duplicate rows.

### Spark SQL and PySpark deep drills

1. Spark SQL expresses logic in SQL strings; PySpark DataFrame API expresses it in Python objects. Both can compile to Catalyst plans.
2. Transformations build a logical plan; actions execute it.
3. Lazy execution matters because errors/performance only appear when an action triggers the plan.
4. Driver coordinates the application; executors run tasks and store/cache data.
5. Shuffle redistributes data across partitions, often for joins, aggregations, and windows.
6. Narrow transformations keep each output partition dependent on few input partitions; wide transformations require shuffle.
7. Inner joins enrich matched records; left joins preserve input rows; left anti finds DQ orphans; left semi filters to matched keys; full outer reconciles two outputs.
8. Point-in-time join uses business key plus `event_date >= effective_start` and `event_date < effective_end`.
9. Money should use decimals to avoid floating-point rounding errors.
10. Nulls create mismatches because filters, joins, and equality comparisons treat null differently than normal values.
11. Row-based windows count rows; time-based windows use time ranges and need careful date/timestamp semantics.
12. Detect orphans with left anti join from transactions to valid account/customer keys.
13. Data skew means a few keys or partitions hold disproportionate data and slow tasks.
14. AQE can adjust join strategy, coalesce shuffle partitions, and handle skew at runtime.
15. Broadcast a table when it is small enough and avoids expensive shuffle joins.
16. `collect()` can overwhelm driver memory and expose sensitive detail.
17. Cache when reused expensive DataFrames fit memory and repeated actions justify the cost.
18. Deterministic dedupe uses stable keys, ordering, and tie-breakers.
19. Test PySpark with tiny inputs, explicit expected outputs, edge cases, schema checks, and assertions.
20. Prove tuning with before/after reconciliation and invariant checks.

### Spark SQL query basics drills

1. Logical order is `FROM/JOIN`, `WHERE`, `GROUP BY`, aggregates, `HAVING`, `SELECT`, `ORDER BY`, `LIMIT`.
2. `WHERE` filters rows before grouping; `HAVING` filters groups after aggregation.
3. `country_code <> 'CA'` does not return null countries because null comparison is unknown.
4. Posted WIRE rows are those where both `status = 'POSTED'` and `transaction_type = 'WIRE'`.
5. Inner join hides orphan accounts by dropping unmatched rows.
6. Left anti join returns left rows that have no matching right row.
7. GroupBy changes grain from individual rows to one row per group.
8. `COUNT(*)` counts rows; `COUNT(column)` counts non-null values.
9. Tie-breakers make ordering deterministic when multiple rows share the same sort value.
10. `UNION` removes duplicates; `UNION ALL` preserves them.
11. `ROW_NUMBER()` assigns deterministic sequence within a partition when ordering is complete.
12. Latest transaction per account uses `ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY transaction_date DESC, transaction_id)`.
13. Deterministic alert key concatenates stable rule/customer/period/grain fields and hashes them.
14. A left anti join from transactions to accounts proves `t6` is an orphan DQ exception.
15. Supporting transactions are the eligible rows that roll up to `c1`'s alert, such as `t1` and `t2` in the tiny dataset.

### WHERE vs HAVING filter placement drills

Full inline answers live in [`spark/where-having-filter-placement.md`](spark/where-having-filter-placement.md).

1. `WHERE` gates rows before `GROUP BY`; `HAVING` gates groups after aggregates exist, so only `HAVING` can reference `SUM`/`COUNT`.
2. PySpark has no `HAVING` keyword; a `.filter()` before `groupBy()` is the row gate and a `.filter()` after `.agg()` on the aggregate's alias is the group gate. `filter` and `where` are aliases - position, not name, carries the meaning.
3. Putting an aggregate threshold at row level misses structuring: account `a1` wires 60 and 50, each under 100, total 110 - only the group gate catches it.
4. Dropping the row gate can keep the same alert account set while corrupting totals and supporting transactions, so reconcile counts, amounts, and supporting keys, never counts alone.
5. Catalyst pushes row predicates toward the scan and may evaluate a grouping-key-only `HAVING` early, but it never moves an aggregate predicate before grouping; placement defines semantics, the optimizer only changes the physical plan.

### Tech stack closed-book drills

1. Source systems feed ADF/Fabric ingestion into ADLS/OneLake bronze, Databricks/Spark silver/gold, Delta rule outputs, evidence tables, BI, catalog/lineage, and audit packs.
2. ADF moves/orchestrates across services; Lakeflow Jobs orchestrate Databricks tasks; Databricks processing performs Spark transformations and rule execution.
3. Bronze stores raw, silver cleans/conforms, gold curates, alert tables store rule outputs, and evidence tables store proof and drill-through.
4. Unity Catalog matters for centralized permissions, ownership, lineage, discovery, and governance.
5. Managed tables let platform manage storage; external tables reference data in external locations with separate storage ownership.
6. Spark SQL and PySpark share Catalyst optimization for DataFrame/SQL plans.
7. Lazy execution builds plans; transformations are plan steps; actions run jobs; shuffles redistribute data.
8. Prevent row explosion by checking key uniqueness, join grain, effective dates, dedupe, and pre/post join counts.
9. Delta improves on Parquet with transaction log, ACID operations, schema controls, history, and safer reruns.
10. Aggressive vacuum can remove files needed for time travel, rollback, or audit replay.
11. Lakeflow Connect ingests, Declarative Pipelines manage transformations/tables, and Jobs orchestrate workflows.
12. Warn logs issues, drop removes bad records, fail stops the run, and quarantine routes records for review.
13. Triggered mode runs on schedule or demand; continuous mode processes ongoing streaming updates.
14. Trustworthy dashboard has governed definitions, lineage, refresh status, reconciliation, access controls, and drill-through.
15. Validate Power BI by comparing source queries, semantic model filters, row-level security, refresh time, and reconciliation totals.
16. MLflow tracks experiments, parameters, metrics, artifacts, models, environment, and lineage.
17. Label leakage uses future outcome or reviewer information unavailable at score time.
18. Rule migration reconstructs business behavior, not just code syntax.
19. SAS risks include macros/formats/merge behavior; Oracle risks include stored logic/null/date semantics; IMS risks include hierarchy/extract layouts.
20. Sign-off pack includes specs, tests, DQ, reconciliation, defects, expected differences, evidence samples, and approvals.

---

## 6. Study-System Prompt Answers

For `05-make-it-stick-study-system.md`, prompts that ask a coach to withhold answers are interactive study prompts. In this repo, the self-study answer key is:

- Use this file for model answers after the attempt.
- Use [`06-practice-lab-retrieval-tests.md`](06-practice-lab-retrieval-tests.md) for practice prompts.
- Use the relevant role guide or stack guide to repair weak answers.

Meeting decision example, “Use transaction_date for monitoring windows, not posting_date”:

1. If posting date differs by 10 days, the monitoring month/window can change, so reconciliation should compare both date bases and quantify affected records.
2. If legacy used posting date by mistake, classify it as potential expected legacy behavior or defect, document the difference, and get owner approval before changing behavior.
3. Metrics: counts and amounts by transaction month versus posting month, alert counts by rule/month, and matched/unmatched alert keys.
4. Rule spec section: time-window definition, date-field choice, boundary conditions, and approved assumptions.
5. Evidence: code/query condition, rule spec approval, test records, reconciliation output, and supporting sample alerts.

---

## 7. Project Scope Call Prep Answers

1. An informal scope call matters because it often reveals real project expectations, team pain points, ownership boundaries, and fit criteria before a formal process does.
2. The four conversations are project scope, team operating model, data-science/remediation work, and your skill fit.
3. Scope questions should clarify business/control problem, deliverables, in-scope data/systems/periods, sign-off criteria, and explicit exclusions.
4. Operating-model questions should clarify role split, requirement owner, approval owner, tools, defect triage, and recurring checkpoints.
5. Remediation evidence matters because a fix is not complete until root cause, impact, fix, retest, and approval are documented.
6. Avoid assuming model training by asking whether data scientists are doing exploration, feature engineering, validation, monitoring, DQ analysis, remediation analytics, or governed ML.
7. A strong 30-second positioning answer names the problem you help solve, one relevant example, how you clarify scope, and how you produce reviewable evidence.
8. Listen for artifacts such as scope docs, backlog, data inventory, DQ reports, reconciliation outputs, defect tickets, notebooks, dashboards, feature tables, and sign-off checklists.
9. A weak fit answer is a generic tool list. A stronger answer connects your skills to first-month deliverables, data risks, evidence, and team handoffs.
10. A good follow-up note summarizes your understanding of scope, team needs, relevant skills you can contribute, open questions, and agreed next steps without copying private chat wording.
