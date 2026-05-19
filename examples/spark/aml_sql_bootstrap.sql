-- Reusable Spark SQL bootstrap for AML/TM learning examples.
-- Run this first in Databricks SQL or a Spark SQL notebook.
-- It creates tiny temp views and validates them.

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

-- Expected: every row returns PASS.
WITH checks AS (
  SELECT 'transactions_count' AS check_name, COUNT(*) = 8 AS passed FROM transactions
  UNION ALL
  SELECT 'accounts_count', COUNT(*) = 4 FROM accounts
  UNION ALL
  SELECT 'country_risk_count', COUNT(*) = 3 FROM country_risk
  UNION ALL
  SELECT 'transaction_ids_t1_to_t8', COUNT(DISTINCT transaction_id) = 8 FROM transactions
  UNION ALL
  SELECT 'orphan_candidate_t6_exists', COUNT(*) = 1 FROM transactions WHERE transaction_id = 't6' AND account_id = 'a9'
  UNION ALL
  SELECT 'missing_country_t8_exists', COUNT(*) = 1 FROM transactions WHERE transaction_id = 't8' AND country_code IS NULL
)
SELECT
  check_name,
  CASE WHEN passed THEN 'PASS' ELSE 'FAIL' END AS test_status
FROM checks;
