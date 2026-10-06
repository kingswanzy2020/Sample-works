# Break-it experiments

### Experiment 1: Find the drift
- **Procedure:** run `scripts/seed-drift.sh` **without reading it**. Then find every change using only Ansible.
- **Measure:** how many changes did you find? Which ones would your baseline role have reverted, and which did it not even look at?
- **Result:**

### Experiment 2: Not idempotent
- **Procedure:** run `site.yml` twice. Anything "changed" on the second run is a bug.
- **Measure:** number of non-idempotent tasks; why each one changes every time.
- **Result:**

### Experiment 3: A bad change across the fleet
- **Procedure:** introduce a change that breaks SSH or a service on every host (on the lab only), and roll it out with your ADR-0003 strategy.
- **Measure:** how many servers were affected before it stopped? How did you recover the broken ones?
- **Result:**

### Experiment 4: Unreachable host mid-run
- **Procedure:** `docker compose stop kafka-02` while a run is in progress.
- **Measure:** what does Ansible do with the rest of the fleet? How do you find and fix the host it skipped later?
- **Result:**

### Experiment 5 (VMs): A kernel setting that hurts
- **Procedure:** on a VM, roll out a latency setting from project 10 that's wrong for that host type (e.g. isolating cores a small VM needs).
- **Measure:** how did you notice? Could a post-apply check have caught it?
- **Result:**
