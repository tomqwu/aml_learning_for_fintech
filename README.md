# AML Learning for Fintech

Public-safe learning system for AML / Transaction Monitoring modernization, Azure Databricks, Spark, SQL, data quality, analytics, ML/data science, and role-based interview readiness.

The repo is meant to be a one-stop learning shop: deep explanations live in `docs/`, runnable Spark/PySpark/SQL labs live in notebooks, and README files stay short so learners can navigate without getting lost.

## Start Here

| Goal | Go to |
|---|---|
| See the full documentation map | [`docs/README.md`](docs/README.md) |
| Learn the AML/TM modernization case study | [`docs/00-research-map.md`](docs/00-research-map.md) |
| Run Spark, PySpark, Spark SQL, and Databricks examples | [`examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb) |
| Pick a guided path | the three sections below: by role, by background, by scenario |
| Set up local Databricks Connect | [`docs/code/databricks-connect-local-setup.md`](docs/code/databricks-connect-local-setup.md) |
| Understand contribution standards for agents | [`AGENTS.md`](AGENTS.md) |
| See what changed in each release | [`CHANGELOG.md`](CHANGELOG.md) |

## How To Use This Repo

1. Pick a guided path below: by role, by background, or by scenario.
2. Read the main guide until you can explain the mental model without notes.
3. Run the canonical notebook cells that match the topic and predict outputs before running.
4. Use the closed-book drills to test recall.
5. Compare against the inline model answers in the same file and repair gaps.
6. When adding new material, keep deep content in dedicated docs and keep README files as maps.

## Path By Role

Every role path starts from the same foundation and shared project story, then specializes. Read in order, run the listed notebook sections, then drill.

| Role | Read in this order | Run | Drill |
|---|---|---|---|
| Data Engineer | 1. [`docs/01`](docs/01-aml-transaction-monitoring-foundations.md) 2. [`docs/02`](docs/02-5year-lookback-azure-modernization.md) 3. [`docs/09`](docs/09-role-data-engineer.md) 4. [`docs/spark/`](docs/spark/README.md) in its read order 5. [`docs/04`](docs/04-data-quality-reconciliation-defect-management.md) | full notebook top to bottom | drills inside each guide, then [`docs/06`](docs/06-practice-lab-retrieval-tests.md) |
| Data Analyst / BI | 1. [`docs/01`](docs/01-aml-transaction-monitoring-foundations.md) 2. [`docs/10`](docs/10-role-data-analyst-bi.md) 3. [`docs/sql/`](docs/sql/README.md) 4. [`docs/spark/spark-sql-query-basics-examples.md`](docs/spark/spark-sql-query-basics-examples.md) 5. [`docs/spark/where-having-filter-placement.md`](docs/spark/where-having-filter-placement.md) | notebook Appendix B, then C | drills inside each guide, then [`docs/06`](docs/06-practice-lab-retrieval-tests.md) |
| Data Scientist / ML | 1. [`docs/01`](docs/01-aml-transaction-monitoring-foundations.md) 2. [`docs/ml/`](docs/ml/README.md) 3. [`docs/ml/aml-ml-data-science-guide.md`](docs/ml/aml-ml-data-science-guide.md) 4. windows and point-in-time sections of [`docs/spark/spark-sql-pyspark-deep-learning.md`](docs/spark/spark-sql-pyspark-deep-learning.md) | notebook Step 12, then Appendix C | drills inside each guide, then [`docs/06`](docs/06-practice-lab-retrieval-tests.md) |
| QA / DQ Engineer | 1. [`docs/01`](docs/01-aml-transaction-monitoring-foundations.md) 2. [`docs/12`](docs/12-role-qa-dq-engineer.md) 3. [`docs/04`](docs/04-data-quality-reconciliation-defect-management.md) including the amount-drift case study 4. golden-record thinking in [`docs/03`](docs/03-rule-migration-spec-as-code.md) | notebook Step 4 (DQ), Step 8 (reconciliation), Appendix D | drills inside each guide, then [`docs/06`](docs/06-practice-lab-retrieval-tests.md) |
| Solution Architect / Lead | 1. [`docs/00`](docs/00-research-map.md) 2. [`docs/02`](docs/02-5year-lookback-azure-modernization.md) 3. [`docs/13`](docs/13-role-solution-architect-lead.md) 4. [`docs/14`](docs/14-tech-stack-reference.md) 5. skim [`docs/03`](docs/03-rule-migration-spec-as-code.md) and [`docs/04`](docs/04-data-quality-reconciliation-defect-management.md) for the controls you must govern | notebook Steps 9-11 and 15 for platform behavior | cross-role scenario in [`docs/08`](docs/08-interview-knowledge-by-role-and-tech-stack.md), then [`docs/06`](docs/06-practice-lab-retrieval-tests.md) |

Role-to-role comparison, depth expectations, and the one-day / three-day / one-week study sequences live in [`docs/08-interview-knowledge-by-role-and-tech-stack.md`](docs/08-interview-knowledge-by-role-and-tech-stack.md).

## Path By Background

If you are preparing from the background you come from rather than the role you target, start with the profile playbooks in [`docs/18-candidate-profile-fit-interview-drills.md`](docs/18-candidate-profile-fit-interview-drills.md), then jump to the technical asset your profile will be screened on.

| Your background | Playbook | Likely technical screen to drill |
|---|---|---|
| General data engineer (no AML) | doc 18, section 3.1 | filter placement: [`docs/spark/where-having-filter-placement.md`](docs/spark/where-having-filter-placement.md) plus notebook Appendix C |
| SQL / BI analyst | doc 18, section 3.2 | Spark SQL basics and PySpark translation: notebook Appendix B, then C |
| Legacy SAS / ETL / mainframe developer | doc 18, section 3.3 | rule migration and equivalence: [`docs/03-rule-migration-spec-as-code.md`](docs/03-rule-migration-spec-as-code.md) |
| Backend / application developer | doc 18, section 3.4 | set thinking and golden records: [`docs/spark/first-principles-examples.md`](docs/spark/first-principles-examples.md) plus notebook Appendix A |
| Data scientist / ML | doc 18, section 3.5 | point-in-time joins and leakage: [`docs/spark/spark-sql-pyspark-deep-learning.md`](docs/spark/spark-sql-pyspark-deep-learning.md) |
| Business analyst / MBA / product-strategy | doc 18, section 3.6 | rule specs in plain language: [`docs/03-rule-migration-spec-as-code.md`](docs/03-rule-migration-spec-as-code.md) and the data literacy floor in doc 18 |

## Path By Scenario

| Your situation | Path |
|---|---|
| Brand new to AML/TM | [`docs/00-research-map.md`](docs/00-research-map.md) then [`docs/01-aml-transaction-monitoring-foundations.md`](docs/01-aml-transaction-monitoring-foundations.md) then pick a role path above |
| Interview tomorrow / this week | study sequences in [`docs/08-interview-knowledge-by-role-and-tech-stack.md`](docs/08-interview-knowledge-by-role-and-tech-stack.md), section 8 |
| Technical screen on SQL / PySpark / "PySQL" | [`docs/spark/where-having-filter-placement.md`](docs/spark/where-having-filter-placement.md), then notebook Appendices B, A, C and Step 14 |
| Asked to explain why totals changed between layers | amount-drift case study in [`docs/04-data-quality-reconciliation-defect-management.md`](docs/04-data-quality-reconciliation-defect-management.md), section 11, then notebook Appendix D |
| Informal scope or team-fit call | [`docs/17-project-scope-call-prep.md`](docs/17-project-scope-call-prep.md) |
| Recruiter probing your background fit | [`docs/18-candidate-profile-fit-interview-drills.md`](docs/18-candidate-profile-fit-interview-drills.md) |
| Want runnable practice only | the canonical notebook top to bottom, with [`docs/spark/README.md`](docs/spark/README.md) as the companion |
| Want a study method, not just content | [`docs/05-make-it-stick-study-system.md`](docs/05-make-it-stick-study-system.md), then [`docs/06-practice-lab-retrieval-tests.md`](docs/06-practice-lab-retrieval-tests.md) with [`docs/16-model-answer-bank.md`](docs/16-model-answer-bank.md) and [`templates/retrieval_session_template.md`](templates/retrieval_session_template.md) |
| Converting your own notes or meetings into learning assets | [`templates/meeting_to_memory_converter.md`](templates/meeting_to_memory_converter.md) and [`docs/15-learning-depth-standard.md`](docs/15-learning-depth-standard.md) |

## Canonical Notebook Map

One notebook carries all runnable learning: [`examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb). Run it top to bottom; every code cell is preceded by an explanation and validated by assertions.

