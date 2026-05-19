# AGENTS.md

This repository is a Markdown-first learning system for AML / Transaction Monitoring, fintech data engineering, Azure Databricks modernization, role-based interview readiness, and active recall.

Follow these instructions whenever an agent or coding assistant works in this repo.

---

## Mission

When the user provides a source, note, screenshot summary, meeting memory, job description, article, documentation link, or project hint, convert it into a public-safe one-stop learning asset.

The output should help the user learn deeply without needing to chase scattered references.

---

## Public-safety and confidentiality

Do not commit:

- screenshots
- personal names from private notes
- private chat content
- confidential project wording
- production credentials
- real customer data
- proprietary rule logic
- evasion guidance or instructions for hiding suspicious activity

Sanitize private context into generic, public-safe case-study language.

---

## Default source-to-learning workflow

For each user-provided source:

1. **Intake**
   - Identify the topic, audience, role relevance, and tech-stack relevance.
   - Extract only public-safe learning facts.
   - Note assumptions and missing context.

2. **Research**
   - Verify unstable or current technical facts with official or primary sources.
   - Prefer regulators, government guidance, Microsoft Learn, Databricks docs, Apache Spark docs, vendor official docs, and peer-reviewed sources.
   - Add or update `docs/07-annotated-bibliography.md` when new authoritative sources are used.

3. **Design the learning asset**
   - Make the result one-stop: knowledge, theory, diagrams, examples, Q&A, mistakes, drills, and retrieval prompts.
   - Choose the right home:
     - domain foundation: `docs/01-aml-transaction-monitoring-foundations.md`
     - architecture and modernization: `docs/02-5year-lookback-azure-modernization.md`
     - rule migration: `docs/03-rule-migration-spec-as-code.md`
     - DQ and defects: `docs/04-data-quality-reconciliation-defect-management.md`
     - study system: `docs/05-make-it-stick-study-system.md`
     - practice drills: `docs/06-practice-lab-retrieval-tests.md`
     - role guides: `docs/09-role-data-engineer.md` through `docs/13-role-solution-architect-lead.md`
     - stack reference: `docs/14-tech-stack-reference.md`
   - If a new role or stack deserves its own file, add it and update the README and index.

4. **Write in this repo's style**
   - Use Markdown.
   - Use Mermaid diagrams where they clarify flow, architecture, lifecycle, or decision logic.
   - Prefer concrete AML/TM modernization examples.
   - Add low-level examples when teaching technical topics: tiny input tables, manual expected outputs, code, diagrams, and debugging exercises.
   - Include Q&A that teaches reasoning, not memorized trivia.
   - Include closed-book retrieval prompts.
   - Keep content evidence-first: data, controls, tradeoffs, failure modes, and sign-off.

5. **Validate**
   - Run `npm install` if dependencies are missing.
   - Run `npm run lint`.
   - Run `git diff --check`.
   - Fix lint or whitespace failures before finishing.

6. **Commit and push**
   - When the user asks to auto commit/push or when the task explicitly updates repository content for them, commit the changes after validation.
   - Use a clear commit message, such as `Add role-specific AML interview guides`.
   - Push the current branch to `origin`.
   - Do not rewrite history or force push unless the user explicitly asks.

---

## One-stop learning asset checklist

A strong document usually contains:

- purpose and audience
- mental model
- theory
- diagrams
- implementation or analysis playbook
- tech-stack notes
- examples
- Q&A bank
- common mistakes
- closed-book drills
- source references when new external facts are introduced

---

## Validation commands

```bash
npm run lint
git diff --check
```

---

## Commit discipline

Before committing:

- Review `git status --short`.
- Make sure no private files, screenshots, credentials, or local-only artifacts are staged.
- Prefer one cohesive commit per learning update.
- Push after commit when the user requested auto push.
