# Build plan: Project 12, incident response and on-call

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how you'll know it's done.
Open hints one level at a time, after a real attempt: **Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Rough time:** 12–20 hours, spread over several game days.

---

## Phase 0: Setup

### Task 0.1: Landscape running, faults visible
**Goal:** start the landscape, inject a fault by hand, and see an alert fire.
**Done when:** you've seen `KafkaDegraded` (or another alert) firing in Alertmanager, then cleared it.

<details><summary>Hint 1</summary>Alerts need time: a rate window plus the rule's <code>for:</code> duration. How long is that for each rule?</details>

### Task 0.2: Read the platform like a new joiner
**Goal:** read the catalog, the alerts and the runbooks, and write down what you'd want to know before your first on-call shift.
**Done when:** you have a list of at least 5 gaps. Keep it: it feeds projects 15 and 17.

---

## Phase 1: Measure the "before"

### Task 1.1: A game day with no process
**Goal:** run one blind game day before writing any process.
**Done when:** you have an honest timeline and an incident record, even if it's messy.

<details><summary>Hint 1</summary>Write the timeline <em>as it happens</em>, with timestamps. Reconstructing it afterwards is always wrong.</details>

---

## Phase 2: Decide

### Task 2.1: ADR-0001 to ADR-0003 and the `process/` docs
**Done when:** every prompt in `process/` is replaced with your policy, and the ADRs justify it.

<details><summary>Hint 3</summary>Google SRE book, "Managing Incidents": https://sre.google/sre-book/managing-incidents/; PagerDuty's open incident response docs: https://response.pagerduty.com/</details>

---

## Phase 3: Build

### Task 3.1: Run the process in game days 1–4
**Done when:** each has an incident record that validates against `SCHEMA.md` and a postmortem.

<details><summary>Hint 1</summary>"Detected" means when a human or alert noticed, not when you started looking at the dashboard because you knew a game day was on.</details>

### Task 3.2: Validate incident records automatically
**Goal:** a small script that checks every `incidents/*.yaml` has the required fields and sensible timestamps.
**Done when:** it fails on a record with `detected` before `started`, or an action with no owner.

<details><summary>Hint 1</summary>16 and 17 will read these files. Bad data here becomes wrong reports there.</details>

### Task 3.3: Fix what the game days exposed
**Goal:** at least one process change and one runbook rewrite driven by evidence.
**Done when:** a superseding ADR or a runbook diff links to the game day that justified it.

---

## Phase 4: Verify
**Done when:** you can show the trend across game days (detect/mitigate times, time to first update).

## Phase 5: Break
**Goal:** game days 5 and 6 from `docs/break-it.md`.

## Phase 6: Decide again, then improve
- [ ] ADR-0004 lists the triage steps to hand to project 14, each with its time cost.
- [ ] ADR-0005 accepted; every action item from your game days has an owner, a due date and a status.

## Phase 7: Document
- [ ] Interview story with real times.
- [ ] You can answer: "Tell me about an incident you led", "How do you run an incident with two people?", "How do you make postmortems blameless?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| No alert fires after injection | Has the rule's window + `for:` elapsed? Does a rule cover that service at all? | Prometheus → Alerts (pending) |
| `game_master.py` can't connect | Is the simulator running on :9200? | `docker compose ps` in landscape |
| Everything seems to fail at once | Is one dependency causing it? | Catalog `depends_on`; simulator `/state` |
| Timeline doesn't match the reveal | Did you record when *impact* started, or when you noticed? | Injection log vs your notes |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
