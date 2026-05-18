# 01 — AML / Transaction Monitoring Foundations

## 1. The purpose of AML/TM

Anti-money laundering and transaction monitoring programs help financial institutions identify activity that may require review, investigation, escalation, or reporting. A transaction monitoring system is not the same as a law-enforcement system. It is a risk-control system that helps a reporting entity decide whether observed facts, context, and indicators meet the threshold for escalation.

A practical AML/TM data professional should understand four layers:

```text
Regulatory obligation
    ↓
Risk assessment and policy
    ↓
Monitoring scenarios and alert generation
    ↓
Review, case disposition, reporting, feedback, and evidence
```

The work of a data engineer or analyst is to make this process reliable, traceable, and testable.

---

## 2. Core vocabulary

| Term | Practical meaning |
|---|---|
| AML | Anti-money laundering control framework. |
| CFT/CTF | Countering terrorist financing. |
| TM | Transaction monitoring. Usually rules, scenarios, models, and workflows that detect activity needing review. |
| STR/SAR | Suspicious Transaction Report / Suspicious Activity Report, depending on jurisdiction. |
| KYC | Know Your Customer. Customer identity, profile, occupation/business, beneficial ownership, and expected activity. |
| CDD | Customer Due Diligence. Baseline understanding of the customer. |
| EDD | Enhanced Due Diligence. Additional review for higher-risk relationships. |
| Scenario | A detection pattern, usually expressed as a rule/model with thresholds and conditions. |
| Alert | System-generated item that requires review. |
| Case | Investigation unit that may contain one or more alerts and supporting information. |
| Disposition | Investigator decision or case outcome. |
| False positive | Alert reviewed and not escalated as suspicious. |
| Threshold | Numeric or logical trigger value used by a rule. |
| Tuning | Adjusting rules/thresholds/segmentation to improve effectiveness and reduce noise. |
| Lineage | Ability to trace output back to source data and transformations. |

---

## 3. The risk-based approach

A risk-based approach means controls should be designed around the level and type of risk. A monitoring program should consider factors such as:

- customer type and customer risk rating
- products and services
- transaction channels
- geography
- expected versus observed behavior
- beneficial ownership and relationship context
- new technologies and delivery channels
- past alerts, cases, and reporting outcomes

For data work, this means risk attributes are not decorative metadata. They often drive scenario eligibility, threshold selection, alert priority, and case-routing logic.

Example:

```text
Same transaction amount
  + low-risk customer with expected business behavior
  -> may not trigger or may receive lower priority

Same transaction amount
  + high-risk customer, unusual geography, unexpected channel
  -> may trigger a scenario or receive higher priority
```

---

## 4. Facts, context, indicators

A transaction monitoring system should preserve three categories of information.

### Facts

Facts are directly observable data points.

Examples:

- transaction date
- transaction amount
- account identifier
- customer identifier
- channel
- currency
- country or region code
- counterparty identifier, where available

### Context

Context explains what the facts mean for this customer or relationship.

Examples:

- customer occupation or business type
- expected activity level
- historical transaction pattern
- relationship length
- risk rating
- product type
- business purpose

### Indicators

Indicators are red flags or patterns that may require review. They are not proof by themselves; they must be interpreted with facts and context.

Examples at a safe, defensive level:

- activity inconsistent with known customer profile
- unusual increase in volume or frequency
- use of higher-risk geography or product/channel combinations
- relationship links that do not fit the expected business purpose
- repeated activity that requires explanation

A strong alert package does not only say “threshold exceeded.” It explains the relevant facts, context, and indicators.

---

## 5. Typical transaction monitoring data model

A simplified AML/TM data model often includes:

```text
customer
  customer_id
  name/entity fields
  customer_type
  risk_rating
  occupation/business
  onboarding_date
  kyc_review_date

account
  account_id
  customer_id
  product_type
  open_date
  close_date
  status

transaction
  transaction_id
  account_id
  transaction_date
  amount
  currency
  direction
  channel
  transaction_type
  counterparty_id
  country_code

reference_data
  country_code
  country_risk_level
  currency_code
  product_risk_level
  scenario_thresholds

alert
  alert_id
  rule_id
  rule_version
  customer_id
  account_id
  alert_date
  trigger_reason
  supporting_transaction_ids

case
  case_id
  alert_ids
  investigator_id
  disposition
  decision_date
```

