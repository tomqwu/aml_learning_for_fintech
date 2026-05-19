# 17 - Spark SQL Query Basics With AML/TM Examples

This is a code-heavy Spark SQL learning guide for AML / Transaction Monitoring work.

Use it when you want query basics from first principles:

```text
What rows do I start with?
What rows survive?
What columns are created?
What grain does the result have?
What evidence proves the query is correct?
```

Companion runnable file:

- `examples/spark/aml_query_basics_examples.sql`

Runnable contract:

- Run the companion SQL file top to bottom in Databricks SQL or a Spark SQL notebook.
- It creates its own temp views.
- Each numbered query can run after setup.
- The final validation section should return `PASS` for all checks.

Code Bootstrap:

```text
Run examples/spark/aml_sql_bootstrap.sql first if you want only the shared setup and validation.
Run examples/spark/aml_query_basics_examples.sql top to bottom if you want setup plus all query examples.
```

---

## 1. Tiny tables used in the examples

### transactions

| transaction_id | account_id | transaction_date | amount_cad | transaction_type | status | country_code |
|---|---|---|---:|---|---|---|
| t1 | a1 | 2022-06-01 | 60.00 | WIRE | POSTED | IR |
| t2 | a1 | 2022-06-03 | 50.00 | WIRE | POSTED | IR |
| t3 | a1 | 2022-06-05 | 10.00 | CARD | POSTED | CA |
| t4 | a2 | 2022-06-02 | 200.00 | WIRE | POSTED | CA |
| t5 | a3 | 2022-06-02 | 20.00 | WIRE | REVERSED | IR |
| t6 | a9 | 2022-06-02 | 80.00 | WIRE | POSTED | IR |
| t7 | a2 | 2022-07-01 | 300.00 | WIRE | POSTED | IR |
| t8 | a4 | 2022-06-10 | 100.00 | CASH | POSTED | null |

### accounts

| account_id | customer_id | account_status | product_type |
|---|---|---|---|
| a1 | c1 | ACTIVE | CHECKING |
| a2 | c2 | ACTIVE | CHECKING |
| a3 | c3 | ACTIVE | SAVINGS |
| a4 | c4 | CLOSED | CHECKING |

### country_risk

| country_code | risk_level |
|---|---|
| IR | HIGH |
| CA | LOW |
| US | LOW |

---

## 2. First principle: every query has a logical order

SQL is written like this:

```sql
SELECT ...
FROM ...
WHERE ...
GROUP BY ...
HAVING ...
ORDER BY ...
LIMIT ...
```

But the mental order is closer to:

```text
FROM       choose rows/tables
JOIN       attach related rows
WHERE      filter rows
GROUP BY   collapse rows into groups
HAVING     filter groups
SELECT     choose/create columns
ORDER BY   sort final result
LIMIT      keep final top rows
```

This matters because:

```text
WHERE filters rows before aggregation.
HAVING filters groups after aggregation.
SELECT aliases usually cannot be used in WHERE.
GROUP BY changes the grain.
```

---

## 3. Setup query

Use this setup in Spark SQL or Databricks SQL.

```sql
CREATE OR REPLACE TEMP VIEW transactions AS
SELECT * FROM VALUES
  ('t1', 'a1', DATE '2022-06-01', CAST(60.00 AS DECIMAL(18,2)),  'WIRE', 'POSTED',   'IR'),
  ('t2', 'a1', DATE '2022-06-03', CAST(50.00 AS DECIMAL(18,2)),  'WIRE', 'POSTED',   'IR'),
  ('t3', 'a1', DATE '2022-06-05', CAST(10.00 AS DECIMAL(18,2)),  'CARD', 'POSTED',   'CA'),
  ('t4', 'a2', DATE '2022-06-02', CAST(200.00 AS DECIMAL(18,2)), 'WIRE', 'POSTED',   'CA'),
  ('t5', 'a3', DATE '2022-06-02', CAST(20.00 AS DECIMAL(18,2)),  'WIRE', 'REVERSED', 'IR'),
  ('t6', 'a9', DATE '2022-06-02', CAST(80.00 AS DECIMAL(18,2)),  'WIRE', 'POSTED',   'IR'),
  ('t7', 'a2', DATE '2022-07-01', CAST(300.00 AS DECIMAL(18,2)), 'WIRE', 'POSTED',   'IR'),
  ('t8', 'a4', DATE '2022-06-10', CAST(100.00 AS DECIMAL(18,2)), 'CASH', 'POSTED',   NULL)
AS transactions(
  transaction_id,
  account_id,
  transaction_date,
  amount_cad,
  transaction_type,
  status,
  country_code
);

CREATE OR REPLACE TEMP VIEW accounts AS
SELECT * FROM VALUES
  ('a1', 'c1', 'ACTIVE', 'CHECKING'),
  ('a2', 'c2', 'ACTIVE', 'CHECKING'),
  ('a3', 'c3', 'ACTIVE', 'SAVINGS'),
  ('a4', 'c4', 'CLOSED', 'CHECKING')
AS accounts(account_id, customer_id, account_status, product_type);

CREATE OR REPLACE TEMP VIEW country_risk AS
SELECT * FROM VALUES
  ('IR', 'HIGH'),
  ('CA', 'LOW'),
  ('US', 'LOW')
AS country_risk(country_code, risk_level);
```

