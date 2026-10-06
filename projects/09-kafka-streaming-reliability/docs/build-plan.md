# Build plan: Project 09, reliable Kafka streaming

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how you'll know it's done.
Open hints one level at a time, after a real attempt (20–30 min): **Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Rough time:** 15–25 hours. **Cost:** free (local).

---

## Phase 0: Setup

### Task 0.1: Cluster and pipeline running
**Goal:** 3 brokers up, topic created, producer and consumer flowing.
**Done when:** `scripts/lag.sh` shows the group consuming every partition, with lag near zero.

<details><summary>Hint 1</summary>The producer and consumer are behind a Compose profile. Check how to start services in a profile.</details>

### Task 0.2: Understand the topic description
**Goal:** explain every column of `kafka-topics.sh --describe`.
**Done when:** you can say what Leader, Replicas and Isr mean, and what happens to Isr when a broker dies.

<details><summary>Hint 3</summary>https://kafka.apache.org/documentation/#replication</details>

---

## Phase 1: Measure the "before"

### Task 1.1: Build the verifier (the most important task)
**Goal:** a script that compares `data/produced.jsonl` with `data/consumed.jsonl`.
**Done when:** it reports produced, consumed, **lost** (acked but never consumed) and **duplicated** (consumed more than once), and you've tested it on a hand-made file with known gaps.

<details><summary>Hint 1</summary>Sequence numbers are unique. What data structure makes "seen twice" and "never seen" easy to find?</details>
<details><summary>Hint 2</summary>"Lost" must only count messages the broker <em>acknowledged</em>. Unacked messages were never promised.</details>
<details><summary>Hint 3</summary>Run the verifier only after the consumer has caught up (lag 0). Otherwise "lost" just means "not yet consumed".</details>

### Task 1.2: Baseline with weak settings
**Goal:** run experiment 1 with *weak* settings first (e.g. acks=1) and record the loss.
**Done when:** you have a non-zero loss number you can reproduce. That's your "before".

<details><summary>Hint 1</summary>Loss is easier to see with a higher produce rate and a hard kill of the leader of the busiest partitions.</details>

---

## Phase 2: Decide

### Task 2.1: ADR-0001 and ADR-0002
**Done when:** both are accepted, with produce p99 latency measured for at least two settings.

<details><summary>Hint 2</summary>Measure produce latency from the producer's side (time from <code>produce</code> to the delivery callback). The starter doesn't record it; adding it is part of the task.</details>

---

## Phase 3: Build

### Task 3.1: Zero loss under leader failure
**Goal:** your chosen settings survive experiment 1 with 0 lost acked messages.
**Done when:** the verifier shows 0 lost across 3 runs.

### Task 3.2: Duplicates handled
> **Depends on your ADR-0002:** at-least-once needs idempotent processing. At-most-once needs a written justification for accepting loss. Exactly-once needs transactions and a clear statement of what it does **not** cover.

**Done when:** a consumer crash produces no *effective* duplicates downstream (or the ADR justifies the alternative).

<details><summary>Hint 1</summary>What could a consumer remember per instrument so that replaying an old message has no effect?</details>

### Task 3.3: Lag and freshness are visible
**Goal:** lag and data age on a dashboard, with an alert tied to a freshness SLO.
**Done when:** a slow consumer triggers the alert before data is older than your SLO.

<details><summary>Hint 1</summary><code>kafka-exporter</code> exposes lag in <em>messages</em>. Your SLO is probably in <em>seconds</em>. How do you convert, or measure age directly?</details>
<details><summary>Hint 2</summary>The consumer already records end-to-end latency per message. Could it expose that as a metric?</details>
<details><summary>Hint 3</summary>Point project 04's Prometheus at <code>kafka-exporter:9308</code> (both stacks need to share a network, or use the host port).</details>

### Task 3.4: Capacity numbers
**Goal:** max throughput of one consumer, and of the group.
**Done when:** ADR-0003 cites both numbers.

---

## Phase 4: Verify
**Done when:** every success criterion has evidence (verifier output, a dashboard screenshot, the alert firing).

## Phase 5: Break
**Goal:** all experiments in `docs/break-it.md`, each with a postmortem.

<details><summary>Exp 2: two brokers down</summary>Read the producer's error carefully. It names the setting that protected you.</details>
<details><summary>Exp 5: full disk</summary>Docker can mount a size-limited tmpfs as a volume. Check the Compose docs for tmpfs options.</details>
<details><summary>Exp 6: poison message</summary>Look up the "dead letter queue" pattern.</details>

## Phase 6: Decide again, then improve
- [ ] ADR-0003 and ADR-0004 accepted, with evidence.
- [ ] A runbook for "consumer lag high", and one for "broker down". These feed the landscape's `runbooks/kafka.md` used in 14–17.

## Phase 7: Document
- [ ] Interview story with real numbers.
- [ ] You can answer: "What does acks=all actually guarantee?", "How do you get exactly-once?", "Why can't you add consumers forever?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| Producer can't connect | Are brokers up and reachable by their advertised name? | `docker compose ps`; broker logs |
| `NOT_ENOUGH_REPLICAS` | How many brokers are in sync vs `min.insync.replicas`? | Topic describe → Isr |
| Consumer gets nothing | Which offset does a new group start from? Is it subscribed to the right topic? | `auto.offset.reset`; `lag.sh` |
| Verifier says "lost" but lag isn't 0 | Has the consumer caught up yet? | `lag.sh` |
| Extra consumers idle | How many partitions are there? | Group describe |
| Exporter shows odd (negative) lag | Are offsets read at slightly different moments? | Compare with `lag.sh` |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
