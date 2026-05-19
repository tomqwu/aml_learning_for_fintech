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
/Users/tomwu/Projects/aml_learning_for_fintech/.venv-databricks-connect/bin/python
```

Verify the environment:

```bash
.venv-databricks-connect/bin/python --version
.venv-databricks-connect/bin/python -m pip show databricks-connect
```

Expected for the example above:

```text
Python 3.12.x
Name: databricks-connect
Version: 17.3.x
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

### `No matching distribution found for databricks-connect==17.3.*`

If the error lists available versions only up to `16.1.7`, the install is almost certainly running from an unsupported Python interpreter, such as Python 3.14.

Check which Python is running the install:

```bash
python --version
python -m pip index versions databricks-connect | head
```

Then compare with the dedicated Databricks Connect environment:

```bash
.venv-databricks-connect/bin/python --version
.venv-databricks-connect/bin/python -m pip index versions databricks-connect | head
```

For Runtime 17.3, the dedicated environment should use Python 3.12 and should show `17.3.x` versions.

Do not click **Install databricks-connect** while the Databricks extension shows:

```text
Active Environment: .venv (3.14.5)
```

Switch the interpreter to:

```text
.venv-databricks-connect/bin/python
```

Then retry the Databricks Connect setup.

### VS Code Still Says `databricks-connect` Is Not Installed

If the package is installed in `.venv-databricks-connect` but the Databricks extension
still shows:

```text
Failed to set up Python environment for Databricks Connect:
databricks-connect package is not installed in the current environment.
```

the extension is still pinned to a different interpreter. In this repo, the failure
looked like this in the Databricks extension log:

```text
.venv/bin/python -m pip install databricks-connect==17.3.*
```

That is the wrong environment because `.venv` is Python 3.14 on this machine. The
Databricks extension has its own Python environment selector, so changing only
`python.defaultInterpreterPath` may not be enough.

Fix it from VS Code:

1. Open the Command Palette.
2. Run `Databricks: Change Python environment`.
3. Choose `Enter interpreter path...` if the venv is not listed.
4. Paste:

   ```text
   /Users/tomwu/Projects/aml_learning_for_fintech/.venv-databricks-connect/bin/python
   ```

5. Run `Databricks: Refresh python environment status`.
6. Re-run the Databricks Connect setup from the Databricks panel.

Do not click **Install databricks-connect** while the Databricks panel still shows:

```text
Active Environment: .venv (3.14.5)
```

The active environment must be the dedicated Python 3.12 venv:

```text
Active Environment: .venv-databricks-connect
```

If the command palette flow does not update the panel, reload the VS Code window and
run `Databricks: Refresh python environment status` again.

---

## References

- Microsoft Learn: Databricks Connect usage requirements
- Microsoft Learn: Install Databricks Connect for Python
