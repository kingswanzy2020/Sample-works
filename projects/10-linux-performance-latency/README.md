# Project 10: Linux performance and tail-latency tuning

> **Problem:** A latency-sensitive service (think: a quote engine) has a fine average but a p99.9 that
> spikes every few minutes. Nobody can say why, and "just add more CPU" hasn't helped.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

## Decisions this project proves you can make

1. **How to measure latency honestly:** which percentiles, open vs closed loop, how many samples, which environment.
2. **CPU isolation:** none, affinity, cgroup cpusets, or kernel isolation (`isolcpus`/`nohz_full`), and what each costs.
3. **Kernel and hardware tuning scope:** IRQ affinity, frequency/C-states, THP, swap, and power vs latency.
4. **Containers vs bare metal** for latency-critical workloads.
5. **When to stop tuning:** the point where the remaining jitter is cheaper to accept than to remove.

## Success criteria

- [ ] A reproducible baseline: p50/p99/p99.9/max, ≥3 runs, with the host configuration captured.
- [ ] Each noisy-neighbour mode attributed: you can say *which* resource causes *which* part of the tail.
- [ ] A tuned configuration that reduces p99.9 by a measured amount, **one change at a time**, in `docs/tuning-log.md`.
- [ ] At least one latency spike explained with `perf` or eBPF evidence (a flame graph or a trace), not a guess.
- [ ] The tuning written as code (project 11), so it's repeatable on a fleet.

## Prerequisites and cost

- **A Linux host you control,** ideally with ≥4 dedicated cores. This choice is ADR-0001.
  Docker Desktop on macOS/Windows hides the real kernel. A cloud VM shares hardware, so results are noisier but still meaningful for relative comparisons.
- Tools: `scripts/install-tools.sh` (sockperf, stress-ng, perf, bpftrace, numactl).
- Cost: free on your own Linux machine; a few dollars on a cloud instance (stop it when idle).

## Starter layout

```
scripts/install-tools.sh     # sockperf, stress-ng, perf, bpftrace, numactl, hwloc
scripts/capture-baseline.sh  # records CPU topology, NUMA, governors, C-states, THP, IRQs, kernel cmdline
scripts/measure.sh           # sockperf at a FIXED rate, optional CPU pinning, saves percentiles
scripts/noise.sh             # noisy neighbours: cpu | cache | memory | io | syscall
docs/tuning-log.md           # one change per row, with evidence
results/                     # every run's raw output (commit it)
```

The starter measures. It does **not** tune anything. Every tuning change is yours to choose, apply and justify.

## How this project connects

| Direction | Project | What flows |
|-----------|---------|------------|
| Feeds | [11 Ansible fleet](../11-ansible-fleet-config/) | The tuning you prove here becomes an Ansible role there, applied to a fleet with checks |
| Uses (optional) | [09 Kafka](../09-kafka-streaming-reliability/) | The consumer's end-to-end latency is a second, realistic workload to profile |
| Related, not repeated | [07 Autoscaling](../07-cost-aware-autoscaling/) | 07 looks at CPU limits from a cost and throughput angle in Kubernetes. Here you go down to the host: cores, interrupts, kernel |
| Feeds | [16 Reliability reporting](../16-reliability-reporting/) | Your latency percentiles and their definitions inform how latency SLIs are reported |

**Not in this project:** autoscaling and cost (07), metrics dashboards (04), and fleet rollout (11).

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-measurement-method.md) | Lab environment and measurement method | Proposed |
| [0002](docs/adr/0002-cpu-isolation.md) | CPU isolation strategy | Proposed |
| [0003](docs/adr/0003-kernel-tuning-scope.md) | Which kernel/hardware knobs, and the power tradeoff | Proposed |
| [0004](docs/adr/0004-containers-vs-bare-metal.md) | Containers vs bare metal for latency-critical services | Proposed |

## Interview story

> "p99.9 was ___ µs with spikes to ___. Using ___ I traced the spikes to ___. Isolating ___ and changing ___
> brought p99.9 to ___. I stopped at ___ because the next step would have cost ___. On a fleet, I'd ___."
