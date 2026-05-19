# Code Example Standards

Use this folder for standards and templates that apply to runnable code examples across the repository.

Main standard:

- [`runnable-code-example-standards.md`](runnable-code-example-standards.md)
- [`databricks-connect-local-setup.md`](databricks-connect-local-setup.md)
- [`../../databricks.example.yml`](../../databricks.example.yml)

Template:

- [`../../templates/code_bootstrap_template.md`](../../templates/code_bootstrap_template.md)

Core rule:

```text
PySpark, Python, Spark SQL, and PySQL-style learning examples live in notebooks.
Every code-heavy notebook section starts with a bootstrap.
```

That means:

- environment
- setup code
- tiny input data
- run order
- expected output
- validation checks
- failure meaning
- Markdown links to the runnable notebook cells instead of duplicating them
