# Build plan: Project 14, automated alert triage

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how you'll know it's done.
Open hints one level at a time, after a real attempt: **Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Rough time:** 15–25 hours.

---

## Phase 0: Setup

### Task 0.1: Alerts flow into triage
**Goal:** landscape running, triage service running, a real alert from Alertmanager appears in `data/triage-log.jsonl`.
**Done when:** you've seen a record from a fault you injected (not just the replay fixture).

<details><summary>Hint 1</summary>Alertmanager runs in Docker; triage runs on your host. How does a container reach a port on the host? Look at the landscape's Alertmanager config.</details>
<details><summary>Hint 2</summary>Alertmanager waits <code>group_wait</code> before the first notification and retries failed deliveries. Triage must listen on all interfaces, not just localhost.</details>

---

## Phase 1: Measure the "before"

### Task 1.1: Baseline triage time
**Goal:** a game day (project 12) using bare alerts; record time from first alert to "I know who owns this and what to check".
**Done when:** you have that number for at least one scenario.

---

## Phase 2: Decide

### Task 2.1: ADR-0001, ADR-0002 and ADR-0004
**Done when:** accepted, with project 12's ADR-0004 list as input.

---

## Phase 3: Build

### Task 3.1: Enrichment
**Goal:** every record carries the context you decided on.
**Done when:** tests prove enrichment for a known service, an unknown service, and a service with missing fields (risk-engine).

<details><summary>Hint 1</summary>Not every alert carries a <code>service</code> label the same way. Check what labels each landscape rule actually produces.</details>
<details><summary>Hint 2</summary>Runbook age: the catalog has <code>runbook_updated</code>. What threshold makes a runbook "stale", and should that be visible in the page?</details>

### Task 3.2: Correlation
> **Depends on your ADR-0002:** time windows need state and a clock. Topology needs the `depends_on` graph walked in the right direction.

**Done when:** `kafka-storm.json` produces one group with kafka as probable cause, and `double-trouble` produces two.

<details><summary>Hint 1</summary>If A depends on B and both alert, which one is more likely the cause?</details>
<details><summary>Hint 2</summary>Walk <code>depends_on</code> transitively: risk-engine → positions-api → kafka.</details>
<details><summary>Hint 3</summary>Write the tests first from the two fixtures. Make a second fixture for <code>double-trouble</code>.</details>

### Task 3.3: Routing, including unowned services
**Done when:** routing follows your on-call design (project 12 ADR-0003), and an unowned-service alert goes somewhere deliberate, with a note.

### Task 3.4: Read-only diagnostics
**Done when:** at least two diagnostics run per alert with timeouts, and a hanging check can't delay the page beyond your budget.

<details><summary>Hint 2</summary>Prometheus HTTP API for dependency health; the simulator's <code>/state</code>; project 13's read-only actions.</details>

### Task 3.5: Fail open
> **Depends on your ADR-0004.**

**Done when:** you've stopped triage, injected a fault, and a page still arrived.

<details><summary>Hint 2</summary>An Alertmanager route can have <code>continue: true</code> to deliver to more than one receiver.</details>

### Task 3.6: Feedback loop
**Goal:** responders can mark an alert actionable or not, easily.
**Done when:** `feedback.jsonl` gets entries from your game days. Project 17 needs this data.

---

## Phase 4: Verify
**Done when:** a game day with triage on vs the Phase 1 baseline, same scenario, times compared.

## Phase 5: Break
**Goal:** all experiments in `docs/break-it.md`, each with a postmortem.

## Phase 6: Decide again, then improve
- [ ] ADR-0003 and ADR-0005 accepted.
- [ ] Correlation state survives a restart, or the ADR explains why it doesn't need to.

## Phase 7: Document
- [ ] Interview story with before/after numbers.
- [ ] You can answer: "How do you avoid merging unrelated incidents?", "What if your triage service is down?", "What would you never automate?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| Nothing arrives from Alertmanager | Can the Alertmanager container reach host port 8080? Is triage bound to 0.0.0.0? | Alertmanager logs ("notify" errors); `extra_hosts` |
| 422 errors on /alerts | Does the payload match the model? | FastAPI error detail; `triage/models.py` |
| Same alert recorded repeatedly | Is Alertmanager re-sending on `repeat_interval` / group changes? | Alertmanager config; dedupe by fingerprint |
| Groups lost after restart | Where does correlation state live? | ADR-0002 / Phase 6 |
| Tests can't find the catalog | Which path does `catalog.load()` try? | `CATALOG` env var |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