---

## 4. SELECT basics

### Example 1: Select all columns

```sql
SELECT *
FROM transactions;
```

Use for exploration, not production reporting. Production queries should usually name columns explicitly.

### Example 2: Select specific columns

```sql
SELECT
  transaction_id,
  account_id,
  amount_cad
FROM transactions;
```

Expected grain:

```text
one row per transaction
```

### Example 3: Rename columns with aliases

```sql
SELECT
  transaction_id AS txn_id,
  account_id AS acct_id,
  amount_cad AS amount
FROM transactions;
```

### Example 4: Create a derived column

```sql
SELECT
  transaction_id,
  amount_cad,
  amount_cad * 1.13 AS amount_with_buffer
FROM transactions;
```

### Example 5: Add a constant column

```sql
SELECT
  transaction_id,
  amount_cad,
  'TM_TRAINING' AS source_label
FROM transactions;
```

### Example 6: Select distinct values

```sql
SELECT DISTINCT transaction_type
FROM transactions;
```

Expected values:

```text
WIRE, CARD, CASH
```

### Example 7: Distinct combinations

```sql
SELECT DISTINCT
  transaction_type,
  status
FROM transactions;
```

Distinct applies to the full selected combination, not one column at a time.

---

## 5. WHERE basics

### Example 8: Filter posted transactions

```sql
SELECT *
FROM transactions
WHERE status = 'POSTED';
```

Manual expected rows:

```text
t1,t2,t3,t4,t6,t7,t8
```

### Example 9: Filter WIRE transactions

```sql
SELECT *
FROM transactions
WHERE transaction_type = 'WIRE';
```

Manual expected rows:

```text
t1,t2,t4,t5,t6,t7
```

### Example 10: Combine filters with AND

```sql
SELECT *
FROM transactions
WHERE status = 'POSTED'
  AND transaction_type = 'WIRE';
```

Manual expected rows:

```text
t1,t2,t4,t6,t7
```

### Example 11: Combine filters with OR

```sql
SELECT *
FROM transactions
WHERE transaction_type = 'WIRE'
   OR transaction_type = 'CASH';
```

Manual expected rows:

```text
t1,t2,t4,t5,t6,t7,t8
```

### Example 12: Use IN

```sql
SELECT *
FROM transactions
WHERE transaction_type IN ('WIRE', 'CASH');
```

Same logical result as Example 11.

### Example 13: Use NOT IN

```sql
SELECT *
FROM transactions
WHERE transaction_type NOT IN ('CARD', 'CASH');
```

Expected:

```text
WIRE transactions only
```

### Example 14: Amount threshold

```sql
SELECT *
FROM transactions
WHERE amount_cad > 100;
```

Manual expected rows:

```text
t4,t7
```

### Example 15: Boundary condition

```sql
SELECT *
FROM transactions
WHERE amount_cad >= 100;
```

Manual expected rows:

```text
t4,t7,t8
```

Learning point:

```text
> 100 and >= 100 are different rule behaviors.
Always test threshold boundaries.
```

### Example 16: Date range

```sql
SELECT *
FROM transactions
WHERE transaction_date BETWEEN DATE '2022-06-01' AND DATE '2022-06-30';
```

Expected:

```text
all rows except t7
```

