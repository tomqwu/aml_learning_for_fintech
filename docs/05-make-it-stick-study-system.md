# 05 — Make-It-Stick Study System for AML/TM + Azure Modernization

## 1. Why this study system works

This repository is built around active learning principles:

- **Retrieval practice:** close the notes and pull the idea from memory.
- **Spaced repetition:** revisit the material after delay.
- **Interleaving:** mix AML domain, data engineering, DQ, and governance so you learn when to use which concept.
- **Elaboration:** connect new ideas to things you already understand.
- **Desirable difficulty:** make practice hard enough that your brain must work.
- **Feynman explanation:** explain in plain language until the idea is clear.

The point is not to feel fluent while reading. The point is to perform when the notes are closed.

---

## 2. Active Recall Architect

Use this after each file.

### Prompt template

```text
I am studying [TOPIC]. Act as a learning coach.
Generate 5 challenging open-ended questions that require me to explain the core concepts from memory.
Do not provide the answers yet.
After I answer, grade my responses and explain gaps in my logic.
```

### AML/TM version

```text
I am studying AML transaction monitoring foundations.
Ask me 5 open-ended questions that test whether I can explain:
- risk-based monitoring
- facts/context/indicators
- alert vs case vs report
- customer/account/transaction data model
- why evidence matters
Do not give answers until I answer first.
```

### Azure modernization version

```text
I am studying a 5-year transaction monitoring lookback on Azure.
Ask me 5 open-ended questions that test whether I can explain:
- historical replay
- point-in-time data
- ADLS/ADF/Databricks/Delta/Fabric/Purview roles
- partitioning and idempotence
- reconciliation and audit evidence
Do not give answers until I answer first.
```

---

## 3. 30-day spaced repetition schedule

Use the schedule below after your first full pass through the material. Review sessions are intentionally short. Spend 3 minutes retrieving, then 7–15 minutes repairing gaps.

| Day | Review focus | 3-minute quick-fire retrieval exercise |
|---:|---|---|
| 1 | Big picture | Explain the whole AML/TM modernization case in 90 seconds. Then list the five core mental models. |
| 2 | AML/TM foundations | Define alert, case, STR/SAR, scenario, false positive, KYC, CDD, EDD, and risk rating from memory. |
| 3 | No formal review | Write one sentence connecting AML risk to data engineering. |
| 4 | Azure architecture | Draw source -> bronze -> silver -> gold -> rule -> alert -> evidence from memory. |
| 5 | No formal review | Recall three Azure components and their roles. |
| 6 | No formal review | Name two reasons point-in-time data matters. |
| 7 | Rule migration | Explain why migration is equivalence before optimization. Then list rule-spec sections. |
| 8 | No formal review | Recall three legacy migration failure modes. |
| 9 | No formal review | Explain deterministic alert keys in one sentence. |
| 10 | No formal review | Write one example of a rule boundary test. |
| 11 | DQ/reconciliation | List ten DQ dimensions and give one check for each. |
| 12 | No formal review | Recall three reconciliation metrics beyond row count. |
| 13 | No formal review | Explain defect categories from memory. |
| 14 | No formal review | State what belongs in an evidence pack. |
| 15 | No formal review | Explain false positives vs rule defects. |
| 16 | Interleaving | Solve one mixed scenario: a rule mismatch after a backfill. Diagnose domain, data, and engineering causes. |
| 17 | No formal review | Draw customer-account-transaction-reference-alert relationships. |
| 18 | No formal review | Explain batch ID to a non-technical person. |
| 19 | No formal review | List five questions to ask before changing a threshold. |
| 20 | No formal review | Explain why current reference data can break a lookback. |
| 21 | No formal review | Write a one-paragraph summary from memory, then check notes. |
| 22 | Spec-as-code | Recreate the YAML rule spec headings from memory. |
| 23 | No formal review | Recall four approval gates for production deployment. |
| 24 | No formal review | Explain the difference between source, mapping, and rule defects. |
| 25 | No formal review | Name three dashboard metrics for alert analytics. |
| 26 | No formal review | Explain why lineage supports compliance and debugging. |
| 27 | No formal review | Recall a full defect lifecycle without looking. |
| 28 | No formal review | Explain the architecture as if to a 10-year-old. |
| 29 | No formal review | Attempt five questions from `06-practice-lab-retrieval-tests.md`. |
| 30 | Final synthesis | Write a one-page closed-book explanation of the entire field and compare it to `README.md`. |

---

## 4. Interleaving Engine

Interleaving means mixing topics so you practice selecting the right tool.

### Topics to mix

- **Topic A:** AML/TM domain logic
- **Topic B:** Azure data engineering
- **Topic C:** DQ/reconciliation/defects

### Interleaved session: 45 minutes

#### Scenario 1 — Alert spike

A migrated rule produces twice as many alerts in Azure as legacy for the same month.

Switch between:

- AML: Is this rule interpretation, threshold, customer segmentation, or expected behavior?
- Azure: Did the pipeline duplicate data or mis-handle partitions?
- DQ: Are counts, amounts, and eligible populations reconciled?

#### Scenario 2 — Missing alerts

Legacy produces alerts for customers who are absent in Azure output.

Switch between:

- AML: Were those customers eligible under the rule?
- Azure: Did customer/account stitching fail?
- DQ: Are there orphaned transactions or missing point-in-time references?

#### Scenario 3 — Reference data change

A country risk table changed in 2024, but the lookback covers 2020–2024.

Switch between:

- AML: Which risk level should apply to 2021 transactions?
- Azure: How should effective dates be modeled?
- DQ: How do you test reference coverage?

