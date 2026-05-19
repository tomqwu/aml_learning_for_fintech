# DQ Check Template for AML/TM Pipelines

Use this as a Markdown template for designing DQ and reconciliation checks before implementing them in a Databricks notebook, Lakeflow expectation, or production SQL task.

Replace placeholders such as `${TABLE_NAME}`, `${CHECK_NAME}`, and `${BUSINESS_KEY}` with project-safe names.

---

## 1. Required Field Check

```sql
SELECT
    '${CHECK_NAME}' AS check_name,
    batch_id,
    COUNT(*) AS failed_record_count
FROM ${TABLE_NAME}
WHERE ${REQUIRED_FIELD} IS NULL
GROUP BY batch_id;
```

Expected evidence:

- check name
- batch ID
- failed record count
- sample failed records when count is greater than zero

---

## 2. Duplicate Business Key Check

```sql
SELECT
    '${DUPLICATE_CHECK_NAME}' AS check_name,
    ${BUSINESS_KEY},
    COUNT(*) AS duplicate_count
FROM ${TABLE_NAME}
GROUP BY ${BUSINESS_KEY}
HAVING COUNT(*) > 1;
```

Expected evidence:

- duplicated business key
- duplicate count
- downstream impact assessment

---

## 3. Referential Integrity Check

```sql
SELECT
    '${RI_CHECK_NAME}' AS check_name,
    t.batch_id,
    COUNT(*) AS orphan_count
FROM ${CHILD_TABLE} t
LEFT JOIN ${PARENT_TABLE} p
  ON t.${FK_FIELD} = p.${PK_FIELD}
WHERE p.${PK_FIELD} IS NULL
GROUP BY t.batch_id;
```

Expected evidence:

- orphan count by batch
- orphan examples
- rule impact if orphan rows are excluded

---

## 4. Point-In-Time Reference Coverage Check

```sql
SELECT
    '${PIT_CHECK_NAME}' AS check_name,
    t.${BUSINESS_KEY},
    t.${REFERENCE_KEY},
    t.${BUSINESS_DATE}
FROM ${FACT_TABLE} t
LEFT JOIN ${REFERENCE_TABLE} r
  ON t.${REFERENCE_KEY} = r.${REFERENCE_KEY}
 AND t.${BUSINESS_DATE} BETWEEN r.effective_start_date AND r.effective_end_date
WHERE r.${REFERENCE_KEY} IS NULL;
```

Expected evidence:

- missing reference key
- business date
- effective-date gap or reference-data defect

---

## 5. Reconciliation Control Total Check

```sql
WITH from_stage AS (
    SELECT batch_id, COUNT(*) AS row_count, SUM(${AMOUNT_FIELD}) AS amount_total
    FROM ${FROM_TABLE}
    GROUP BY batch_id
), to_stage AS (
    SELECT batch_id, COUNT(*) AS row_count, SUM(${AMOUNT_FIELD}) AS amount_total
    FROM ${TO_TABLE}
    GROUP BY batch_id
)
SELECT
    f.batch_id,
    f.row_count AS from_row_count,
    t.row_count AS to_row_count,
    f.row_count - t.row_count AS row_count_difference,
    f.amount_total AS from_amount_total,
    t.amount_total AS to_amount_total,
    f.amount_total - t.amount_total AS amount_difference
FROM from_stage f
JOIN to_stage t
  ON f.batch_id = t.batch_id;
```

Expected evidence:

- source row count and target row count
- source amount total and target amount total
- explained difference
- sign-off owner