### Example 17: Safer month filter

```sql
SELECT *
FROM transactions
WHERE transaction_date >= DATE '2022-06-01'
  AND transaction_date <  DATE '2022-07-01';
```

This pattern avoids timestamp-end-of-day bugs when using timestamps.

---

## 6. NULL basics

### Example 18: Find null country codes

```sql
SELECT *
FROM transactions
WHERE country_code IS NULL;
```

Expected:

```text
t8
```

### Example 19: Find non-null country codes

```sql
SELECT *
FROM transactions
WHERE country_code IS NOT NULL;
```

Expected:

```text
t1,t2,t3,t4,t5,t6,t7
```

### Example 20: Null trap

```sql
SELECT *
FROM transactions
WHERE country_code <> 'CA';
```

Expected:

```text
t1,t2,t5,t6,t7
```

Why not `t8`?

```text
t8 country_code is null.
null <> 'CA' is unknown, not true.
WHERE keeps true rows only.
```

### Example 21: Include null explicitly

```sql
SELECT *
FROM transactions
WHERE country_code <> 'CA'
   OR country_code IS NULL;
```

Expected:

```text
t1,t2,t5,t6,t7,t8
```

### Example 22: Replace null for display

```sql
SELECT
  transaction_id,
  COALESCE(country_code, 'UNKNOWN') AS country_code_display
FROM transactions;
```

Warning:

Use `COALESCE` for display or explicit business logic. Do not hide data quality issues by replacing nulls silently.

---

## 7. ORDER BY and LIMIT

### Example 23: Largest transactions first

```sql
SELECT
  transaction_id,
  amount_cad
FROM transactions
ORDER BY amount_cad DESC;
```

### Example 24: Top 3 transactions

```sql
SELECT
  transaction_id,
  amount_cad
FROM transactions
ORDER BY amount_cad DESC
LIMIT 3;
```

Expected:

```text
t7 = 300
t4 = 200
t8 = 100
```

### Example 25: Stable ordering

```sql
SELECT
  transaction_id,
  amount_cad,
  transaction_date
FROM transactions
ORDER BY amount_cad DESC, transaction_id ASC;
```

Use tie-breakers when outputs must be reproducible.

---

## 8. CASE expressions

### Example 26: Create amount bands

```sql
SELECT
  transaction_id,
  amount_cad,
  CASE
    WHEN amount_cad >= 200 THEN 'LARGE'
    WHEN amount_cad >= 100 THEN 'MEDIUM'
    ELSE 'SMALL'
  END AS amount_band
FROM transactions;
```

### Example 27: Create eligibility flag

```sql
SELECT
  transaction_id,
  CASE
    WHEN status = 'POSTED' AND transaction_type = 'WIRE' THEN true
    ELSE false
  END AS is_posted_wire
FROM transactions;
```

### Example 28: Reason code

```sql
SELECT
  transaction_id,
  CASE
    WHEN country_code IS NULL THEN 'MISSING_COUNTRY'
    WHEN status <> 'POSTED' THEN 'NOT_POSTED'
    WHEN transaction_type <> 'WIRE' THEN 'NOT_WIRE'
    ELSE 'ELIGIBLE_CANDIDATE'
  END AS eligibility_reason
FROM transactions;
```

This kind of query is excellent for debugging rule eligibility.

---

## 9. String functions

### Example 29: Trim and uppercase

```sql
SELECT
  transaction_id,
  UPPER(TRIM(account_id)) AS account_id_norm
FROM transactions;
```

### Example 30: Concatenate business key

```sql
SELECT
  CONCAT_WS('|', account_id, transaction_id) AS transaction_business_key
FROM transactions;
```

### Example 31: Hash alert key

```sql
SELECT
  SHA2(CONCAT_WS('|', 'TM001', '1.0.0', '2022-06', account_id), 256) AS alert_key_candidate,
  account_id
FROM transactions;
```

### Example 32: Pattern match

```sql
SELECT *
FROM transactions
WHERE transaction_id LIKE 't%';
```

### Example 33: Normalize blank values

```sql
SELECT
  transaction_id,
  NULLIF(TRIM(country_code), '') AS country_code_clean
FROM transactions;
```

---

## 10. Date functions

### Example 34: Extract month

