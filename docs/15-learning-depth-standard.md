# 15 - One-Stop Learning Depth Standard

This repo should not produce thin summaries. A one-stop learning asset should
let the learner understand, explain, practice, debug, and defend the topic
without immediately leaving the repo.

The goal is not to make every file huge. The goal is to make every major section
serious.

---

## 1. What "deep" means here

A deep section answers more than "what is this?"

It should answer:

1. What problem does this solve?
2. What is the first-principles mental model?
3. What are the core concepts and vocabulary?
4. What does it look like in the AML/TM modernization case study?
5. What are the implementation or analysis steps?
6. What can go wrong?
7. How do we detect, reconcile, or govern failure?
8. What evidence proves the result?
9. How would I explain it in an interview?
10. How do I test my memory without looking?

If a section only has a definition and two bullets, it is not done.

---

## 2. Section Depth Contract

Every major learning section should include most of these pieces.

| Piece | Purpose | Example |
|---|---|---|
| Purpose | Why the section exists | "Use this to explain rule replay design." |
| First principles | The simplest mental model | "A lookback is replay plus proof." |
| Key vocabulary | Terms the learner must own | batch ID, rule version, point-in-time join |
| Diagram | Visual structure or flow | source to bronze to silver to alerts |
| AML/TM example | Concrete sanitized scenario | high-risk wire rule replay |
| Step-by-step playbook | What to do in order | inventory, map, test, compare, sign off |
| Failure modes | How it breaks | row explosion, stale reference data, duplicate alerts |
| Controls/evidence | How to prove correctness | DQ checks, reconciliation, logs, approvals |
| Stack notes | Tool-specific relevance | Databricks, Delta, Lakeflow, Power BI |
| Interview framing | How to say it clearly | strong answer shape and tradeoffs |
| Practice/drills | Retrieval and application | closed-book prompts and what-if changes |
| Source map | Why the claims are trusted | official docs, regulators, primary sources |

Not every small section needs all twelve pieces, but every major topic should.

---

## 3. Depth Levels

Use these levels when reviewing existing docs.

| Level | Meaning | Signs |
|---|---|---|
| 0 - Stub | Placeholder | heading, one paragraph, no example |
| 1 - Summary | Intro only | definitions and bullets, little application |
| 2 - Useful | Teaches basics | examples, some pitfalls, some questions |
| 3 - One-stop | Serious learning unit | theory, examples, diagrams, failure modes, evidence, drills |
| 4 - Practicum | Runnable or production-like | notebook, validation, scenarios, debugging, sign-off pack |

Target:

- Role guides should reach Level 3.
- Spark/PySpark/Spark SQL practice should reach Level 4 through notebooks.
- Stack reference sections should reach Level 3, with notebook links for code.
- Landing pages can be shorter, but should explain how to reach Level 3 or 4.

---

## 4. What Not To Do

Do not "deepen" a document by only adding:

- more trivia questions
- more links
- generic definitions
- long lists of tools
- interview buzzwords
- copied vendor marketing language
- code snippets in Markdown that should be notebook cells

Depth means more reasoning, more examples, more failure analysis, more evidence,
and more practice.

---

## 5. Required Pattern For Technical Sections

Technical sections should follow this shape:

```text
1. Concept
2. Why it matters in AML/TM
3. Diagram or row-grain explanation
4. Implementation playbook
5. Failure modes
6. Evidence and validation
7. Interview answer
8. Closed-book drill
9. Notebook link when code is involved
```

Example for point-in-time joins:

```text
Concept:
  Join facts to the dimension row effective at the business date.

Why it matters:
  Customer risk and account status can change. Historical rules must use the
  correct historical state.

Failure mode:
  Joining to the latest dimension can create false positives or false negatives.

Evidence:
  Boundary tests, unmatched reference rows, effective-date coverage, and sample
  joined records.
```

---

## 6. Required Pattern For Role Sections

Role sections should not only say what the role does. They should teach how the
role thinks.

Each role topic should include:

- mission of the role
- decisions the role owns
- artifacts the role produces
- tools and stack pieces the role must understand
- common interview traps
- project examples
- quality bar
- evidence of good work
- escalation and collaboration points
- closed-book drills

Example:

```text
Data Engineer depth is not "knows PySpark."
It is "can design rerunnable, governed, reconciled pipelines that preserve
business behavior and produce evidence."
```

---

## 7. Required Pattern For Q&A

