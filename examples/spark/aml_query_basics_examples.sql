-- Spark SQL query basics examples for AML/TM learning.
-- Companion to docs/17-spark-sql-query-basics-examples.md.
-- Paste this file into Databricks SQL or a Spark SQL notebook.

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

-- 01. Explore all rows.
SELECT * FROM transactions;

-- 02. Select useful columns.
SELECT transaction_id, account_id, amount_cad
FROM transactions;

-- 03. Aliases.
SELECT
  transaction_id AS txn_id,
  account_id AS acct_id,
  amount_cad AS amount
FROM transactions;

-- 04. Derived column.
SELECT
  transaction_id,
  amount_cad,
  amount_cad * 1.13 AS amount_with_buffer
FROM transactions;

-- 05. Distinct transaction types.
SELECT DISTINCT transaction_type
FROM transactions;

-- 06. Posted transactions.
SELECT *
FROM transactions
WHERE status = 'POSTED';

-- 07. Posted wires.
SELECT *
FROM transactions
WHERE status = 'POSTED'
  AND transaction_type = 'WIRE';

-- 08. June 2022 transactions.
SELECT *
FROM transactions
WHERE transaction_date >= DATE '2022-06-01'
  AND transaction_date <  DATE '2022-07-01';

-- 09. Amount threshold.
SELECT *
FROM transactions
WHERE amount_cad > 100;

-- 10. Boundary threshold.
SELECT *
FROM transactions
WHERE amount_cad >= 100;

-- 11. Null country.
SELECT *
FROM transactions
WHERE country_code IS NULL;

-- 12. Null trap: t8 is not returned.
SELECT *
FROM transactions
WHERE country_code <> 'CA';

-- 13. Include null explicitly.
SELECT *
FROM transactions
WHERE country_code <> 'CA'
   OR country_code IS NULL;

-- 14. COALESCE for display.
SELECT
  transaction_id,
  COALESCE(country_code, 'UNKNOWN') AS country_code_display
FROM transactions;

-- 15. Largest transactions.
SELECT transaction_id, amount_cad
FROM transactions
ORDER BY amount_cad DESC, transaction_id ASC;

-- 16. Top 3 transactions.
SELECT transaction_id, amount_cad
FROM transactions
ORDER BY amount_cad DESC, transaction_id ASC
LIMIT 3;

-- 17. CASE amount bands.
SELECT
  transaction_id,
  amount_cad,
  CASE
    WHEN amount_cad >= 200 THEN 'LARGE'
    WHEN amount_cad >= 100 THEN 'MEDIUM'
    ELSE 'SMALL'
  END AS amount_band
FROM transactions;

-- 18. Eligibility reason.
SELECT
  transaction_id,
  CASE
    WHEN country_code IS NULL THEN 'MISSING_COUNTRY'
    WHEN status <> 'POSTED' THEN 'NOT_POSTED'
    WHEN transaction_type <> 'WIRE' THEN 'NOT_WIRE'
    ELSE 'ELIGIBLE_CANDIDATE'
  END AS eligibility_reason
FROM transactions;

-- 19. String normalization.
SELECT
  transaction_id,
  UPPER(TRIM(account_id)) AS account_id_norm
FROM transactions;

-- 20. Deterministic key candidate.
SELECT
  transaction_id,
  SHA2(CONCAT_WS('|', 'TM001', '1.0.0', '2022-06', account_id), 256) AS key_candidate
FROM transactions;

-- 21. Month extraction.
SELECT
  transaction_id,
  DATE_FORMAT(transaction_date, 'yyyy-MM') AS transaction_month
FROM transactions;

-- 22. Rolling window start.
SELECT
  transaction_id,
  transaction_date,
  DATE_SUB(transaction_date, 29) AS rolling_30_day_start
FROM transactions;

-- 23. Count all rows.
SELECT COUNT(*) AS row_count
FROM transactions;

-- 24. Count by transaction type.
SELECT
  transaction_type,
  COUNT(*) AS row_count