```sql
SELECT
  transaction_id,
  DATE_FORMAT(transaction_date, 'yyyy-MM') AS transaction_month
FROM transactions;
```

### Example 35: Month start

```sql
SELECT
  transaction_id,
  DATE_TRUNC('MONTH', transaction_date) AS transaction_month_start
FROM transactions;
```

### Example 36: Add and subtract days

```sql
SELECT
  transaction_id,
  transaction_date,
  DATE_SUB(transaction_date, 29) AS rolling_30_day_start,
  DATE_ADD(transaction_date, 1) AS next_day
FROM transactions;
```

### Example 37: Days between

```sql
SELECT
  transaction_id,
  DATEDIFF(DATE '2022-07-01', transaction_date) AS days_before_july
FROM transactions;
```

### Example 38: June 2022 processing month

```sql
SELECT *
FROM transactions
WHERE transaction_date >= DATE '2022-06-01'
  AND transaction_date <  DATE '2022-07-01';
```

Use this pattern constantly in AML batch jobs.

---

## 11. Aggregation basics

### Example 39: Count all rows

```sql
SELECT COUNT(*) AS row_count
FROM transactions;
```

Expected:

```text
8
```

### Example 40: Count by transaction type

```sql
SELECT
  transaction_type,
  COUNT(*) AS row_count
FROM transactions
GROUP BY transaction_type;
```

Expected:

```text
WIRE = 6
CARD = 1
CASH = 1
```

### Example 41: Sum by account

```sql
SELECT
  account_id,
  SUM(amount_cad) AS total_amount_cad
FROM transactions
GROUP BY account_id;
```

Result grain:

```text
one row per account
```

### Example 42: Multiple aggregations

```sql
SELECT
  account_id,
  COUNT(*) AS txn_count,
  SUM(amount_cad) AS total_amount_cad,
  AVG(amount_cad) AS avg_amount_cad,
  MAX(amount_cad) AS max_amount_cad
FROM transactions
GROUP BY account_id;
```

### Example 43: Distinct count

```sql
SELECT
  COUNT(DISTINCT account_id) AS distinct_account_count
FROM transactions;
```

Expected:

```text
5, because a1,a2,a3,a4,a9 appear.
```

### Example 44: Conditional aggregation

```sql
SELECT
  account_id,
  SUM(CASE WHEN transaction_type = 'WIRE' THEN amount_cad ELSE 0 END) AS wire_amount_cad,
  COUNT(CASE WHEN transaction_type = 'WIRE' THEN 1 END) AS wire_count
FROM transactions
GROUP BY account_id;
```

### Example 45: Posted wire amount by account

```sql
SELECT
  account_id,
  SUM(CASE
        WHEN status = 'POSTED' AND transaction_type = 'WIRE' THEN amount_cad
        ELSE 0
      END) AS posted_wire_amount_cad
FROM transactions
GROUP BY account_id;
```

---

## 12. HAVING basics

### Example 46: Accounts above total amount threshold

```sql
SELECT
  account_id,
  SUM(amount_cad) AS total_amount_cad
FROM transactions
GROUP BY account_id
HAVING SUM(amount_cad) > 100;
```

Why `HAVING`?

```text
WHERE filters rows before grouping.
HAVING filters groups after grouping.
```

### Example 47: Accounts with at least two transactions

```sql
SELECT
  account_id,
  COUNT(*) AS txn_count
FROM transactions
GROUP BY account_id
HAVING COUNT(*) >= 2;
```

Expected:

```text
a1 and a2
```

---

## 13. JOIN basics

### Example 48: Inner join transactions to accounts

```sql
SELECT
  t.transaction_id,
  t.account_id,
  a.customer_id
FROM transactions t
JOIN accounts a
  ON t.account_id = a.account_id;
```

What happens:

```text
t6 drops because account_id a9 is not in accounts.
```

### Example 49: Left join preserves transaction rows

```sql
SELECT
  t.transaction_id,
  t.account_id,
  a.customer_id
FROM transactions t
LEFT JOIN accounts a
  ON t.account_id = a.account_id;
```

What happens:

```text
t6 remains with customer_id = null.
```

### Example 50: Find orphan accounts with left anti join

```sql
SELECT t.*
FROM transactions t
LEFT ANTI JOIN accounts a
  ON t.account_id = a.account_id;
```

Expected:

