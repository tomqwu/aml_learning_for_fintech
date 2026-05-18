# 03 — Rule Migration and Spec-as-Code

## 1. Why rule migration is hard

Legacy transaction monitoring rules often live across many places:

- SAS programs
- Oracle SQL scripts
- stored procedures
- IMS/mainframe extracts
- parameter tables
- reference files
- Excel-based exception lists
- scheduler dependencies
- undocumented business assumptions

Migrating a rule is not simply translating syntax. It means preserving behavior, explaining assumptions, testing output, and making the rule governable.

A rule migration should answer:

```text
What is the rule trying to detect?
Which source fields does it use?
Which customers/accounts/transactions are eligible?
Which records are excluded?
Which time window is used?
Which thresholds apply?
Which reference data is required?
What output should be produced?
How do we prove the new output matches the old output?
```

---

## 2. Migration workflow

```text
1. Rule inventory
2. Legacy code analysis
3. Source-to-target mapping
4. Rule specification
5. Test data design
6. Cloud implementation
7. Unit testing
8. Parallel run validation
9. Reconciliation and defect triage
10. Business sign-off
11. Production deployment
12. Post-run monitoring
```

### Step 1 — Rule inventory

Capture every rule/scenario:

```text
rule_id
rule_name
description
business owner
technical owner
legacy platform
source tables
output tables
threshold parameters
run frequency
known exclusions
known defects
status
```

### Step 2 — Legacy code analysis

Read the old implementation and extract logic.

For SAS-style logic, look for:

- DATA steps
- PROC SQL
- macros
- formats
- retained variables
- sort order dependencies
- merge logic
- date functions
- output datasets
- implicit missing value behavior

For Oracle-style logic, look for:

- joins
- window functions
- stored procedures
- parameter tables
- indexes
- materialized views
- date arithmetic
- exception handling

For IMS/mainframe-style data, look for:

- hierarchical segment relationships
- extract layout
- copybook-like field definitions
- effective dating
- encoding/format issues
- batch timing
- record keys

### Step 3 — Source-to-target mapping

Every output field should map to its source and transformation.

| Target field | Source field(s) | Transformation | Rule dependency | Notes |
|---|---|---|---|---|
| customer_id | account.customer_id | direct | eligibility, grouping | Must be point-in-time. |
| total_amount | transaction.amount | sum over window | threshold | Convert currency first if needed. |
| alert_date | batch date | derived | output | Must be deterministic. |
| reason_code | rule condition | derived | explainability | Standardized across scenarios. |

---

## 3. What a good rule specification contains

A rule spec should be readable by business, engineering, QA, and audit.

Minimum contents:

```text
identity
  rule_id
  rule_name
  owner
  version
  status
  effective dates

business intent
  what risk pattern the rule is designed to identify
  why the rule exists
  what is out of scope

input data
  required tables
  required fields
  reference data
  point-in-time requirements

eligibility
  customer/account/transaction filters
  inclusion rules
  exclusion rules

logic
  joins
  time window
  aggregation key
  threshold
  reason codes
  currency handling
  duplicate handling

output
  fields
  deterministic keys
  supporting records
  alert narrative fields

controls
  data quality checks
  reconciliation checks
  test cases
  approval requirements

change history
  version
  author
  change reason
  impact summary
  approval
```

---

## 4. Spec-as-code example

```yaml
rule_id: TM_HIGH_RISK_GEO_001
rule_name: High Risk Geography Transaction Aggregation
owner: Financial Crime Risk
technical_owner: Data Engineering
status: draft
version: 1.0.0

business_intent: >
  Identify customers whose transaction activity with higher-risk geographies exceeds
  the approved scenario threshold within a defined monitoring window.

input_tables:
  - name: transactions
    alias: t
    required_fields:
      - transaction_id
      - account_id
      - transaction_date
      - amount
      - currency
      - transaction_type
      - country_code
  - name: accounts
    alias: a
    required_fields:
      - account_id
      - customer_id
      - product_type
      - open_date
      - close_date
  - name: customers
    alias: c
    required_fields:
      - customer_id
      - customer_type
      - risk_rating
      - effective_start_date
      - effective_end_date
  - name: country_risk_reference
    alias: r
    required_fields:
      - country_code
      - risk_level
      - effective_start_date
      - effective_end_date

point_in_time_requirements:
  - customer risk rating must be valid on transaction_date
  - country risk level must be valid on transaction_date
  - account ownership must be valid on transaction_date

eligibility:
  include:
    - transaction_type in [WIRE, EFT]
    - account_status is active during transaction_date
  exclude:
    - test accounts
    - reversed transactions
    - internal operational accounts

logic:
  aggregation_key: customer_id
  window: rolling_30_days
  condition:
    country_risk_level: HIGH
    total_amount_greater_than: parameter.threshold_amount
  reason_code: HIGH_RISK_GEO_AMOUNT_THRESHOLD

output_fields:
  - alert_key
  - rule_id
  - rule_version
  - customer_id
  - window_start_date
  - window_end_date
  - total_amount
  - transaction_count
  - reason_code
  - supporting_transaction_ids
  - batch_id

controls:
  dq_checks:
    - transaction_id_not_null
    - account_id_not_null
    - customer_id_not_null
    - valid_country_code
    - amount_non_negative_or_business_approved_exception
    - point_in_time_reference_coverage
  reconciliation:
    - source_to_silver_transaction_count
    - silver_to_rule_input_transaction_count
    - rule_input_to_alert_supporting_transaction_count
    - alert_count_by_month

test_cases:
  - name: customer_below_threshold_no_alert
  - name: customer_above_threshold_alert
  - name: reference_data_effective_date_boundary
  - name: duplicate_transaction_excluded
  - name: reversed_transaction_excluded

change_history:
  - version: 1.0.0
    change: initial draft
    approver: pending
```

