# ML and Data Science Learning Track

Use this folder for ML, data science, model governance, feature engineering, MLflow, alert prioritization, false-positive analysis, and regulated analytics.

## Start Here

| Need | Link |
|---|---|
| Main ML and data science guide | [`aml-ml-data-science-guide.md`](aml-ml-data-science-guide.md) |
| Tech stack reference | [`../14-tech-stack-reference.md`](../14-tech-stack-reference.md) |
| Practice drills | [`../06-practice-lab-retrieval-tests.md`](../06-practice-lab-retrieval-tests.md) |
| Canonical Spark notebook | [`../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb`](../../examples/spark/notebooks/aml_databricks_one_stop_learning.ipynb) |

## Learning Focus

| Area | What to learn |
|---|---|
| Problem framing | which human decision the model supports |
| Labels | quality, timing, bias, and review outcome definitions |
| Features | point-in-time correctness and leakage prevention |
| Evaluation | precision, recall, calibration, ranking quality, segment behavior |
| Explainability | reason codes, feature contribution, reviewer trust |
| MLOps | MLflow tracking, registry evidence, deployment gates, rollback |
| Monitoring | drift, performance decay, policy changes, data pipeline breaks |
| Governance | approval, documentation, model risk, audit evidence |

## Practical Rule

ML in AML/TM should usually start as decision support:

```text
prioritize -> explain -> monitor -> govern -> only then automate
```

Do not frame ML as replacing deterministic rules unless the control owner, model governance process, and monitoring design support that operating model.

## Deep ML Standard

You should be able to answer:

1. What decision is the model supporting?
2. What label is being predicted or ranked?
3. What features are available at decision time?
4. What leakage risks exist?
5. How does performance vary by segment?
6. What evidence is tracked in MLflow or the model evidence pack?
7. What happens when drift appears?
8. What human review or governance remains in the loop?

Answer standard:

- The model supports a specific human decision, usually alert prioritization or reviewer triage.
- Labels are delayed and imperfect, so label definition and bias must be documented.
- Features must be point-in-time and available at score time.
- Leakage, segment performance, explainability, drift, MLflow evidence, approval, and rollback must be covered.
- Human review remains in the loop unless a control owner and model governance process approve a different operating model.

Mental model:

```text
historical evidence -> point-in-time features -> governed experiment
                    -> explainable score -> monitored decision support
```

## Common Shallow Answer To Upgrade

Shallow:

```text
Use ML to reduce false positives.
```

Deeper:

```text
Use ML as governed decision support: define the alert outcome label, build point-in-time features, check leakage, validate precision/recall and segment impact, track experiments in MLflow, explain scores to reviewers, monitor drift, and require approval before changing operational treatment.
```

## Expansion Rule

Keep AML/TM ML, analytics, feature engineering, explainability, and model-governance content here. If a future ML section needs executable PySpark/Python code, put the runnable version in a notebook and link to it from the guide.
