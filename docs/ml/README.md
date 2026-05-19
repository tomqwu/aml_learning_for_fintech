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
