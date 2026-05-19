# DQ Check Template for AML/TM Pipelines

Use this as a Markdown template for designing DQ and reconciliation checks before implementing them in a Databricks notebook, Lakeflow expectation, or production SQL task.

Replace placeholders such as `${TABLE_NAME}`, `${CHECK_NAME}`, and `${BUSINESS_KEY}` with project-safe names.

---

## 1. Required Field Check

Notebook implementation should calculate failed required-field records by
`batch_id` for `${TABLE_NAME}` where `${REQUIRED_FIELD}` is missing.

Expected evidence:

- check name
- batch ID
- failed record count
- sample failed records when count is greater than zero

---

## 2. Duplicate Business Key Check

Notebook implementation should group `${TABLE_NAME}` by `${BUSINESS_KEY}` and
return keys where the duplicate count is greater than one.

Expected evidence:

- duplicated business key
- duplicate count
- downstream impact assessment

---

## 3. Referential Integrity Check

Notebook implementation should left join `${CHILD_TABLE}` to `${PARENT_TABLE}`
using `${FK_FIELD}` and `${PK_FIELD}`, then count orphan child rows by `batch_id`.

Expected evidence:

- orphan count by batch
- orphan examples
- rule impact if orphan rows are excluded

---

## 4. Point-In-Time Reference Coverage Check

Notebook implementation should left join `${FACT_TABLE}` to `${REFERENCE_TABLE}`
on `${REFERENCE_KEY}` and the effective-date range, then return fact rows that
do not have point-in-time reference coverage.

Expected evidence:

- missing reference key
- business date
- effective-date gap or reference-data defect

---

## 5. Reconciliation Control Total Check

Notebook implementation should compare `${FROM_TABLE}` and `${TO_TABLE}` by
`batch_id`, including row counts, `${AMOUNT_FIELD}` totals, and differences.

Expected evidence:

- source row count and target row count
- source amount total and target amount total
- explained difference
- sign-off owner