In a real platform, each of these may come from separate systems and may change over time. Historical projects must account for that.

---

## 6. Alert lifecycle

```text
1. Data lands from source systems.
2. Data is validated, standardized, and stitched.
3. Scenarios/rules run against eligible population.
4. Alerts are generated when conditions are met.
5. Alerts are enriched with supporting facts and context.
6. Alerts move to review/case workflow.
7. Investigator disposition creates feedback.
8. Analytics teams use feedback for tuning and quality monitoring.
9. Governance teams review evidence, metrics, and defects.
```

Important distinction:

- A rule trigger is a system event.
- An alert is a review object.
- A case is an investigation object.
- A report is a regulated filing decision.

Do not collapse these into one concept.

---

## 7. What transaction monitoring rules look like

Many TM scenarios use combinations of:

- filters
- joins
- time windows
- aggregations
- thresholds
- reference lists
- customer segmentation
- exclusion rules
- output formatting

Generic example:

```sql
SELECT
    c.customer_id,
    COUNT(*) AS transaction_count,
    SUM(t.amount) AS total_amount
FROM transactions t
JOIN accounts a
  ON t.account_id = a.account_id
JOIN customers c
  ON a.customer_id = c.customer_id
JOIN country_risk r
  ON t.country_code = r.country_code
WHERE t.transaction_date >= DATEADD(day, -30, CURRENT_DATE)
  AND r.risk_level = 'HIGH'
  AND c.customer_status = 'ACTIVE'
GROUP BY c.customer_id
HAVING SUM(t.amount) > :threshold_amount;
```

This simple pattern hides many real questions:

- Which customer risk rating should be used: current or historical?
- What if country risk changed during the 30-day window?
- Are reversals included?
- Are internal transfers excluded?
- How are currency conversions handled?
- What if an account changed ownership?
- What if the same transaction appears in two source systems?

These questions define the real implementation complexity.

---

## 8. False positives and tuning

A false positive is not always a system failure. Monitoring is designed to generate reviewable signals. However, excessive false positives can reduce operational effectiveness and bury meaningful alerts.

Tuning can involve:

- threshold adjustment
- customer segmentation
- exclusion logic
- better reference data
- better point-in-time context
- better scenario eligibility filters
- prioritization models
- investigator-feedback analysis

Tuning should be governed. A tuning change should have:

- rationale
- before/after impact
- alert volume impact
- risk impact assessment
- test results
- approval
- effective date
- rollback plan

---

## 9. Red flags for weak AML/TM data systems

A system is weak if:

- alerts cannot be traced back to source records
- rules are coded but not documented
- thresholds exist in code only
- DQ exceptions are silently dropped
- historical reference data is missing
- defects lack root cause
- output mismatches are explained verbally but not evidenced
- reruns produce different results without explanation
- investigators cannot see why an alert triggered
- tuning decisions lack impact analysis

---

## 10. What to memorize

Memorize this compact model:

```text
AML/TM = Risk-based monitoring + explainable alerts + investigation workflow + reporting obligations + evidence.
```

And this implementation model:

```text
Customer + Account + Transaction + Reference Data + Rule Version + Time Window
    -> Alert
    -> Review / Case
    -> Feedback / Reporting / Governance
```

---

## 11. Active recall questions

Close this file and answer from memory:

1. What is the difference between facts, context, and indicators?
2. Why is an alert not the same as a report?
3. What data domains are needed to run most transaction monitoring scenarios?
4. Why does point-in-time data matter for historical monitoring?
5. What makes tuning risky if it is not governed?
6. Why are false positives not always a sign of failure?
7. How would you explain transaction monitoring to a non-technical person in three sentences?
8. What evidence should accompany an alert so an investigator can understand it?
