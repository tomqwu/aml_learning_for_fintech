# AML Learning for Fintech

Public-safe learning system for AML / Transaction Monitoring modernization, Azure Databricks, Spark, SQL, data quality, analytics, ML/data science, and role-based interview readiness.

The repo is meant to be a one-stop learning shop: deep explanations live in `docs/`, runnable Spark/PySpark/SQL labs live in notebooks, and README files stay short so learners can navigate without getting lost.

## Start Here

| Goal | Go to |
|---|---|
| See the full documentation map | [`docs/README.md`](docs/README.md) |
| Learn the AML/TM modernization case study | [`docs/00-research-map.md`](docs/00-research-map.md) |
| Run Spark, PySpark, Spark SQL, and Databricks examples | [`examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb) |
| Prepare by interview role | [`docs/08-interview-knowledge-by-role-and-tech-stack.md`](docs/08-interview-knowledge-by-role-and-tech-stack.md) |
| Learn the tech stack | [`docs/14-tech-stack-reference.md`](docs/14-tech-stack-reference.md) |
| Practice active recall | [`docs/06-practice-lab-retrieval-tests.md`](docs/06-practice-lab-retrieval-tests.md) |
| Set up local Databricks Connect | [`docs/code/databricks-connect-local-setup.md`](docs/code/databricks-connect-local-setup.md) |
| Understand contribution standards for agents | [`AGENTS.md`](AGENTS.md) |

## How To Use This Repo

1. Pick a role path or stack path below.
2. Read the main guide until you can explain the mental model without notes.
3. Run the canonical notebook cells that match the topic.
4. Use the closed-book drills to test recall.
5. When adding new material, keep deep content in dedicated docs and keep README files as maps.

## Role Paths

| Role | Main path | What to master |
|---|---|---|
| Data Engineer | [`docs/09-role-data-engineer.md`](docs/09-role-data-engineer.md) | ingestion, medallion design, Spark, Delta, reruns, DQ, reconciliation |
| Data Analyst / BI | [`docs/10-role-data-analyst-bi.md`](docs/10-role-data-analyst-bi.md) | governed metrics, SQL, dashboards, tie-outs, alert analytics |
| Data Scientist / ML | [`docs/ml/README.md`](docs/ml/README.md) | leakage, labels, feature engineering, explainability, MLflow, model governance |
| QA / DQ Engineer | [`docs/12-role-qa-dq-engineer.md`](docs/12-role-qa-dq-engineer.md) | DQ dimensions, golden records, reconciliation, defect evidence |
| Solution Architect / Lead | [`docs/13-role-solution-architect-lead.md`](docs/13-role-solution-architect-lead.md) | target architecture, controls, NFRs, roadmap, governance, tradeoffs |

## Stack Paths

| Stack or domain | Main path |
|---|---|
| AML / Transaction Monitoring foundations | [`docs/01-aml-transaction-monitoring-foundations.md`](docs/01-aml-transaction-monitoring-foundations.md) |
| 5-year lookback and Azure modernization | [`docs/02-5year-lookback-azure-modernization.md`](docs/02-5year-lookback-azure-modernization.md) |
| Rule migration and spec-as-code | [`docs/03-rule-migration-spec-as-code.md`](docs/03-rule-migration-spec-as-code.md) |
| Data quality, reconciliation, and defects | [`docs/04-data-quality-reconciliation-defect-management.md`](docs/04-data-quality-reconciliation-defect-management.md) |
| Spark SQL and PySpark | [`docs/spark/README.md`](docs/spark/README.md) |
| SQL learning | [`docs/sql/README.md`](docs/sql/README.md) |
| ML and data science | [`docs/ml/README.md`](docs/ml/README.md) |
| Runnable code standards | [`docs/code/README.md`](docs/code/README.md) |
| Source map | [`docs/07-annotated-bibliography.md`](docs/07-annotated-bibliography.md) |

## Runnable Notebook

Use the consolidated Databricks/Spark notebook as the first-class place for executable examples:

[`examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb)

It includes:

- Databricks modernization flow for AML/TM.
- Bronze, silver, and gold table thinking.
- DQ checks and reconciliation.
- Alert generation and evidence tables.
- Delta-style persistence and BI-ready outputs.
- Lakeflow / Jobs thinking.
- Spark SQL versus PySpark practice.
- Focused PySpark DataFrame basics.
- Focused Spark SQL query basics.

Notebook rule:

```text
PySpark, Python, Spark SQL, and PySQL-style learning examples belong in notebooks.
Markdown explains concepts, diagrams, expected outputs, validation logic, Q&A, and drills.
```

## Repository Layout

| Area | Purpose |
|---|---|
| [`docs/`](docs/) | Deep learning guides, role paths, stack references, standards, bibliography |
| [`examples/spark/`](examples/spark/) | Notebook-first runnable Spark/PySpark/SQL examples |
| [`templates/`](templates/) | Reusable templates for rule specs, DQ checks, retrieval sessions, and code bootstraps |
| [`scripts/`](scripts/) | Validation and setup helpers |
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

The lint suite checks Markdown, whitespace, runnable-code policy, notebook structure, notebook code-cell explanations, and README navigation health.

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
