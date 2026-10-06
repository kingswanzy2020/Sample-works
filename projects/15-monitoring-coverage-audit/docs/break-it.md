# Break-it experiments

### Experiment 1: Up but wrong
- **Procedure:** inject `latency_ms: 800` on price-feed (no errors).
- **Measure:** which signal noticed: white-box alerts, black-box probes, nothing? How long did it take?
- **Result:**

### Experiment 2: The probe that lies
- **Procedure:** probe an endpoint that always returns 200 (e.g. a health endpoint that checks nothing) while the real path fails.
- **Measure:** what did the probe report? What makes a probe meaningful?
- **Result:**

### Experiment 3: Dead exporter
- **Procedure:** stop the blackbox exporter (or the simulator).
- **Measure:** does the scanner report PASS, FAIL or an error? Does any alert fire? A check that can't run is not a pass.
- **Result:**

### Experiment 4: New service, no monitoring
- **Procedure:** add a new tier-1 service to the catalog with nothing else.
- **Measure:** would your ADR-0003 process have stopped it? How fast does the scanner flag it?
- **Result:**
