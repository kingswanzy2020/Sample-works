# Build plan: Project 16, cross-service reliability reporting

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how you'll know it's done.
Open hints one level at a time, after a real attempt: **Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Rough time:** 15–25 hours, plus a few weeks of weekly reports for the trend.

---

## Phase 0: Setup

### Task 0.1: One SLO, one number
**Done when:** the report renders `order-gateway` with a real number, and you can recompute it by hand in the Prometheus UI.

<details><summary>Hint 1</summary>If you injected faults recently, the number may look terrible. That's real data, not a bug.</details>

---

## Phase 1: Measure the "before"

### Task 1.1: Ask the question the old way
**Goal:** answer "how reliable was the trading platform last week?" without this project's tooling.
**Done when:** you've written down how long it took and how confident you are. That's your "before".

---

## Phase 2: Decide

### Task 2.1: ADR-0001 and ADR-0003
**Done when:** targets and windows are decided for every tier-1 and platform service.

<details><summary>Hint 3</summary>Google SRE workbook, "Implementing SLOs": https://sre.google/workbook/implementing-slos/</details>

---

## Phase 3: Build

### Task 3.1: SLOs for every tier-1 and platform service
> **Depends on your ADR-0002:** in-house YAML means adding entries. Sloth/Pyrra/OpenSLO means writing specs in that format and deciding how the report reads them.

**Done when:** every tier-1 and platform service has at least an availability SLO, and tier-1 has a latency SLO.

<details><summary>Hint 2</summary>A latency SLI from a histogram: the share of requests faster than a threshold = bucket(le=threshold) ÷ count. The threshold must be a real bucket boundary.</details>

### Task 3.2: Trading-hours measurement (if ADR-0003 chose it)
**Done when:** tests show an outage outside trading hours doesn't count, and one inside does.

<details><summary>Hint 1</summary>An instant query over <code>[7d]</code> can't skip nights. What query type returns values over time?</details>
<details><summary>Hint 2</summary>Two common approaches: a range query with a step, filtered in Python by timestamp; or a recording rule that multiplies by a 0/1 "market open" series built from <code>hour()</code>, <code>day_of_week()</code>.</details>
<details><summary>Hint 3</summary>PromQL time functions: https://prometheus.io/docs/prometheus/latest/querying/functions/#hour. Mind the timezone: these return UTC.</details>

### Task 3.3: Composite availability
**Done when:** `composite_availability` is tested, and the report shows each tier-1 service's dependency ceiling next to its SLO.

<details><summary>Hint 1</summary>If a service needs ALL of its dependencies to work, and failures are independent, how do probabilities combine?</details>

### Task 3.4: Attribution
> **Depends on your ADR-0004.**

**Done when:** after a Kafka game day, the report attributes the burn to Kafka, with the dependents shown as impacted.

### Task 3.5: The report people read
**Done when:** someone non-technical read it and could tell you which service is the biggest reliability risk, and why.

---

## Phase 4: Verify
**Done when:** 3 weekly reports committed, and you can describe the trend in one sentence.

## Phase 5: Break
**Goal:** all experiments in `docs/break-it.md`, each with a postmortem.

## Phase 6: Decide again, then improve
- [ ] ADR-0002, ADR-0004 and ADR-0005 accepted.
- [ ] Missed SLOs exported in a form project 17 can read (owner, SLO, how much budget burned).

## Phase 7: Document
- [ ] Interview story with real numbers.
- [ ] You can answer: "SLA vs SLO?", "Why measure only trading hours?", "Your app was down because of Kafka. Whose SLO is that?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| "no data" for an SLO | Does the query return anything in the Prometheus UI? Is the window longer than the data you have? | Prometheus → Graph |
| Budget remaining like −6000% | Is the actual far below target, e.g. after fault injection? | That can be correct. Check the raw good/total numbers |
| Hours look shifted | Are you mixing UTC and local time? | Catalog timezone vs PromQL `hour()` (UTC) |
| No incidents found | Is `INCIDENTS_DIR` pointing at project 12's records? | `sources.incidents()` |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
