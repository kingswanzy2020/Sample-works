# Build plan: Project 17, reliability governance

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how you'll know it's done.
Open hints one level at a time, after a real attempt: **Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Rough time:** 15–25 hours, plus 3+ weeks of weekly reviews.

---

## Phase 0: Setup

### Task 0.1: Scorecard runs on sample data
**Done when:** `python -m governance.scorecard` shows the ownership findings, and you've read every sample-data file.

---

## Phase 1: Measure the "before"

### Task 1.1: Find the problems by hand first
**Goal:** read the sample data (and the landscape catalog and runbooks) and list every problem you can find, with numbers.
**Done when:** you have a list. That's the answer key your metrics must reproduce.

<details><summary>Hint 1</summary>Group alerts by name and service; count; join with feedback. Look at incident root causes over time. Look at action due dates vs today.</details>

---

## Phase 2: Decide

### Task 2.1: ADR-0001 and ADR-0004
**Done when:** every metric has a precise definition (numerator, denominator, window, minimum sample size), and a counter-metric.

<details><summary>Hint 3</summary>Google SRE workbook, "On-Call" (pages per shift, actionable alerts): https://sre.google/workbook/on-call/</details>

---

## Phase 3: Build

### Task 3.1: Implement the metrics
**Done when:** each metric is tested on small hand-written inputs, and on the sample data it finds the problems from Phase 1.

<details><summary>Hint 1 (alert quality)</summary>Join triage records to feedback by <code>fingerprint</code>. Alerts with no feedback are a third category, not "not actionable".</details>
<details><summary>Hint 1 (runbook quality)</summary>Three different failures: missing, old, and "used but didn't help". Which one does each data source tell you?</details>
<details><summary>Hint 1 (follow-through)</summary>A repeat incident with the same root cause while an action from the first one is still open is a strong finding.</details>

### Task 3.2: The scorecard format
> **Depends on your ADR-0002:** a public view needs careful wording and no rankings (or deliberate rankings). Private views need per-team output.

**Done when:** the scorecard output is something you'd be comfortable sending to the team it's about.

### Task 3.3: Switch to real data
**Done when:** the scorecard runs on data from projects 12 and 14 (and 15/16 if done), via the env vars in `governance/sources.py`.

### Task 3.4: Run weekly reviews
**Done when:** 3 reviews in `review/`, using the templates, each with findings written to `review/finding-template.md` standard.

### Task 3.5: Drive one finding to done
**Done when:** a finding went from evidence → conversation → change → metric improved, and you documented each step.

<details><summary>Hint 1</summary>Pick the finding with the clearest evidence and the cheapest fix first. Early wins build trust for the harder ones.</details>

---

## Phase 4: Verify
**Done when:** every success criterion has evidence (tests, scorecards, reviews, the fixed finding).

## Phase 5: Break
**Goal:** all experiments in `docs/break-it.md`, each with a postmortem.

## Phase 6: Decide again, then improve
- [ ] ADR-0002, ADR-0003 and ADR-0005 accepted; `review/escalation-policy.md` written.
- [ ] At least one metric changed because it was gamed or misleading (superseding ADR).

## Phase 7: Document
- [ ] Interview story with real numbers.
- [ ] You can answer: "How do you get a team you don't manage to fix their alerts?", "How do you stop metrics being gamed?", "What's a good page?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| Empty results | Did you run `sample-data/generate.py`? Do the env vars point somewhere real? | `governance/sources.py` |
| Percentages jump around week to week | Is the sample size too small to mean anything? | Your ADR-0001 minimum sample size |
| Findings feel unfair to a team | Does the metric account for things outside their control (dependencies, project 16 attribution)? | ADR-0001 counter-metrics |
| Nobody acts on findings | Is each one specific, evidenced, with one ask and a due date? | `review/finding-template.md` |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