#### Scenario 4 — Performance issue

A rule takes 14 hours to process one year.

Switch between:

- AML: Can the scenario be segmented by risk/customer group?
- Azure: Are partitions, joins, and file sizes optimized?
- DQ: Can partial outputs be trusted if the job fails halfway?

#### Scenario 5 — Business asks for threshold change

Business wants to reduce alert volume before sign-off.

Switch between:

- AML: What is the risk impact?
- Azure: How do you parameterize and version the threshold?
- DQ/Governance: What evidence and approvals are required?

---

## 5. Elaboration Specialist

Use elaboration to connect new AML/TM ideas to something familiar.

### Mental bridge: AML/TM pipeline as a school exam system

| AML/TM concept | School metaphor |
|---|---|
| Source data | Student answers collected from classrooms. |
| DQ checks | Confirm each answer sheet has name, date, and no missing pages. |
| Rule logic | Grading rubric. |
| Alert | Answer that needs teacher review. |
| Case | Teacher investigation into a pattern. |
| Evidence pack | Graded work, rubric, notes, and audit trail. |
| Reconciliation | Did every answer sheet make it from classroom to grading system? |
| Defect | Missing page, wrong rubric, duplicate sheet, or system error. |

### Deep elaboration questions

1. If AML/TM is like grading exams, what is the equivalent of a grading rubric changing halfway through the year?
2. If data stitching is like matching student names to classes, what happens when two students have the same name or one student changes classes?
3. If a lookback is like regrading five years of exams, why do you need the old rubrics and old class rosters, not just today’s versions?

---

## 6. Desirable Difficulty Designer

Make practice harder so learning sticks.

### Fill-in-the-blank

1. A lookback fails point-in-time correctness when it uses ________ reference data instead of ________ reference data.
2. A pipeline is idempotent when rerunning it produces ________ rather than ________.
3. A rule spec should include business intent, input data, eligibility, logic, output, controls, and ________.
4. A reconciliation report should compare more than row count; it should also compare ________, ________, and ________.
5. A defect should not be closed until there is root cause, fix description, retest result, and ________.

### Reverse-engineering task

Given this output:

```text
Rule TM001 generated 0 alerts for March 2022.
Source transaction count: 10,000,000.
Gold rule input count: 8,000,000.
DQ exception count: 2,000,000.
Most exceptions: missing account_id.
```

Explain:

1. Why zero alerts may not mean low risk.
2. Which defect category is likely.
3. Which reconciliation level failed.
4. What evidence you need before sign-off.

### Constraint task

Explain a 5-year lookback without using these words:

```text
pipeline, data, rule, Azure, alert
```

This forces you to find a simpler mental model.

---

## 7. Mental Model Refiner / Feynman Technique

### Explain like age 10

A transaction monitoring system is like a careful checker at a bank. It watches for money activity that does not fit what the bank normally expects. If something looks unusual, it creates a note for a person to review. The system must also remember exactly why it created the note, so another person can check whether the system made a fair decision.

### Explain back prompt

```text
Explain why the system must remember exactly why it created an alert.
Use no jargon. Use an example, but keep it simple.
```

### Jargon detector

If your explanation uses any of these words, simplify:

```text
lineage, reconciliation, orchestration, idempotent, reference data, segmentation, typology
```

Translate them:

| Jargon | Plain language |
|---|---|
| lineage | where something came from and how it changed |
| reconciliation | checking that two sides match |
| orchestration | making steps run in the right order |
| idempotent | safe to run again without making duplicates |
| reference data | lookup lists used by the system |
| segmentation | grouping similar customers or activity |
| typology | known pattern of concern |

---

## 8. Meeting-to-Memory Converter

After a meeting, do not write only notes. Convert notes into application tests.

### Template

```text
Meeting topic:
Main decisions:
Open questions:
Risks:
Owners:
Evidence needed:

What-if test 1:
What if [a related input changes]? What should we do?

What-if test 2:
What if [a defect appears]? How do we classify it?

What-if test 3:
What if [business asks for a change]? What evidence is needed?

What-if test 4:
What if [output does not match]? How do we investigate?

What-if test 5:
What if [audit asks for proof]? What artifact do we show?
```

### Example

Meeting decision:

```text
Use transaction_date for monitoring windows, not posting_date.
```

Retrieval tests:

1. What if posting_date and transaction_date differ by 10 days?
2. What if legacy used posting_date by mistake?
3. What reconciliation metric would reveal the difference?
4. What rule spec section must capture this decision?
5. What evidence would prove the Azure implementation follows the decision?

---

## 9. Weekly self-exam format

Every week, write one page from memory:

```text
1. What did I learn?
2. What can I explain without notes?
3. What still feels fuzzy?
4. What scenario exposed my weakness?
5. What will I retrieve again next week?
```

Score yourself:

| Score | Meaning |
|---|---|
| 1 | I only recognize the terms. |
| 2 | I can define terms but cannot apply them. |
| 3 | I can apply concepts to simple examples. |
| 4 | I can diagnose realistic scenarios. |
| 5 | I can explain tradeoffs, evidence, and failure modes. |

---

## 10. Core learning-science references

- Roediger and Karpicke, “Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention,” Psychological Science, 2006. https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x
- Dunlosky et al., “Improving Students’ Learning With Effective Learning Techniques,” Psychological Science in the Public Interest, 2013. https://journals.sagepub.com/doi/10.1177/1529100612453266
- Bjork Learning and Forgetting Lab research overview. https://bjorklab.psych.ucla.edu/research/
