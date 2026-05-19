# Documentation Index

Use this page as the map for the repo's deep learning material. README files should point you to the right place; the linked docs and notebooks do the teaching.

## Start And Orientation

| Need | Link |
|---|---|
| Understand the knowledge landscape | [`00-research-map.md`](00-research-map.md) |
| Learn the study system | [`05-make-it-stick-study-system.md`](05-make-it-stick-study-system.md) |
| Practice recall and what-if drills | [`06-practice-lab-retrieval-tests.md`](06-practice-lab-retrieval-tests.md) |
| Prepare for informal scope/team-fit calls | [`17-project-scope-call-prep.md`](17-project-scope-call-prep.md) |
| Compare practice answers | [`16-model-answer-bank.md`](16-model-answer-bank.md) |
| Check source references | [`07-annotated-bibliography.md`](07-annotated-bibliography.md) |

## Domain Foundations

| Topic | Link |
|---|---|
| AML / Transaction Monitoring basics | [`01-aml-transaction-monitoring-foundations.md`](01-aml-transaction-monitoring-foundations.md) |
| 5-year lookback and Azure modernization | [`02-5year-lookback-azure-modernization.md`](02-5year-lookback-azure-modernization.md) |
| Rule migration and spec-as-code | [`03-rule-migration-spec-as-code.md`](03-rule-migration-spec-as-code.md) |
| DQ, reconciliation, and defect management | [`04-data-quality-reconciliation-defect-management.md`](04-data-quality-reconciliation-defect-management.md) |

## Role Guides

| Role | Link |
|---|---|
| Role and stack interview index | [`08-interview-knowledge-by-role-and-tech-stack.md`](08-interview-knowledge-by-role-and-tech-stack.md) |
| Data Engineer | [`09-role-data-engineer.md`](09-role-data-engineer.md) |
| Data Analyst / BI | [`10-role-data-analyst-bi.md`](10-role-data-analyst-bi.md) |
| Data Scientist / ML | [`ml/README.md`](ml/README.md) |
| QA / DQ Engineer | [`12-role-qa-dq-engineer.md`](12-role-qa-dq-engineer.md) |
| Solution Architect / Lead | [`13-role-solution-architect-lead.md`](13-role-solution-architect-lead.md) |

## Stack Tracks

| Stack | Link |
|---|---|
| Azure, Databricks, Spark, Delta, Lakeflow, BI, MLflow | [`14-tech-stack-reference.md`](14-tech-stack-reference.md) |
| Spark SQL and PySpark | [`spark/README.md`](spark/README.md) |
| SQL | [`sql/README.md`](sql/README.md) |
| ML and data science | [`ml/README.md`](ml/README.md) |
| Runnable-code standards and Databricks Connect setup | [`code/README.md`](code/README.md) |
| Sanitized Databricks bundle template | [`../databricks.example.yml`](../databricks.example.yml) |

## Runnable Labs

| Lab | Link |
|---|---|
| Canonical Databricks/Spark/PySpark/SQL notebook | [`../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb) |
| Spark examples folder | [`../examples/spark/`](../examples/spark/) |
| Notebook README | [`../examples/spark/notebooks/README.md`](../examples/spark/notebooks/README.md) |

## Standards And Templates

| Asset | Link |
|---|---|
| Learning depth standard | [`15-learning-depth-standard.md`](15-learning-depth-standard.md) |
| Model answer bank | [`16-model-answer-bank.md`](16-model-answer-bank.md) |
| Runnable code example standard | [`code/runnable-code-example-standards.md`](code/runnable-code-example-standards.md) |
| Rule spec template | [`../templates/rule_spec_template.yaml`](../templates/rule_spec_template.yaml) |
| DQ check template | [`../templates/dq_check_template.md`](../templates/dq_check_template.md) |
| Code bootstrap template | [`../templates/code_bootstrap_template.md`](../templates/code_bootstrap_template.md) |
| Retrieval session template | [`../templates/retrieval_session_template.md`](../templates/retrieval_session_template.md) |
| Meeting-to-memory converter | [`../templates/meeting_to_memory_converter.md`](../templates/meeting_to_memory_converter.md) |

## Where New Content Goes

| New material | Put it here |
|---|---|
| AML concepts, monitoring lifecycle, or reporting controls | `01-aml-transaction-monitoring-foundations.md` |
| Azure, Fabric, Databricks, or lookback architecture | `02-5year-lookback-azure-modernization.md` or `14-tech-stack-reference.md` |
| Rule migration, spec design, or equivalence testing | `03-rule-migration-spec-as-code.md` |
| DQ checks, reconciliation, defects, or evidence packs | `04-data-quality-reconciliation-defect-management.md` |
| Spark SQL, PySpark, or Spark execution theory | `spark/` plus the canonical notebook |
| SQL learning that is not Spark-specific | `sql/` |
| ML, analytics, feature engineering, or model governance | `ml/` |
| Interview prep | the matching role guide plus `08-interview-knowledge-by-role-and-tech-stack.md` |
| Runnable PySpark/Python/Spark SQL/PySQL code | `../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb` |

## Maintenance Rule

If a README starts explaining a topic in depth, move that explanation into a guide and leave the README as a linkable map. The goal is simple navigation on the first click and serious learning on the second.
