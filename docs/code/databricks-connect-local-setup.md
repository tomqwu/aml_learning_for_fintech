# Databricks Connect Local Setup

Use this when VS Code or the Databricks extension reports:

```text
Failed to set up Python environment for Databricks Connect:
databricks-connect package is not installed in the current environment.
```

The fix is not only "install a package." The local Python version and the `databricks-connect` version must match the Databricks Runtime version you connect to.

---

## Quick Fix for This Machine

The default `python` in this workspace is Python 3.14, which is not a supported Databricks Connect Python version for the current supported runtimes.

This machine has Python 3.12 at `/opt/homebrew/bin/python3.12`, so for a Databricks Runtime 17.3 target run:

```bash
PYTHON_BIN=/opt/homebrew/bin/python3.12 \
DATABRICKS_CONNECT_VERSION=17.3 \
bash scripts/setup_databricks_connect.sh
```

If your Databricks cluster uses a different runtime, change `DATABRICKS_CONNECT_VERSION` to that runtime's major/minor version.

After the script finishes, select this interpreter in VS Code:

```text
.venv-databricks-connect/bin/python
```

---

## Version Map

| Databricks Connect version | Compute type | Required local Python |
|---|---|---|
| 18.0 to 18.2 | Cluster / serverless version 5 | 3.12 |
| 17.2 to 17.3 | Cluster / serverless version 4 | 3.12 |
| 16.4 / 16.4.1+ | Cluster / serverless version 3 | 3.12 |
| 15.4 / 15.4.10+ | Cluster / serverless version 2 | 3.11 |
| 14.3 | Cluster | 3.10 |
| 13.3 | Cluster | 3.10 |

Rule of thumb:

```text
Databricks Runtime major.minor == databricks-connect major.minor
```

For example, a Databricks Runtime 17.3 cluster should use:

```bash
pip install "databricks-connect==17.3.*"
```

---

## Why Not Install Into the Default Python?

Do not install `databricks-connect` into a random global Python.

Reasons:

- Databricks Connect has strict Python compatibility requirements.
- The package conflicts with a standalone `pyspark` install.
- VS Code and the Databricks extension need to use the same interpreter where `databricks-connect` is installed.
- A dedicated virtual environment makes the setup repeatable.

---

## Troubleshooting Checklist

1. Confirm the target Databricks Runtime version.
2. Pick the matching local Python version from the table above.
3. Run `scripts/setup_databricks_connect.sh`.
4. Select `.venv-databricks-connect/bin/python` in VS Code.
5. Authenticate through the Databricks extension or Databricks CLI.
6. Re-run the Databricks Connect environment setup.

If you see a PySpark conflict, remove standalone `pyspark` from the Databricks Connect virtual environment. The setup script does this automatically when it detects `pyspark` in that venv.

---

## References

- Microsoft Learn: Databricks Connect usage requirements
- Microsoft Learn: Install Databricks Connect for Python
