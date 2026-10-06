# Break-it experiments

Before every experiment, clear `data/` so produced/consumed counts are clean. Your verifier from Task 3.1 measures the result.

### Experiment 1: Kill the leader under load
- **Hypothesis:** With RF=3, min ISR=2 and acks=all, killing a partition leader loses 0 acked messages. With acks=1 it loses ___.
- **Procedure:** find which broker leads the most partitions (`kafka-topics.sh --describe`) and stop it with `docker kill` (not `stop`: no graceful shutdown).
- **Measure:** lost / duplicated messages, produce errors, and how long until new leaders were elected.
- **Result:**

### Experiment 2: Lose two brokers
- **Hypothesis:** With min ISR=2, the producer gets errors instead of losing data.
- **Measure:** what does the producer log? What happens to the consumer? What happens when the brokers return?
- **Result:**

### Experiment 3: Crash the consumer mid-processing
- **Procedure:** run with each `COMMIT_MODE`, and `docker kill` the consumer every 20 seconds for 2 minutes.
- **Measure:** lost vs duplicated messages per mode. Does it match ADR-0002's prediction?
- **Result:**

### Experiment 4: Slow consumer and rebalance storm
- **Procedure:** set `PROCESS_MS=10` at 200 msg/s. Watch lag grow. Then scale consumers (`--scale consumer=N`) past the partition count.
- **Measure:** lag over time, time to catch up, and what the extra consumers did.
- **Result:**

### Experiment 5: Full disk
- **Procedure:** limit one broker's data volume (e.g. a small tmpfs) and keep producing.
- **Measure:** how does the broker fail? Do the others keep serving? What would have warned you earlier?
- **Result:**

### Experiment 6: Poison message
- **Procedure:** produce one message the consumer can't parse.
- **Measure:** does the consumer crash-loop on it forever? What's your strategy (skip, dead-letter topic, alert)?
- **Result:**