---

## 5. Translating rule specs into SQL/Spark logic

Example Spark SQL shape:

```sql
WITH rule_input AS (
    SELECT
        t.transaction_id,
        a.customer_id,
        t.account_id,
        t.transaction_date,
        t.amount_base_currency,
        r.risk_level
    FROM silver_transactions t
    JOIN silver_accounts_point_in_time a
      ON t.account_id = a.account_id
     AND t.transaction_date BETWEEN a.effective_start_date AND a.effective_end_date
    JOIN silver_country_risk_point_in_time r
      ON t.country_code = r.country_code
     AND t.transaction_date BETWEEN r.effective_start_date AND r.effective_end_date
    WHERE t.transaction_type IN ('WIRE', 'EFT')
      AND t.is_reversal = false
      AND a.is_test_account = false
), aggregated AS (
    SELECT
        customer_id,
        window_start_date,
        window_end_date,
        SUM(amount_base_currency) AS total_amount,
        COUNT(*) AS transaction_count,
        COLLECT_SET(transaction_id) AS supporting_transaction_ids
    FROM rule_input
    WHERE risk_level = 'HIGH'
    GROUP BY customer_id, window_start_date, window_end_date
)
SELECT
    SHA2(CONCAT_WS('|', 'TM_HIGH_RISK_GEO_001', customer_id, window_start_date, window_end_date), 256) AS alert_key,
    'TM_HIGH_RISK_GEO_001' AS rule_id,
    '1.0.0' AS rule_version,
    customer_id,
    window_start_date,
    window_end_date,
    total_amount,
    transaction_count,
    'HIGH_RISK_GEO_AMOUNT_THRESHOLD' AS reason_code,
    supporting_transaction_ids
FROM aggregated
WHERE total_amount > :threshold_amount;
```

This is not a complete production rule. It is a study example showing the shape of a governed rule implementation.

---

## 6. Equivalence validation

### Goal

Prove that the new implementation produces the same results as the old implementation when using the same business logic and same data assumptions.

### Compare at multiple levels

| Level | Question |
|---|---|
| Population | Did both systems evaluate the same customers/accounts/transactions? |
| Filter | Did both systems include/exclude the same records? |
| Aggregation | Did both systems produce the same totals/counts/windows? |
| Threshold | Did both systems trigger the same alert conditions? |
| Output | Did both systems produce the same alert fields? |
| Evidence | Can mismatches be explained and approved? |

### Difference classification

```text
1. Exact match
2. Expected difference due to approved change
3. Source data difference
4. Mapping defect
5. Transformation defect
6. Rule logic defect
7. Reference data defect
8. Timing/window defect
9. Legacy system behavior now exposed
10. Unknown and requires triage
```

---

## 7. Golden record testing

Golden records are small, controlled examples with expected outputs.

Example cases:

| Test case | Purpose |
|---|---|
| Exactly below threshold | Ensures no false trigger at boundary. |
| Exactly equal to threshold | Tests greater-than vs greater-or-equal logic. |
| Above threshold | Ensures rule triggers. |
| Reference value changes mid-window | Tests point-in-time logic. |
| Duplicate transaction | Tests deduplication. |
| Reversed transaction | Tests exclusion. |
| Missing customer link | Tests exception handling. |
| Multiple accounts per customer | Tests aggregation key. |

Golden records should be versioned with the rule spec.

---

## 8. Governance design

A rule should not move to production unless the following are complete:

```text
rule spec approved
source-to-target mapping approved
test cases executed
DQ checks executed
parallel run completed
mismatches triaged
known limitations documented
business owner sign-off obtained
technical owner sign-off obtained
rollback or rerun approach documented
```

---

## 9. Reverse-engineering exercise

Given this legacy pseudo-code:

```text
read transactions
keep records where type = WIRE
join accounts to get customer
join country list where risk = high
for each customer in last 30 days:
    if sum(amount) > threshold:
        output alert
```

Create a rule spec that answers:

1. What are the required input tables?
2. What point-in-time checks are needed?
3. What exclusions must be clarified?
4. What boundary conditions must be tested?
5. What reconciliation metrics are needed?
6. What fields should be included in alert output?

---

## 10. Active recall questions

1. Why is rule migration not just syntax translation?
2. What belongs in a rule inventory?
3. What is source-to-target mapping?
4. What makes a rule specification useful to both engineering and audit?
5. What is a golden record?
6. What is the difference between an expected difference and a defect?
7. Why should thresholds be parameterized and versioned?
8. How does spec-as-code improve governance?