| Section | What it teaches |
|---|---|
| Steps 0-13 | Databricks modernization flow: parameters, bronze/silver/gold, DQ checks, alerts and evidence, reconciliation, Delta-style persistence, BI views, Lakeflow/Jobs thinking, ML feature readiness, performance hooks |
| Step 14 | the same AML rule in Spark SQL and PySpark, reconciled |
| Step 15 | final validation scorecard |
| Appendix A | focused PySpark DataFrame basics |
| Appendix B | focused Spark SQL query basics |
| Appendix C | WHERE vs HAVING and PySpark filter placement, including the structuring trap |
| Appendix D | amount drift across bronze/silver/gold: cast loss, conservation identity, FX, join explosion |

## Stack Paths

| Stack or domain | Main path |
|---|---|
| AML / Transaction Monitoring foundations | [`docs/01-aml-transaction-monitoring-foundations.md`](docs/01-aml-transaction-monitoring-foundations.md) |
| 5-year lookback and Azure modernization | [`docs/02-5year-lookback-azure-modernization.md`](docs/02-5year-lookback-azure-modernization.md) |
| Rule migration and spec-as-code | [`docs/03-rule-migration-spec-as-code.md`](docs/03-rule-migration-spec-as-code.md) |
| Data quality, reconciliation, and defects | [`docs/04-data-quality-reconciliation-defect-management.md`](docs/04-data-quality-reconciliation-defect-management.md) |
| Azure, Databricks, Delta, Lakeflow, BI, MLflow reference | [`docs/14-tech-stack-reference.md`](docs/14-tech-stack-reference.md) |
| Spark SQL and PySpark | [`docs/spark/README.md`](docs/spark/README.md) |
| SQL learning | [`docs/sql/README.md`](docs/sql/README.md) |
| ML and data science | [`docs/ml/README.md`](docs/ml/README.md) |
| Runnable code standards | [`docs/code/README.md`](docs/code/README.md) |
| Source map | [`docs/07-annotated-bibliography.md`](docs/07-annotated-bibliography.md) |
| Cross-repo model answer index | [`docs/16-model-answer-bank.md`](docs/16-model-answer-bank.md) |

