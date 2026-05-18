-- DQ Check Template for AML/TM pipelines
-- Replace placeholders with table, field, and batch details.

-- 1. Required field check
SELECT
    '${CHECK_NAME}' AS check_name,
    batch_id,
    COUNT(*) AS failed_record_count
FROM ${TABLE_NAME}
WHERE ${REQUIRED_FIELD} IS NULL
GROUP BY batch_id;

-- 2. Duplicate business key check
SELECT
    '${DUPLICATE_CHECK_NAME}' AS check_name,
    ${BUSINESS_KEY},
    COUNT(*) AS duplicate_count
FROM ${TABLE_NAME}
GROUP BY ${BUSINESS_KEY}
HAVING COUNT(*) > 1;

-- 3. Referential integrity check
SELECT
    '${RI_CHECK_NAME}' AS check_name,
    t.batch_id,
    COUNT(*) AS orphan_count
FROM ${CHILD_TABLE} t
LEFT JOIN ${PARENT_TABLE} p
  ON t.${FK_FIELD} = p.${PK_FIELD}
WHERE p.${PK_FIELD} IS NULL
GROUP BY t.batch_id;

-- 4. Point-in-time reference coverage check
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

-- 5. Reconciliation control total check
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