Q&A should be used to test reasoning, not to decorate the page.

Good Q&A:

- asks about tradeoffs
- forces the learner to explain failure modes
- connects tools to business controls
- includes a strong answer, not just a phrase
- puts the model answer in the same file, near the question
- reveals what evidence proves the answer

Weak Q&A:

- asks for a definition only
- has one-sentence answers
- leaves the learner with no answer key
- repeats vendor wording
- does not connect to AML/TM or the project story

Good question:

```text
Q: Why can a row-count reconciliation pass while alert output is still wrong?
```

Good answer shape:

```text
Because row counts only prove volume movement, not business correctness.
Amounts, keys, point-in-time reference joins, thresholds, dedupe rules, and
supporting transaction evidence can still be wrong.
```

---

## 8. Required Pattern For Examples

Examples should be small enough to reason about and complete enough to trust.

Every example needs:

- tiny public-safe input rows
- expected output
- explanation of why those rows survive or fail
- validation or reconciliation
- failure interpretation

If the example uses PySpark, Python, Spark SQL, or PySQL-style logic, the
runnable version belongs in a notebook.

Markdown should include:

- purpose
- data shape
- expected output
- diagram
- notebook link
- what to change for practice

---

## 9. Required Pattern For Diagrams

Diagrams should clarify one of these:

- data flow
- ownership boundary
- lifecycle
- decision logic
- failure path
- evidence path
- role responsibility
- architecture layer

Weak diagram:

```text
Tool A -> Tool B -> Tool C
```

Better diagram:

```text
Source extract -> bronze immutable table -> DQ checks -> silver standardized
table -> rule-ready gold table -> alert output -> reconciliation evidence
```

Best diagram:

```text
Show where failures are caught, where evidence is emitted, and which role owns
the decision.
```

---

## 10. Required Pattern For Drills

Closed-book drills should force the learner to retrieve and apply.

Every drill section must include a nearby model answer in the same file. The
shared model answer bank can duplicate or summarize answers, but it cannot be
the only place where the learner finds the answer.

Use drill types:

- explain from memory
- predict row movement
- draw the architecture
- identify failure mode
- choose a control
- compare two designs
- write the sign-off evidence
- answer as a specific role

Bad drill:

```text
What is Delta Lake?
```

Better drill:

```text
Explain why Delta Lake helps a June 2022 rule rerun, then name two things Delta
does not solve by itself.
```

---

## 11. Depth Audit For Current Repo

This audit guides future improvements.

| Area | Current depth | Upgrade direction |
|---|---|---|
| Spark deep guide | Level 3 to 4 | Keep migrating runnable code from Markdown into notebooks. |
| Spark notebooks | Level 4 | Continue adding runnable first-principles labs. |
| Tech stack reference | Level 3 | Keep examples notebook-linked; add diagrams and evidence where gaps appear. |
| Role guides | Level 2 to 3 | Add deeper per-section playbooks, artifacts, failure modes, and role-specific evidence. |
| Domain foundations | Level 2 to 3 | Add more scenario reasoning, case lifecycle examples, and control evidence. |
| DQ/reconciliation | Level 2 to 3 | Add more defect triage patterns and notebook-linked DQ labs. |
| SQL landing page | Level 1 | Keep as an index, but clarify paths to Level 3 and Level 4 learning. |
| ML landing page | Level 1 | Keep as an index, but add a role/learning path map. |
| Templates | Level 2 | Keep templates aligned with notebook-first examples and evidence-first learning. |

Priority order:

1. Convert legacy Spark Markdown code blocks into notebook sections.
2. Deepen each role guide section beyond definitions and Q&A.
3. Deepen domain and DQ docs with failure paths, evidence packs, and drills.
4. Expand landing pages only enough to guide the learner to the deep assets.

---

## 12. Review Checklist

Before committing a learning update, ask:

1. Does each major section explain why the topic matters?
2. Does it include a first-principles mental model?
3. Does it include a concrete AML/TM modernization example?
4. Does it include failure modes?
5. Does it include controls or evidence?
6. Does it include practice, drills, or retrieval prompts?
7. Does code live in notebooks when it is PySpark, Python, Spark SQL, or PySQL?
8. Does the Markdown link to the runnable notebook section?
9. Does the section teach reasoning, not only terms?
10. Would a learner still need to leave the repo immediately to understand the topic?

If the answer to question 10 is yes, the section is not deep enough yet.
