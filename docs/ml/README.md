# ML and Data Science Learning Track

Use this folder for ML, data science, model governance, feature engineering, MLflow, alert prioritization, false-positive analysis, and regulated analytics.

Main guide:

- [`aml-ml-data-science-guide.md`](aml-ml-data-science-guide.md)

Related stack reference:

- [`../14-tech-stack-reference.md`](../14-tech-stack-reference.md)

---

## Learning Focus

This track keeps ML in one place:

- labels and label quality
- temporal leakage
- feature engineering
- imbalanced evaluation
- alert prioritization
- false-positive analysis
- anomaly detection
- explainability
- MLflow and MLOps
- drift monitoring
- governance and approval

---

## Practical Rule

ML in AML/TM should usually start as decision support:

```text
prioritize -> explain -> monitor -> govern -> only then automate
```

Do not frame ML as replacing deterministic rules unless the control owner, model governance process, and monitoring design support that decision.

---

## What Deep ML Learning Means Here

ML depth is not "knows algorithms." In this repo, ML depth means you can explain
how analytics fits inside a regulated monitoring control.

You should be able to answer:

1. What decision is the model supporting?
2. What label is being predicted or ranked?
3. What features are available at decision time?
4. What leakage risks exist?
5. How does performance vary by segment?
6. What evidence is tracked in MLflow or the model evidence pack?
7. What happens when drift appears?
8. What human review or governance remains in the loop?

First-principles mental model:

```text
historical evidence -> point-in-time features -> governed experiment
                    -> explainable score -> monitored decision support
```

AML/TM example:

```text
An alert prioritization model should help reviewers order work. It should not
silently suppress alerts unless governance, validation, monitoring, and policy
approval support that operating model.
```

---

## Depth Checklist

When studying the main ML guide, each topic should connect to:

- business purpose
- feature and label definition
- point-in-time correctness
- leakage prevention
- explainability
- validation metrics
- segment-level behavior
- drift monitoring
- MLflow or model registry evidence
- approval and rollback path

Common shallow answer:

```text
Use ML to reduce false positives.
```

Deeper answer:

```text
Use ML as governed decision support: define the alert outcome label, build
point-in-time features, check leakage, validate precision/recall and segment
impact, track experiments in MLflow, explain scores to reviewers, monitor drift,
and require approval before changing operational treatment.
```
