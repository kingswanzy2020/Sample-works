# Build plan: Project 04, observability and SLOs

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how
you'll know it's done, never *how*. Open hints one level at a time, only after a real attempt (20–30 min):
**Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Decisions:** tasks work with any option you choose. **"Depends on your ADR"** notes say what to think about, not what to type.

**Rough time:** 15–25 hours. **Cost:** free (Docker Compose, ~3 GB RAM).

---

## Phase 0: Setup

### Task 0.1: The stack is up
**Goal:** all services running. The app answers on `:8000`, Grafana on `:3000`, Prometheus on `:9090`.
**Done when:** Prometheus shows the app target as UP, and the Grafana dashboard loads (possibly with empty panels).

<details><summary>Hint 1</summary>Compose needs to find the shared app. Check <code>APP_DIR</code> in <code>docker-compose.yml</code>.</details>
<details><summary>Hint 2</summary>Panels are empty without traffic. There's a load script.</details>

### Task 0.2: Tour the three signals
**Goal:** find one request in all three: its metric, its trace and its log line.
**Done when:** you can go from a Grafana panel → a trace in Tempo → the logs around that time in Loki, and describe what each one told you that the others didn't.

<details><summary>Hint 1</summary>Grafana's Explore view lets you pick a data source and query it directly.</details>
<details><summary>Hint 2</summary>PromQL for Prometheus, LogQL for Loki, TraceQL or Search for Tempo.</details>

---

## Phase 1: Measure the "before"

### Task 1.1: Debug with logs only
**Goal:** have latency injected without knowing where (ask someone, or script a random choice), then find the cause using **only** `docker compose logs`.
**Done when:** you've recorded how long it took, and what you could and couldn't tell from logs.

<details><summary>Hint 1</summary>Toxiproxy has an HTTP API on port 8474. The app has its own latency env var too. A random script could pick one of the two.</details>

---

## Phase 2: Decide

### Task 2.1: ADR-0001, SLIs and SLOs (before looking at the graphs)
**Goal:** your SLO targets, chosen from user expectations, plus the error budget in minutes per 30 days.
**Done when:** the ADR states the targets, which endpoints count, and what happens when the budget runs out.

<details><summary>Hint 1</summary>Error budget = (1 − target) × the time window. Work it out for 99%, 99.5% and 99.9% over 30 days to feel the difference.</details>

### Task 2.2: Make the rules match your SLOs
**Goal:** `prometheus/rules/slo.yml` and the dashboard reflect *your* targets.
**Done when:** the rules validate, and Prometheus shows them as healthy.

<details><summary>Hint 1</summary>Search the rules for the numbers tied to the starter targets. There's one for the budget and one for the latency threshold.</details>
<details><summary>Hint 2</summary>A latency SLI built from histogram buckets can only use thresholds that exist as a bucket. Check the bucket list in the app's metrics code.</details>
<details><summary>Hint 3</summary><code>promtool check rules</code> validates rule files. It ships inside the Prometheus image.</details>

---

## Phase 3: Build

### Task 3.1: Alerts reach you
**Goal:** pages and tickets go to real destinations (Slack, email, a webhook you can see).
**Done when:** a test alert arrives at the destination for each severity.

<details><summary>Hint 1</summary>Alertmanager already routes by severity. The receivers are empty.</details>
<details><summary>Hint 3</summary>https://prometheus.io/docs/alerting/latest/configuration/#receiver-integration-settings</details>

### Task 3.2: Prove the fast-burn alert works
**Goal:** cause real user-facing errors and see `ErrorBudgetFastBurn` fire.
**Done when:** you've measured time from "errors start" to "alert received", and can explain that delay from the rule definition.

<details><summary>Hint 1</summary>What makes <code>/items</code> return 5xx? Think about what's between the app and the database.</details>
<details><summary>Hint 2</summary>The rule needs <em>two</em> windows above the threshold, plus a <code>for:</code> duration. Work out the minimum time on paper first.</details>

