# Build plan: Project 10, Linux performance and tail latency

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how you'll know it's done.
Open hints one level at a time, after a real attempt (20–30 min): **Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Rough time:** 15–25 hours.

---

## Phase 0: Setup

### Task 0.1: A lab host you trust
**Goal:** a Linux host chosen per ADR-0001, with the tools installed.
**Done when:** `sockperf`, `stress-ng`, `perf` and `bpftrace` all run, and `capture-baseline.sh` writes a full `system.txt`.

<details><summary>Hint 1</summary>On a cloud VM, some sections of <code>system.txt</code> will say "not available". Note which, and what that means you can't tune.</details>
<details><summary>Hint 2</summary><code>perf</code> needs the tools package matching your <em>running</em> kernel, and may need <code>kernel.perf_event_paranoid</code> lowered.</details>

### Task 0.2: Read your machine
**Goal:** a diagram of your host's topology: sockets, NUMA nodes, cores, hyperthread siblings, and which cores handle IRQs.
**Done when:** you can say which two logical CPUs share a physical core.

<details><summary>Hint 2</summary><code>lscpu -e</code>, <code>numactl --hardware</code>, <code>lstopo</code> (hwloc).</details>

---

## Phase 1: Measure the "before"

### Task 1.1: An honest baseline
**Goal:** baseline percentiles with enough samples to trust p99.9, repeated ≥3 times.
**Done when:** row 0 of `tuning-log.md` is filled in, with the spread between runs noted.

<details><summary>Hint 1</summary>Look at "Total N observations" in <code>summary.txt</code>. How many observations sit beyond p99.9?</details>
<details><summary>Hint 2</summary><code>sockperf under-load</code> only measures a sample of replies. Look up its <code>--reply-every</code> option, and longer durations.</details>

---

## Phase 2: Decide

### Task 2.1: ADR-0001
**Done when:** it states your noise floor (the run-to-run spread) and the minimum change you'll treat as real.

---

## Phase 3: Build (measure → change one thing → measure)

### Task 3.1: Attribute the noise
**Goal:** run every noise mode and record which percentile each one hurts.
**Done when:** a table maps each noise source to its effect.

### Task 3.2: Apply isolation
> **Depends on your ADR-0002:** affinity/cpusets need no reboot. Kernel isolation needs boot parameters, so think about how you'll undo it if the host misbehaves.

**Goal:** the chosen isolation in place, re-measured under the same noise.
**Done when:** the tuning log shows before/after under identical noise.

<details><summary>Hint 1</summary>Isolating a core doesn't stop interrupts being delivered to it. What else do you need to move?</details>
<details><summary>Hint 3</summary>https://docs.kernel.org/admin-guide/kernel-parameters.html (search isolcpus, nohz_full); https://docs.kernel.org/core-api/irq/irq-affinity.html</details>

### Task 3.3: Tune the knobs you chose (ADR-0003)
**Goal:** each knob applied *alone*, measured, kept or reverted.
**Done when:** every knob has a row and a keep/revert reason.

<details><summary>Hint 2</summary>Power states: <code>cpupower</code>, <code>/sys/devices/system/cpu/cpu*/cpuidle</code>. THP: <code>/sys/kernel/mm/transparent_hugepage</code>. Or compare against a <code>tuned</code> profile.</details>

### Task 3.4: Explain one spike with evidence
**Goal:** a flame graph or trace that shows what caused a measured spike.
**Done when:** the evidence is committed, with a paragraph explaining it.

<details><summary>Hint 1</summary>Spikes are rare. Capture during a noisy run, not a quiet one.</details>
<details><summary>Hint 2</summary>Run-queue latency (how long a runnable task waited for a CPU) is a classic bpftrace one-liner.</details>
<details><summary>Hint 3</summary>https://www.brendangregg.com/FlameGraphs/cpuflamegraphs.html; https://github.com/bpftrace/bpftrace/tree/master/tools (runqlat)</details>

---

## Phase 4: Verify
**Done when:** every success criterion has a results folder or a tuning-log row as evidence.

## Phase 5: Break
**Goal:** all experiments in `docs/break-it.md`, each with a postmortem.

<details><summary>Exp 4: power states</summary>Think about what a CPU does when it's idle between requests, and how long it takes to wake up.</details>
<details><summary>Exp 5: container tax</summary>CPU limits are enforced in time slices (CFS quota). What happens to a request that arrives when the quota is used up?</details>

## Phase 6: Decide again, then improve
- [ ] ADR-0002 to ADR-0004 accepted, citing tuning-log rows.
- [ ] The final tuning written as a list of settings with reasons. That list is project 11's input.

## Phase 7: Document
- [ ] Interview story with numbers.
- [ ] You can answer: "What's coordinated omission?", "Why does a hyperthread sibling matter?", "When did you stop tuning and why?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| Results vary wildly between identical runs | Is something else running? Is the host shared (cloud)? | `top`/`pidstat` during runs; your noise floor |
| `perf` permission denied | What does `perf_event_paranoid` allow? | `/proc/sys/kernel/perf_event_paranoid` |
| No change after pinning | Did the pin apply? Are IRQs or kernel threads still on that core? | `taskset -p <pid>`; `/proc/interrupts` |
| Can't change governor / C-states | Does the VM expose them? | `system.txt` "not available" sections |
| Kernel isolation didn't apply | Did the boot parameters actually take effect? | `/proc/cmdline` after reboot |
| p99.9 equals max | Do you have enough samples? | "Total observations" in the summary |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