```text
t6
```

### Example 51: Keep only rows with matching accounts using left semi join

```sql
SELECT t.*
FROM transactions t
LEFT SEMI JOIN accounts a
  ON t.account_id = a.account_id;
```

Expected:

```text
all transactions except t6
```

### Example 52: Join country risk

```sql
SELECT
  t.transaction_id,
  t.country_code,
  r.risk_level
FROM transactions t
LEFT JOIN country_risk r
  ON t.country_code = r.country_code;
```

Expected:

```text
t8 has risk_level null because country_code is null.
```

### Example 53: High-risk transactions

```sql
SELECT
  t.transaction_id,
  t.amount_cad,
  t.country_code,
  r.risk_level
FROM transactions t
JOIN country_risk r
  ON t.country_code = r.country_code
WHERE r.risk_level = 'HIGH';
```

Expected:

```text
t1,t2,t5,t6,t7
```

### Example 54: Full outer compare two alert tables

```sql
WITH legacy_alerts AS (
  SELECT * FROM VALUES
    ('k1', 'c1', CAST(110.00 AS DECIMAL(18,2))),
    ('k2', 'c2', CAST(200.00 AS DECIMAL(18,2)))
  AS legacy_alerts(alert_key, customer_id, observed_amount_cad)
),
cloud_alerts AS (
  SELECT * FROM VALUES
    ('k1', 'c1', CAST(110.00 AS DECIMAL(18,2))),
    ('k3', 'c3', CAST(150.00 AS DECIMAL(18,2)))
  AS cloud_alerts(alert_key, customer_id, observed_amount_cad)
)
SELECT
  COALESCE(l.alert_key, c.alert_key) AS alert_key,
  CASE
    WHEN l.alert_key IS NULL THEN 'cloud_only'
    WHEN c.alert_key IS NULL THEN 'legacy_only'
    WHEN l.observed_amount_cad <> c.observed_amount_cad THEN 'field_difference'
    ELSE 'matched'
  END AS comparison_status
FROM legacy_alerts l
FULL OUTER JOIN cloud_alerts c
  ON l.alert_key = c.alert_key;
```

Expected:

```text
k1 matched
k2 legacy_only
k3 cloud_only
```

---

## 14. CTE basics

CTE means Common Table Expression. It lets you name a step inside a query.

### Example 55: CTE for posted wires

```sql
WITH posted_wires AS (
  SELECT *
  FROM transactions
  WHERE status = 'POSTED'
    AND transaction_type = 'WIRE'
)
SELECT *
FROM posted_wires;
```

### Example 56: Multi-step CTE

```sql
WITH posted_wires AS (
  SELECT *
  FROM transactions
  WHERE status = 'POSTED'
    AND transaction_type = 'WIRE'
),
with_customer AS (
  SELECT
    t.*,
    a.customer_id
  FROM posted_wires t
  JOIN accounts a
    ON t.account_id = a.account_id
),
customer_totals AS (
  SELECT
    customer_id,
    SUM(amount_cad) AS total_posted_wire_amount
  FROM with_customer
  GROUP BY customer_id
)
SELECT *
FROM customer_totals
WHERE total_posted_wire_amount > 100;
```

CTEs are excellent for learning because each step has a name and can be inspected.

---

## 15. Subquery basics

### Example 57: Accounts with transactions over 100

```sql
SELECT *
FROM accounts
WHERE account_id IN (
  SELECT account_id
  FROM transactions
  WHERE amount_cad > 100
);
```

Expected:

```text
a2
```

### Example 58: Transactions above overall average

```sql
SELECT *
FROM transactions
WHERE amount_cad > (
  SELECT AVG(amount_cad)
  FROM transactions
);
```

### Example 59: NOT EXISTS for missing transactions

```sql
SELECT a.*
FROM accounts a
WHERE NOT EXISTS (
  SELECT 1
  FROM transactions t
  WHERE t.account_id = a.account_id
);
```

Expected:

```text
No rows, because all listed accounts a1-a4 have at least one transaction.
```

---

## 16. Window function basics

Window functions calculate across related rows while keeping row-level detail.

### Example 60: Row number by account

```sql
SELECT
  transaction_id,
  account_id,
  transaction_date,
  amount_cad,
  ROW_NUMBER() OVER (
    PARTITION BY account_id
    ORDER BY transaction_date, transaction_id
  ) AS account_txn_sequence
FROM transactions;
```