### Task 3.3: Logs and traces link to each other
**Goal:** click from a log line to its trace, and from a trace to its logs.
**Done when:** both directions work in Grafana.

<details><summary>Hint 1</summary>For logs → traces, the log line must contain the trace ID. Does it today?</details>
<details><summary>Hint 2</summary>OpenTelemetry's Python logging instrumentation can inject trace context into log records. Grafana's Loki data source has "derived fields" to turn an ID into a link.</details>
<details><summary>Hint 3</summary>Uvicorn configures its own loggers. If the trace ID doesn't appear in access logs, think about where else you could log it.</details>

> **Depends on your ADR-0003 (metrics pipeline):** if you move metrics to OTLP via a collector, metric *names* change (OpenTelemetry semantic conventions), so your SLO rules must be rewritten. Prometheus 3 can receive OTLP directly. Look up the feature flag.
>
> **Depends on your ADR-0004 (sampling):** head sampling is an env var change. Tail sampling needs an OpenTelemetry Collector (the contrib distribution) between app and Tempo.

---

## Phase 4: Verify

**Goal:** every success criterion has evidence.
**Done when:** you have the time-to-cause with traces (compare it with Phase 1), proof that a CPU spike doesn't page, and the cost estimate.

<details><summary>Hint 1</summary>The <code>/work</code> endpoint burns CPU. Which alerts look at CPU? (Should any?)</details>

---

## Phase 5: Break

**Goal:** every experiment in `docs/break-it.md`, each with a postmortem.

<details><summary>Exp 1: latency hunt</summary>Compare the span durations inside the trace. Where is the time actually spent? Then answer the follow-up question about why 300 ms became about 2 s.</details>
<details><summary>Exp 2: cardinality</summary>Prometheus exposes metrics about itself, including how many series it holds. Query them before and after.</details>
<details><summary>Exp 3: silent failure</summary>When there's no data, a ratio is not "0% errors". It's nothing at all. Which PromQL function alerts on missing data?</details>
<details><summary>Exp 5: kill the monitoring</summary>Who watches the watcher? Look up the "Watchdog" / dead man's switch pattern.</details>

---

## Phase 6: Decide again, then improve

### Task 6.1: ADR-0002 to ADR-0006 accepted, each citing evidence.

### Task 6.2: Runbooks
**Goal:** every paging alert links to a runbook.
**Done when:** each runbook says how to confirm the alert, likely causes, and first actions.

### Task 6.3: Take it to Kubernetes
**Goal:** the same SLOs and alerts running against the app in your project 03 cluster.
**Done when:** project 03's canary analysis uses these metrics.

<details><summary>Hint 2</summary>kube-prometheus-stack (Helm) plus a ServiceMonitor for the app. Rules can be loaded as PrometheusRule resources.</details>

---

## Phase 7: Document

**Done when:**
- [ ] The interview story is filled in with before/after time-to-cause.
- [ ] A screenshot of the trace that found the problem.
- [ ] You can answer: "Why burn-rate alerts?", "What's your error budget in minutes?", "Why not page on CPU?", "What does high cardinality cost?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| Grafana panels empty | Is there traffic? Is the time range right? Does the query work in Prometheus directly? | Prometheus UI → Graph |
| Target DOWN | Can Prometheus reach the app by its Compose service name and port? | Prometheus → Status → Targets |
| Recording rules return nothing | Division by zero with no traffic? | Run the load script; query each half of the ratio |
| No traces in Tempo | Is the app exporting to the right endpoint and protocol? | App env vars; Tempo logs |
| No app logs in Loki | Is Alloy running and able to read the Docker socket? Is there a delay? | Alloy logs; Loki label values |
| App image build fails at OpenTelemetry bootstrap | Is a package version incompatible? | Build output; pin versions |
| Alert never fires | Are *both* windows above threshold? Has `for:` elapsed? | Prometheus → Alerts (pending vs firing) |
| Ports already in use | Is another project's stack still running? | `docker ps` |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