## Repository Layout

| Area | Purpose |
|---|---|
| [`docs/`](docs/) | Deep learning guides, role paths, stack references, standards, bibliography |
| [`examples/spark/`](examples/spark/) | Notebook-first runnable Spark/PySpark/SQL examples |
| [`templates/`](templates/) | Reusable templates for rule specs, DQ checks, retrieval sessions, and code bootstraps |
| [`scripts/`](scripts/) | Validation and setup helpers |
| [`CHANGELOG.md`](CHANGELOG.md) | Release notes per version |
| [`databricks.example.yml`](databricks.example.yml) | Sanitized local Databricks bundle template |
| [`.github/workflows/docs-ci.yml`](.github/workflows/docs-ci.yml) | CI validation for docs and notebooks |

## Navigation Standard

This repo uses a simple structure so it can grow:

- README files are short maps for the directory they sit in.
- Deep explanations belong in numbered docs, role guides, stack guides, or notebooks.
- Runnable PySpark/Python/Spark SQL/PySQL examples belong in notebooks.
- Long reference lists belong in [`docs/07-annotated-bibliography.md`](docs/07-annotated-bibliography.md).
- Future agents should follow [`docs/15-learning-depth-standard.md`](docs/15-learning-depth-standard.md) before expanding any guide.

The structure is based on three documentation principles: help users get started quickly, use relative links for repo navigation, and separate tutorials, how-to guidance, reference, and explanation when the repo grows.

## Validation

Install dependencies once:

```bash
npm install
```

Run the full validation suite:

```bash
npm run lint
git diff --check
```

The lint suite checks Markdown, whitespace, runnable-code policy, notebook structure, notebook code-cell explanations, README navigation health, answer-key coverage, and public-safety hygiene.

## Public-Safety Rules

Do not commit:

- screenshots
- personal names from private notes
- private chat content
- confidential project wording
- production credentials
- real customer data
- proprietary rule logic
- evasion guidance or instructions for hiding suspicious activity

Use generic, public-safe case-study language and synthetic data only.

## Adding New Learning Material

When a new source, note, screenshot summary, job description, or project hint arrives:

1. Sanitize it into public-safe learning facts.
2. Add depth to the correct existing guide instead of creating scattered duplicates.
3. Add a new file only when the topic deserves a durable home.
4. Add or update source references in [`docs/07-annotated-bibliography.md`](docs/07-annotated-bibliography.md).
5. Put runnable PySpark/Python/Spark SQL/PySQL examples in notebooks.
6. Run validation, commit, and push.
