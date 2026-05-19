-- Tiny AML/TM Spark SQL first-principles example.
-- Paste into a Databricks SQL editor or Spark SQL notebook cell after creating the temp views.

-- Expected source rows:
-- t1,t2,t3,t4,t5,t6

CREATE OR REPLACE TEMP VIEW raw_transactions AS
SELECT * FROM VALUES
  ('t1', 'a1', '2022-06-01', '60.00',  'WIRE', 'POSTED',   'IR'),
  ('t2', 'a1', '2022-06-03', '50.00',  'WIRE', 'POSTED',   'IR'),
  ('t3', 'a1', '2022-06-05', '10.00',  'CARD', 'POSTED',   'CA'),
  ('t4', 'a2', '2022-06-02', '200.00', 'WIRE', 'POSTED',   'CA'),
  ('t5', 'a3', '2022-06-02', '20.00',  'WIRE', 'REVERSED', 'IR'),
  ('t6', 'a9', '2022-06-02', '80.00',  'WIRE', 'POSTED',   'IR')
AS raw_transactions(
  transaction_id,
  account_id,
  transaction_date,
  amount_cad,
  transaction_type,
  status,
  country_code
);

CREATE OR REPLACE TEMP VIEW account_history AS
SELECT * FROM VALUES
  ('a1', 'c1', '2020-01-01', '2023-01-01'),
  ('a2', 'c2', '2020-01-01', '2023-01-01'),
  ('a3', 'c3', '2020-01-01', '2023-01-01')
AS account_history(
  account_id,
  customer_id,
  effective_start_date,
  effective_end_date
);

CREATE OR REPLACE TEMP VIEW country_risk AS
SELECT * FROM VALUES
  ('IR', 'HIGH', '2020-01-01', '2023-01-01'),
  ('CA', 'LOW',  '2020-01-01', '2023-01-01')
AS country_risk(
  country_code,
  risk_level,
  effective_start_date,
  effective_end_date
);

CREATE OR REPLACE TEMP VIEW tx AS
SELECT
  transaction_id,
  UPPER(TRIM(account_id)) AS account_id,
  TO_DATE(transaction_date, 'yyyy-MM-dd') AS transaction_date,
  CAST(amount_cad AS DECIMAL(18,2)) AS amount_cad,
  transaction_type,
  status,
  UPPER(TRIM(country_code)) AS country_code
FROM raw_transactions;

CREATE OR REPLACE TEMP VIEW posted_wires AS
SELECT *
FROM tx
WHERE status = 'POSTED'
  AND transaction_type = 'WIRE'
  AND transaction_date BETWEEN DATE '2022-06-01' AND DATE '2022-06-30';

-- Expected: t6, because account_id a9 is not in account history.
CREATE OR REPLACE TEMP VIEW dq_orphan_accounts AS
SELECT
  'ORPHAN_ACCOUNT' AS exception_type,
  t.*
FROM posted_wires t
LEFT ANTI JOIN account_history a
  ON t.account_id = a.account_id
 AND t.transaction_date >= TO_DATE(a.effective_start_date, 'yyyy-MM-dd')
 AND t.transaction_date <  TO_DATE(a.effective_end_date, 'yyyy-MM-dd');

CREATE OR REPLACE TEMP VIEW valid_tx AS
SELECT
  t.*,
  a.customer_id
FROM posted_wires t
JOIN account_history a
  ON t.account_id = a.account_id
 AND t.transaction_date >= TO_DATE(a.effective_start_date, 'yyyy-MM-dd')
 AND t.transaction_date <  TO_DATE(a.effective_end_date, 'yyyy-MM-dd');

CREATE OR REPLACE TEMP VIEW high_risk_tx AS
SELECT
  t.*,
  r.risk_level
FROM valid_tx t
JOIN country_risk r
  ON t.country_code = r.country_code
 AND t.transaction_date >= TO_DATE(r.effective_start_date, 'yyyy-MM-dd')
 AND t.transaction_date <  TO_DATE(r.effective_end_date, 'yyyy-MM-dd')
WHERE r.risk_level = 'HIGH';

CREATE OR REPLACE TEMP VIEW customer_totals AS
SELECT
  customer_id,
  SUM(amount_cad) AS observed_amount_cad,
  COUNT(*) AS supporting_transaction_count
FROM high_risk_tx
GROUP BY customer_id;

-- Expected: one alert for c1 with observed_amount_cad = 110.00.
CREATE OR REPLACE TEMP VIEW alerts AS
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

CREATE OR REPLACE TEMP VIEW supporting_transactions AS
SELECT
  a.alert_key,
  h.transaction_id,
  h.customer_id,
  h.account_id,
  h.transaction_date,
  h.amount_cad,
  h.country_code,
  h.risk_level
FROM high_risk_tx h
JOIN alerts a
  ON h.customer_id = a.customer_id;

SELECT * FROM alerts;
SELECT * FROM supporting_transactions ORDER BY transaction_id;
SELECT exception_type, transaction_id, account_id FROM dq_orphan_accounts;

SELECT 'raw_transactions' AS step_name, COUNT(*) AS row_count FROM raw_transactions
UNION ALL
SELECT 'posted_wires', COUNT(*) FROM posted_wires
UNION ALL
SELECT 'orphan_account_exceptions', COUNT(*) FROM dq_orphan_accounts
UNION ALL
SELECT 'valid_account_matched_posted_wires', COUNT(*) FROM valid_tx
UNION ALL
SELECT 'high_risk_posted_wires', COUNT(*) FROM high_risk_tx
UNION ALL
SELECT 'customer_totals', COUNT(*) FROM customer_totals
UNION ALL
SELECT 'alerts', COUNT(*) FROM alerts;

-- Validation checks. Expected: all rows return PASS.
WITH checks AS (
  SELECT 'raw_transactions_count' AS check_name, COUNT(*) = 6 AS passed FROM raw_transactions
  UNION ALL
  SELECT 'posted_wires_count', COUNT(*) = 4 FROM posted_wires
  UNION ALL
  SELECT 'orphan_account_count', COUNT(*) = 1 FROM dq_orphan_accounts
  UNION ALL
  SELECT 'valid_tx_count', COUNT(*) = 3 FROM valid_tx
  UNION ALL
  SELECT 'high_risk_tx_count', COUNT(*) = 2 FROM high_risk_tx
  UNION ALL
  SELECT 'customer_totals_count', COUNT(*) = 1 FROM customer_totals
  UNION ALL
  SELECT 'alerts_count', COUNT(*) = 1 FROM alerts
  UNION ALL
  SELECT 'alert_customer_is_c1', COUNT(*) = 1 FROM alerts WHERE customer_id = 'c1'
  UNION ALL
  SELECT 'supporting_transactions_are_t1_t2', COUNT(*) = 2 FROM supporting_transactions WHERE transaction_id IN ('t1', 't2')
  UNION ALL
  SELECT 'orphan_transaction_is_t6', COUNT(*) = 1 FROM dq_orphan_accounts WHERE transaction_id = 't6'
)
SELECT
  check_name,
  CASE WHEN passed THEN 'PASS' ELSE 'FAIL' END AS test_status
FROM checks;