FROM transactions
GROUP BY transaction_type;

-- 25. Sum by account.
SELECT
  account_id,
  SUM(amount_cad) AS total_amount_cad
FROM transactions
GROUP BY account_id;

-- 26. Multiple aggregations.
SELECT
  account_id,
  COUNT(*) AS txn_count,
  SUM(amount_cad) AS total_amount_cad,
  AVG(amount_cad) AS avg_amount_cad,
  MAX(amount_cad) AS max_amount_cad
FROM transactions
GROUP BY account_id;

-- 27. Conditional aggregation.
SELECT
  account_id,
  SUM(CASE WHEN transaction_type = 'WIRE' THEN amount_cad ELSE 0 END) AS wire_amount_cad,
  COUNT(CASE WHEN transaction_type = 'WIRE' THEN 1 END) AS wire_count
FROM transactions
GROUP BY account_id;

-- 28. HAVING after aggregation.
SELECT
  account_id,
  SUM(amount_cad) AS total_amount_cad
FROM transactions
GROUP BY account_id
HAVING SUM(amount_cad) > 100;

-- 29. Inner join hides t6.
SELECT
  t.transaction_id,
  t.account_id,
  a.customer_id
FROM transactions t
JOIN accounts a
  ON t.account_id = a.account_id;

-- 30. Left join preserves t6.
SELECT
  t.transaction_id,
  t.account_id,
  a.customer_id
FROM transactions t
LEFT JOIN accounts a
  ON t.account_id = a.account_id;

-- 31. Left anti join finds orphan accounts.
SELECT t.*
FROM transactions t
LEFT ANTI JOIN accounts a
  ON t.account_id = a.account_id;

-- 32. Left semi join keeps rows with valid accounts.
SELECT t.*
FROM transactions t
LEFT SEMI JOIN accounts a
  ON t.account_id = a.account_id;

-- 33. Country risk enrichment.
SELECT
  t.transaction_id,
  t.country_code,
  r.risk_level
FROM transactions t
LEFT JOIN country_risk r
  ON t.country_code = r.country_code;

-- 34. High-risk country transactions.
SELECT
  t.transaction_id,
  t.amount_cad,
  t.country_code,
  r.risk_level
FROM transactions t
JOIN country_risk r
  ON t.country_code = r.country_code
WHERE r.risk_level = 'HIGH';

-- 35. Multi-step CTE.
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

-- 36. Subquery: accounts with transactions over 100.
SELECT *
FROM accounts
WHERE account_id IN (
  SELECT account_id
  FROM transactions
  WHERE amount_cad > 100
);

-- 37. Window row number.
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

-- 38. Latest transaction per account.
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

-- 39. Running total.
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

-- 40. Previous amount.
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

-- 41. Required field check.
SELECT
  COUNT(*) AS failed_records
FROM transactions
WHERE transaction_id IS NULL
   OR account_id IS NULL
   OR transaction_date IS NULL
   OR amount_cad IS NULL;

-- 42. Invalid country reference check.
SELECT
  t.transaction_id,
  t.country_code
FROM transactions t
LEFT ANTI JOIN country_risk r
  ON t.country_code = r.country_code
WHERE t.country_code IS NOT NULL;

-- 43. Duplicate transaction key check.
SELECT
  transaction_id,
  COUNT(*) AS duplicate_count
FROM transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- 44. Filter reconciliation.
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

-- 45. Join reconciliation.
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

-- 46. Alert query.
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

-- 47. Supporting transactions for alert query.
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

-- 48. EXCEPT: account IDs in transactions but not accounts.
SELECT account_id
FROM transactions
EXCEPT
SELECT account_id
FROM accounts;

-- 49. UNION ALL metric output.
SELECT 'transaction_count' AS metric_name, COUNT(*) AS metric_value
FROM transactions
UNION ALL
SELECT 'account_count', COUNT(*)
FROM accounts
UNION ALL
SELECT 'country_reference_count', COUNT(*)
FROM country_risk;