### Example 61: Latest transaction per account

```sql
WITH ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY account_id
      ORDER BY transaction_date DESC, transaction_id DESC
    ) AS rn
  FROM transactions
)
SELECT *
FROM ranked
WHERE rn = 1;
```

### Example 62: Running total by account

```sql
SELECT
  transaction_id,
  account_id,
  transaction_date,
  amount_cad,
  SUM(amount_cad) OVER (
    PARTITION BY account_id
    ORDER BY transaction_date, transaction_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_amount_cad
FROM transactions;
```

### Example 63: Previous transaction amount

```sql
SELECT
  transaction_id,
  account_id,
  transaction_date,
  amount_cad,
  LAG(amount_cad) OVER (
    PARTITION BY account_id
    ORDER BY transaction_date, transaction_id
  ) AS previous_amount_cad
FROM transactions;
```

### Example 64: Difference from previous transaction

```sql
WITH ordered AS (
  SELECT
    *,
    LAG(amount_cad) OVER (
      PARTITION BY account_id
      ORDER BY transaction_date, transaction_id
    ) AS previous_amount_cad
  FROM transactions
)
SELECT
  transaction_id,
  account_id,
  amount_cad,
  previous_amount_cad,
  amount_cad - previous_amount_cad AS amount_change
FROM ordered;
```

### Example 65: Rank largest transactions per account

```sql
SELECT
  transaction_id,
  account_id,
  amount_cad,
  DENSE_RANK() OVER (
    PARTITION BY account_id
    ORDER BY amount_cad DESC
  ) AS amount_rank
FROM transactions;
```

---

## 17. DQ query examples

### Example 66: Required field check

```sql
SELECT
  COUNT(*) AS failed_records
FROM transactions
WHERE transaction_id IS NULL
   OR account_id IS NULL
   OR transaction_date IS NULL
   OR amount_cad IS NULL;
```

### Example 67: Orphan account check

```sql
SELECT
  t.transaction_id,
  t.account_id
FROM transactions t
LEFT ANTI JOIN accounts a
  ON t.account_id = a.account_id;
```

Expected:

```text
t6
```

### Example 68: Invalid country reference check

```sql
SELECT
  t.transaction_id,
  t.country_code
FROM transactions t
LEFT ANTI JOIN country_risk r
  ON t.country_code = r.country_code
WHERE t.country_code IS NOT NULL;
```

Expected:

```text
No rows in this tiny dataset.
```

### Example 69: Missing country check

```sql
SELECT
  transaction_id,
  account_id
FROM transactions
WHERE country_code IS NULL;
```

Expected:

```text
t8
```

### Example 70: Duplicate transaction key check

```sql
SELECT
  transaction_id,
  COUNT(*) AS duplicate_count
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;
```

Expected:

```text
No rows in this tiny dataset.
```

### Example 71: Account status DQ impact

```sql
SELECT
  a.account_status,
  COUNT(*) AS transaction_count,
  SUM(t.amount_cad) AS total_amount_cad
FROM transactions t
JOIN accounts a
  ON t.account_id = a.account_id
GROUP BY a.account_status;
```

Expected:

```text
ACTIVE includes a1,a2,a3 transactions.
CLOSED includes t8 through a4.
```

---

## 18. Reconciliation query examples

### Example 72: Source count

```sql
SELECT COUNT(*) AS source_count
FROM transactions;
```

### Example 73: Filter reconciliation

```sql
WITH source AS (
  SELECT COUNT(*) AS source_count
  FROM transactions
),
posted_wires AS (
  SELECT COUNT(*) AS posted_wire_count
  FROM transactions
  WHERE status = 'POSTED'
    AND transaction_type = 'WIRE'
),
not_posted_wire AS (
  SELECT COUNT(*) AS excluded_count
  FROM transactions
  WHERE NOT (status = 'POSTED' AND transaction_type = 'WIRE')
)
SELECT
  source_count,
  posted_wire_count,
  excluded_count,
  source_count - posted_wire_count - excluded_count AS unexplained_difference
FROM source
CROSS JOIN posted_wires
CROSS JOIN not_posted_wire;
```

### Example 74: Join reconciliation

