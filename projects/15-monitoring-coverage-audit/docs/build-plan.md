# Build plan: Project 15, monitoring coverage audit

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how you'll know it's done.
Open hints one level at a time, after a real attempt: **Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Rough time:** 12–20 hours.

---

## Phase 0: Setup

### Task 0.1: Scanner runs against the landscape
**Done when:** with a temporary standard requiring `has_metrics`, the scan prints PASS rows for live services.

---

## Phase 1: Measure the "before"

### Task 1.1: Inventory by hand first
**Goal:** a table of every landscape service and what monitoring it actually has today (metrics, alerts, runbooks, probes).
**Done when:** you've found the gaps manually. This is the answer key your scanner must reproduce.

<details><summary>Hint 2</summary>Prometheus's rules API (<code>/api/v1/rules</code>) lists every loaded rule with its query text.</details>

---

## Phase 2: Decide

### Task 2.1: ADR-0001 and ADR-0002, then fill in `monitoring-standard.yaml`
**Done when:** every tier has a required list, and each check is justified by a game day, a break-it or a principle.

---

## Phase 3: Build

### Task 3.1: Implement the checks
**Done when:** no check reports TODO; each has at least one passing and one failing test.

<details><summary>Hint 1 (has_alert_rule)</summary>Rules don't name services in a field. The service appears in the query text, sometimes inside a regex (<code>service=~"a|b|c"</code>). How robust does your matching need to be?</details>
<details><summary>Hint 1 (runbook_fresh)</summary>The catalog's <code>runbook_updated</code> may be empty, or a date. What should each produce?</details>
<details><summary>Hint 1 (has_synthetic_probe)</summary>Once Prometheus scrapes the blackbox exporter, probe results appear as metrics. What label identifies the target?</details>

### Task 3.2: Synthetic probes for tier 1
**Goal:** Prometheus scrapes blackbox probes for tier-1 services, with an alert on failure and on slowness.
**Done when:** project 12's `slow-postgres` scenario now fires an alert.

<details><summary>Hint 2</summary>The standard pattern is one scrape job with <code>relabel_configs</code> that turns each target into a <code>?target=</code> parameter and points the scrape at the exporter.</details>
<details><summary>Hint 3</summary>https://github.com/prometheus/blackbox_exporter#prometheus-configuration</details>

### Task 3.3: Gap backlog
**Done when:** `docs/gap-backlog.md` lists every FAIL, scored by your ADR-0004 formula, with owners.

### Task 3.4: Close gaps
**Done when:** at least 3 gaps closed in the landscape (new rule, probe, runbook…), and the scanner output shows FAIL → PASS.

---

## Phase 4: Verify
**Done when:** your scanner's output matches your Phase 1 hand inventory (plus anything it found that you missed).

## Phase 5: Break
**Goal:** all experiments in `docs/break-it.md`, each with a postmortem.

## Phase 6: Decide again, then improve
- [ ] ADR-0003 to ADR-0005 accepted.
- [ ] The scanner's exit code and where it runs match ADR-0003.

## Phase 7: Document
- [ ] Interview story with numbers (gaps found, closed, by whom).
- [ ] You can answer: "What's your minimum monitoring standard?", "How do you get another team to add monitoring?", "White-box or black-box?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| Scanner can't reach Prometheus | Is the landscape up? Is `PROMETHEUS_URL` right? | `curl localhost:9090/-/ready` |
| Blackbox compose fails: network not found | Is the landscape running (it creates `landscape_default`)? | `docker network ls` |
| Probe always succeeds | What does the probed endpoint actually check? | Experiment 2 |
| Rule matching gives false positives | Does a service name appear inside another's (e.g. `auth` in `oauth`)? | Your matching logic + tests |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
