# Changelog

Release notes for the AML Learning for Fintech repository. Versions follow the `version` field in [`package.json`](package.json).

## Unreleased

### Added

- `docs/spark/spark-sql-vs-pyspark-usage-guide.md`: when to use Spark SQL vs the PySpark DataFrame API - the one-engine/two-front-doors model, a ten-situation decision framework, the hybrid pattern with its governance argument, the safe-parameterization rule, AML/TM-mapped key-construct catalogs for both doors (population/eligibility, aggregation, joins and DQ, windows and dedupe, nulls/dates/strings, diagnostics and testing - each construct verified against Spark 4.1.2), per-door failure modes, interview scripts, and closed-book drills with inline model answers. Linked from the Spark and SQL track READMEs, the root README technical-screen path, the profile-fit guide, and the model answer bank.

- `docs/19-role-business-analyst.md`: full Business Analyst role guide at the same depth standard as the other five roles - role scope and ownership boundaries, the translation-layer mental model, rule specs vs user stories, the two filter gates in business language, expected-difference vs defect classification, golden-record acceptance design, artifact catalog, lifecycle playbook, a worked policy-sentence-to-spec example, stack literacy for non-coders, Q&A, common mistakes, and closed-book drills with inline model answers. Wired into the role tables in the root README, docs index, interview index (role list, project story, stack map, depth expectations, cross-role scenario), the profile playbook in doc 18, and the model answer bank.

- Amount-drift case study in `docs/04-data-quality-reconciliation-defect-management.md` (section 11): why a transaction amount changes between bronze, silver, and gold - the conservation-of-amount principle, factor catalogs for each hop (casting, locale parsing, units, signs, dedupe, quarantine, FX rates and rate dates, join explosion and row loss, netting, rounding, reruns), a symptom-to-factor diagnostic table, a worked micro-trace, a control playbook, and new recall drills with inline model answers.
- Notebook **Appendix D - Amount Drift Across Bronze/Silver/Gold Micro-Lab**: self-contained asserted steps proving silent cast loss (1250.40 vanishing on one comma), the conservation identity across dedupe and quarantine, FX conversion as an approved difference, and effective-date join explosion as a defect (verified end to end on PySpark 4.1.2).

## v1.0.0 - 2026-06-11

First tagged release. The repository at this point is a complete one-stop learning system: AML/TM domain foundations, the 5-year lookback case study, five role guides, Spark/SQL/ML learning tracks, a canonical runnable Databricks notebook, templates, and a CI suite that enforces notebook-first code, inline model answers, README navigation health, and public-safety hygiene.

### Added

- `docs/spark/where-having-filter-placement.md`: interview-grade deep dive on `WHERE` vs `HAVING` and PySpark filter placement - the two filter gates as first principles, row traces on the shared tiny dataset, the structuring trap (row filter vs group filter), the missing-row-gate evidence trap, optimizer semantics vs physical plan, interview answer scripts, Q&A bank, and closed-book drills with inline model answers.
- Notebook **Appendix C - WHERE vs HAVING and PySpark Filter Placement Micro-Lab** in `examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`: three asserted steps proving the two filter gates in Spark SQL, the structuring trap, and PySpark placement reconciled against the SQL version (verified end to end on PySpark 4.1.2).
- `docs/18-candidate-profile-fit-interview-drills.md`: profile-fit interview preparation that starts from the candidate's background instead of the target role. Six profile playbooks (general data engineer, SQL/BI analyst, legacy SAS/ETL developer, backend developer, data scientist, business analyst / MBA) with leading questions, traps, strong answer shapes, the technical screen each profile should expect, a "PySQL" vs Spark SQL vs PySpark vocabulary check, a business-profile data literacy floor, and closed-book drills with inline model answers.
- `WHERE` vs `HAVING` filter placement drill answers in `docs/16-model-answer-bank.md`.
- This changelog.

### Changed

- Navigation: the new guides are linked from the root `README.md`, `docs/README.md`, `docs/08-interview-knowledge-by-role-and-tech-stack.md`, `docs/spark/README.md`, `docs/sql/README.md`, and the notebook README, so both the role-first and background-first entry points reach them in one click.
- De-duplication: the scattered `WHERE`/`HAVING` explanations in `docs/spark/spark-sql-query-basics-examples.md`, `docs/spark/pyspark-dataframe-basics-examples.md`, and the equivalence cheat sheet in `docs/spark/spark-sql-pyspark-deep-learning.md` now point to the single canonical deep dive instead of drifting independently.