```sql
WITH posted_wires AS (
  SELECT *
  FROM transactions
  WHERE status = 'POSTED'
    AND transaction_type = 'WIRE'
),
valid_accounts AS (
  SELECT COUNT(*) AS valid_count
  FROM posted_wires t
  JOIN accounts a
    ON t.account_id = a.account_id
),
orphans AS (
  SELECT COUNT(*) AS orphan_count
  FROM posted_wires t
  LEFT ANTI JOIN accounts a
    ON t.account_id = a.account_id
),
source AS (
  SELECT COUNT(*) AS posted_wire_count
  FROM posted_wires
)
SELECT
  posted_wire_count,
  valid_count,
  orphan_count,
  posted_wire_count - valid_count - orphan_count AS unexplained_difference
FROM source
CROSS JOIN valid_accounts
CROSS JOIN orphans;
```

Expected:

```text
posted_wire_count = 5
valid_count = 4
orphan_count = 1
unexplained_difference = 0
```

---

## 19. Alert query examples

### Example 75: Simple high-risk posted wire alert

```sql
WITH posted_wires AS (
  SELECT *
  FROM transactions
  WHERE status = 'POSTED'
    AND transaction_type = 'WIRE'
    AND transaction_date >= DATE '2022-06-01'
    AND transaction_date <  DATE '2022-07-01'
),
valid_customer_tx AS (
  SELECT
    t.*,
    a.customer_id
  FROM posted_wires t
  JOIN accounts a
    ON t.account_id = a.account_id
),
high_risk_tx AS (
  SELECT
    t.*
  FROM valid_customer_tx t
  JOIN country_risk r
    ON t.country_code = r.country_code
  WHERE r.risk_level = 'HIGH'
),
customer_totals AS (
  SELECT
    customer_id,
    SUM(amount_cad) AS observed_amount_cad,
    COUNT(*) AS supporting_transaction_count
  FROM high_risk_tx
  GROUP BY customer_id
)
SELECT
  SHA2(CONCAT_WS('|', 'TM_HIGH_RISK_WIRE_001', '1.0.0', '2022-06', customer_id), 256) AS alert_key,
  'TM_HIGH_RISK_WIRE_001' AS rule_id,
  '1.0.0' AS rule_version,
  '2022-06' AS processing_month,
  customer_id,
  observed_amount_cad,
  supporting_transaction_count
FROM customer_totals
WHERE observed_amount_cad > 100;
```

Expected:

```text
c1 alerts with 110.00 from t1+t2.
```

### Example 76: Supporting transactions for the alert

```sql
WITH posted_wires AS (
  SELECT *
  FROM transactions
  WHERE status = 'POSTED'
    AND transaction_type = 'WIRE'
    AND transaction_date >= DATE '2022-06-01'
    AND transaction_date <  DATE '2022-07-01'
),
valid_customer_tx AS (
  SELECT
    t.*,
    a.customer_id
  FROM posted_wires t
  JOIN accounts a
    ON t.account_id = a.account_id
),
high_risk_tx AS (
  SELECT
    t.*
  FROM valid_customer_tx t
  JOIN country_risk r
    ON t.country_code = r.country_code
  WHERE r.risk_level = 'HIGH'
),
alerts AS (
  SELECT
    customer_id,
    SHA2(CONCAT_WS('|', 'TM_HIGH_RISK_WIRE_001', '1.0.0', '2022-06', customer_id), 256) AS alert_key
  FROM high_risk_tx
  GROUP BY customer_id
  HAVING SUM(amount_cad) > 100
)
SELECT
  a.alert_key,
  h.transaction_id,
  h.customer_id,
  h.account_id,
  h.transaction_date,
  h.amount_cad,
  h.country_code
FROM high_risk_tx h
JOIN alerts a
  ON h.customer_id = a.customer_id
ORDER BY h.transaction_id;
```

Expected:

```text
t1 and t2
```

---

## 20. CREATE VIEW basics

### Example 77: Create a reusable temp view

```sql
CREATE OR REPLACE TEMP VIEW june_posted_wires AS
SELECT *
FROM transactions
WHERE status = 'POSTED'
  AND transaction_type = 'WIRE'
  AND transaction_date >= DATE '2022-06-01'
  AND transaction_date <  DATE '2022-07-01';
```

