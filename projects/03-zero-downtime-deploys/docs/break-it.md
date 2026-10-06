# Break-it experiments

Run every experiment under load (`load/during-deploy.js`) so you measure impact instead of guessing.

### Experiment 1: The breaking migration
- **Hypothesis:** A single `ALTER TABLE items RENAME COLUMN name TO title` plus a v2 deploy causes errors until every v1 pod is gone.
- **Procedure:** Add the rename as `app/migrations/002_rename.sql`, change v2 to use `title`, run the migrate Job, then roll out under load.
- **Measure:** failed requests, and for how long. Then redo it with `migrations-expand-contract/` and compare.
- **Result:**

### Experiment 2: No graceful shutdown
- **Hypothesis:** Without `preStop: sleep`, some requests fail during each pod termination because endpoint removal races with SIGTERM.
- **Procedure:** Remove `preStop`, set `terminationGracePeriodSeconds: 1`, deploy under load.
- **Measure:** failed requests per pod replaced.
- **Result:**

### Experiment 3: Liveness probe pointing at the database
- **Hypothesis:** If liveness uses `/readyz`, a 30s database outage restarts every pod, and recovery takes longer than the outage.
- **Procedure:** Change liveness to `/readyz`, then `kubectl -n zdd scale deploy/postgres --replicas=0` for 30s, then back to 1.
- **Measure:** restarts (`kubectl get pods`), time until 200s return. Compare with the starter config.
- **Result:**

### Experiment 4: Bad canary
- **Procedure:** Build v3 with `INJECT_ERROR_RATE=0.2` and roll it out as a canary.
- **Measure:** time to automatic abort; % of users affected; what happens if the error rate is 0.5% (below threshold)?
- **Result:**

### Experiment 5: Node drain during a deploy
- **Procedure:** Start a rollout, then `kubectl drain` a worker node.
- **Measure:** did the PDB hold? Any failed requests?
- **Result:**
