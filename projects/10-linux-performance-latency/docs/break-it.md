# Break-it experiments

Run each with `scripts/measure.sh` while `scripts/noise.sh` runs in another terminal. Repeat ≥3 times.
Then try the same noise with your isolation in place. The difference is the evidence for ADR-0002/0003.

### Experiment 1: CPU neighbour on the same core
- **Hypothesis:** noise on the server's core raises p99 by ___×; noise on a different core barely matters.
- **Procedure:** pin server, client and noise to chosen cores (`SERVER_CPUS`, `CLIENT_CPUS`, `NOISE_CPUS`). Try same core, sibling hyperthread, and a different physical core.
- **Measure:** p99, p99.9, max per placement.
- **Result:**

### Experiment 2: Shared cache and memory bandwidth
- **Procedure:** `MODE=cache` and `MODE=memory` on *different* cores from the server.
- **Measure:** does isolation by core protect you here? Why not?
- **Result:**

### Experiment 3: Interrupts on your core
- **Procedure:** find which core handles the network/disk IRQs (`capture-baseline.sh`), run `MODE=io`, and compare server on that core vs another.
- **Measure:** latency difference; then move IRQs (or stop irqbalance) and re-measure.
- **Result:**

### Experiment 4: Power-saving states
- **Procedure:** compare a low request rate vs high (`MPS=500` vs `MPS=50000`). Then change the frequency governor or limit deep C-states, if your host allows it.
- **Measure:** why can *lower* load produce *higher* latency? What did the change cost in power?
- **Result:**

### Experiment 5: The container tax
- **Procedure:** run the sockperf server in a container: (a) with a CPU limit, (b) with `--cpuset-cpus`, (c) on the host.
- **Measure:** p99.9 and max for each. What does a CPU limit do to the tail? (Connects to project 07's throttling experiment.)
- **Result:**

### Experiment 6: Find a spike's cause from evidence
- **Procedure:** while spikes happen, capture with `perf sched`, `perf record -g`, or a bpftrace one-liner (e.g. run-queue latency).
- **Measure:** can you show *what* was running on the core when the spike happened?
- **Result:**