Then query it:

```sql
SELECT COUNT(*) AS june_posted_wire_count
FROM june_posted_wires;
```

### Example 78: Create a debugging view with reasons

```sql
CREATE OR REPLACE TEMP VIEW transaction_eligibility_debug AS
SELECT
  transaction_id,
  account_id,
  transaction_date,
  amount_cad,
  transaction_type,
  status,
  country_code,
  CASE
    WHEN status <> 'POSTED' THEN 'EXCLUDE_NOT_POSTED'
    WHEN transaction_type <> 'WIRE' THEN 'EXCLUDE_NOT_WIRE'
    WHEN country_code IS NULL THEN 'EXCEPTION_MISSING_COUNTRY'
    ELSE 'CANDIDATE'
  END AS eligibility_status
FROM transactions;
```

Inspect:

```sql
SELECT
  eligibility_status,
  COUNT(*) AS row_count
FROM transaction_eligibility_debug
GROUP BY eligibility_status;
```

---

## 21. Set operation basics

### Example 79: UNION ALL

```sql
SELECT 'source' AS metric_name, COUNT(*) AS metric_value
FROM transactions
UNION ALL
SELECT 'accounts', COUNT(*)
FROM accounts;
```

`UNION ALL` keeps duplicates.

### Example 80: UNION

```sql
SELECT account_id
FROM transactions
UNION
SELECT account_id
FROM accounts;
```

`UNION` removes duplicates.

### Example 81: EXCEPT

```sql
SELECT account_id
FROM transactions
EXCEPT
SELECT account_id
FROM accounts;
```

Expected:

```text
a9
```

### Example 82: INTERSECT

```sql
SELECT account_id
FROM transactions
INTERSECT
SELECT account_id
FROM accounts;
```

Expected:

```text
a1,a2,a3,a4
```

---

## 22. Query debugging checklist

When a query looks wrong, ask:

1. What is the expected grain?
2. How many rows should each step produce?
3. Did a join multiply rows?
4. Did an inner join drop rows?
5. Did a null behave differently than expected?
6. Did a `WHERE` filter belong in `HAVING`?
7. Did a date boundary include or exclude the correct day?
8. Did `DISTINCT` hide a data problem?
9. Did aggregation collapse the detail needed for evidence?
10. Does the output reconcile to the previous step?

---

## 23. Query patterns to memorize

### Pattern 1: Candidate population

```sql
SELECT *
FROM transactions
WHERE status = 'POSTED'
  AND transaction_type = 'WIRE'
  AND transaction_date >= DATE '2022-06-01'
  AND transaction_date <  DATE '2022-07-01';
```

### Pattern 2: Orphan check

```sql
SELECT t.*
FROM transactions t
LEFT ANTI JOIN accounts a
  ON t.account_id = a.account_id;
```

### Pattern 3: Aggregate and threshold

```sql
SELECT
  customer_id,
  SUM(amount_cad) AS total_amount_cad
FROM customer_transactions
GROUP BY customer_id
HAVING SUM(amount_cad) > 100000;
```

### Pattern 4: Deterministic key

```sql
SHA2(CONCAT_WS('|', rule_id, rule_version, processing_month, customer_id), 256) AS alert_key
```

### Pattern 5: Reconciliation metric table

```sql
SELECT
  'posted_wire_count' AS metric_name,
  COUNT(*) AS metric_value
FROM transactions
WHERE status = 'POSTED'
  AND transaction_type = 'WIRE';
```

---

## 24. Closed-book drills

Answer without looking:

1. What is the mental execution order of a SQL query?
2. What is the difference between `WHERE` and `HAVING`?
3. Why does `country_code <> 'CA'` not return null countries?
4. What rows survive `status = 'POSTED' AND transaction_type = 'WIRE'`?
5. Why does an inner join hide orphan accounts?
6. What does left anti join return?
7. What does groupBy do to row grain?
8. What is the difference between `COUNT(*)` and `COUNT(column)`?
9. Why do you need tie-breakers in `ORDER BY`?
10. What is the difference between `UNION` and `UNION ALL`?
11. What does `ROW_NUMBER()` help with?
12. How would you find latest transaction per account?
13. How do you generate a deterministic alert key?
14. What query proves t6 is a DQ exception?
15. What supporting transactions explain c1's alert?
