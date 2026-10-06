# Break-it experiments

Record every run with `scripts/watch-scaling.sh` so you have graphs, not memories.

### Experiment 1: Memory limit too low
- **Procedure:** Set `limits.memory: 64Mi`. Deploy and run `load/spike.js`.
- **Measure:** OOMKilled count (`kubectl get pods` → RESTARTS, `describe` → Last State). Errors during the spike. Does the HPA make it better or worse?
- **Result:**

### Experiment 2: CPU limits and throttling
- **Procedure:** Add `limits.cpu: 250m`. Run `load/find-capacity.js` against one pod with and without the limit.
- **Measure:** p99 latency; `container_cpu_cfs_throttled_periods_total` if you have Prometheus.
- **Result:**

### Experiment 3: Flapping
- **Procedure:** Set `scaleDown.stabilizationWindowSeconds: 0` and send bursty traffic (on 30s, off 30s).
- **Measure:** number of scale events per 10 minutes; errors on each scale-down.
- **Result:**

### Experiment 4: Spot interruption (cloud, or simulated)
- **Procedure (local simulation):** during the spike, `kubectl drain` the node with the most app pods.
  **Cloud:** use AWS Fault Injection Service to send a spot interruption.
- **Measure:** errors; time until capacity recovers; did the PDB hold?
- **Result:**

### Experiment 5: Runaway scaling
- **Procedure:** Build a version with `INJECT_LATENCY_MS=2000` (slow but not erroring). Watch request-rate or CPU scaling respond.
- **Measure:** does it scale to `maxReplicas`? Does more pods fix a slow dependency? What did it cost? Why does the ceiling matter?
- **Result:**
