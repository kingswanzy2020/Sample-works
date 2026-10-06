# Break-it experiments

Keep `load/steady.js` running during all of them.

### Experiment 1: Find the latency (the core exercise)
- **Hypothesis:** With logs only, finding the cause of a slow `/items` takes > 15 minutes. With traces, < 5.
- **Procedure:** Ask someone else to inject latency without telling you where (or script it randomly):
  ```bash
  curl -s -XPOST localhost:8474/proxies/postgres/toxics \
    -d '{"name":"slow-db","type":"latency","stream":"downstream","attributes":{"latency":300,"jitter":50}}'
  # remove: curl -XDELETE localhost:8474/proxies/postgres/toxics/slow-db
  ```
  Alternative: restart the app with `INJECT_LATENCY_MS=300` (in-app, not the DB). Can you tell the two apart from traces?
- **Measure:** time from the alert/dashboard signal to naming the cause. Steps taken.
- **Follow-up question:** 300ms of DB latency makes `/items` take roughly **2 seconds**, not 300ms. Use the trace to explain why.
  (Hint: count the round trips. The app opens a new connection per request.) What design change would you propose, and what would it cost?
- **Result:**

### Experiment 2: Cardinality explosion
- **Hypothesis:** Labelling metrics with the raw path (`/items/123`) multiplies series and slows Prometheus.
- **Procedure:** Temporarily change the middleware to label with `request.url.path`. Hit 10,000 unique paths with a loop.
  Watch `prometheus_tsdb_head_series` and query latency.
- **Measure:** series before/after; Prometheus memory.
- **Result:**

### Experiment 3: The silent failure
- **Hypothesis:** If the app stops being scraped (wrong port, network policy), the SLO alerts *don't* fire, because no data means no errors.
- **Procedure:** Change the scrape target port and reload Prometheus (`curl -XPOST localhost:9090/-/reload`).
- **Measure:** which alert fired, if any? (`TargetDown` exists for this reason. What if the whole job disappears? Look up `absent()`.)
- **Result:**

### Experiment 4: Alert fatigue
- **Procedure:** Add a naive `cpu > 80%` page and an `errors > 0` page. Run a day of load including `/work` spikes and some injected errors.
  Count pages from naive rules vs burn-rate rules, and how many of each were actionable.
- **Result:**

### Experiment 5: Kill the monitoring
- **Procedure:** `docker compose stop prometheus` for 10 minutes while injecting errors.
- **Measure:** who finds out? What would a dead-man's switch (always-firing `Watchdog` alert to an external service) add?
- **Result:**
