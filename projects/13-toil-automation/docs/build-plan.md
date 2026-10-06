# Build plan: Project 13, toil automation with guardrails

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how you'll know it's done.
Open hints one level at a time, after a real attempt: **Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Rough time:** 12–20 hours.

---

## Phase 0: Setup

### Task 0.1: Run what exists
**Goal:** tests pass, `cert-expiry` works, and you understand the framework.
**Done when:** you can explain what happens, step by step, when you run an action with and without `--execute`.

<details><summary>Hint 1</summary>Read <code>Runner.run</code> top to bottom. When does it refuse? What does it log?</details>

---

## Phase 1: Measure the "before"

### Task 1.1: Toil inventory
**Goal:** `docs/toil-inventory.md` with real numbers.
**Done when:** at least 6 rows, each with a frequency and minutes, ranked.

<details><summary>Hint 1</summary>No real job? Use your own work on projects 01–12: what did you repeat? Game days and break-it runs count.</details>
<details><summary>Hint 3</summary>Google SRE book, "Eliminating Toil": https://sre.google/sre-book/eliminating-toil/</details>

---

## Phase 2: Decide

### Task 2.1: ADR-0001 and ADR-0003
**Done when:** you've chosen the top items to automate *and* at least one to fix at the cause instead.

---

## Phase 3: Build

### Task 3.1: Market readiness (read-only)
**Goal:** a pre-open checklist that a human can read in 30 seconds.
**Done when:** it gives a clear GO / NO-GO with reasons, and you've tested it against a landscape fault.

<details><summary>Hint 1</summary>Which data source answers each check? Prometheus has an HTTP API; the catalog lists tier-1 services and trading hours.</details>
<details><summary>Hint 2</summary>Prometheus instant queries: <code>/api/v1/query?query=...</code>. Keep each check a small function that returns pass/fail plus a reason, so it's testable.</details>

### Task 3.2: An action that changes something
**Goal:** one changing action (e.g. restart-stuck-consumer) with `plan()` and `apply()`.
**Done when:** dry-run shows the plan, `--execute` does it, and tests cover "stuck vs slow" detection.

<details><summary>Hint 1</summary>"Stuck" and "slow" look the same in a single snapshot. What do you need to compare over time?</details>
<details><summary>Hint 2</summary>Committed offsets (from <code>kafka-consumer-groups.sh</code> or an admin client) sampled twice, N minutes apart.</details>

### Task 3.3: Your safety model
> **Depends on your ADR-0002:** per-action limits, preconditions (market hours, open incidents) or confirmation prompts each need a small framework change. Test every one.

**Done when:** a test proves each guardrail refuses what it should.

### Task 3.4: Schedule something, and know when it didn't run
**Done when:** a missed scheduled run produces a signal somewhere you'll see.

<details><summary>Hint 2</summary>Look up the "dead man's switch" / heartbeat pattern (e.g. Prometheus Pushgateway, or a healthcheck ping service).</details>

---

## Phase 4: Verify
**Done when:** before/after hours per month for each automated item, with the audit log as evidence of use.

## Phase 5: Break
**Goal:** all experiments in `docs/break-it.md`, each with a postmortem.

## Phase 6: Decide again, then improve
- [ ] ADR-0002 and ADR-0004 accepted with evidence.
- [ ] Mark which read-only actions project 14 may call during triage.

## Phase 7: Document
- [ ] Interview story with numbers.
- [ ] You can answer: "What is toil?", "What did you decide *not* to automate, and why?", "How do you stop automation from making an incident worse?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| `ModuleNotFoundError: toil` | Are you running from the project root with `python -m`? | Current directory |
| Action refused unexpectedly | How many targets did `plan()` return as changing? | Audit log `refused` event |
| Tests pass but real run fails | Do tests use the same data shapes as the real source? | Compare a real API response with your test fixture |
| Scheduled run "succeeded" but did nothing | Did it run in dry-run mode? | Audit log `execute` field |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
