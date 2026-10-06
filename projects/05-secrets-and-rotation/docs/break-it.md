# Break-it experiments

### Experiment 1: Vault goes down
- **Hypothesis:** The app keeps working until the current credential expires (≤ 1 min after the last renewal), then `/readyz` fails.
- **Procedure:** Run `scripts/rotation-under-load.sh 600`, then `docker compose stop vault` and note the time. Restart it after 5 minutes.
  Note: dev mode is in-memory, so a restarted Vault has **lost all config and leases**. What does that teach you about production Vault storage?
- **Measure:** time until first failure; time to recover; what the agent logs say.
- **Result:**

### Experiment 2: Revoke a lease mid-flight (simulated compromise)
- **Procedure:** `docker compose exec -e VAULT_TOKEN=root vault vault lease revoke -prefix database/creds/app`
- **Measure:** does the app fail? For how long? How fast would you contain a real leaked credential this way vs a static password?
- **Result:**

### Experiment 3: Leak a secret into git
- **Procedure:**
  1. Commit a fake AWS key (`AKIA` + 16 chars) with pre-commit **disabled**. Push to a branch.
  2. Does `secret-scan.yml` catch it? Now remove it in a new commit. Is it still in history? Does the scan still flag it?
  3. Write the real-world response: rotate first, then clean history. Why that order?
- **Result:**

### Experiment 4: Over-broad OIDC trust
- **Procedure:** Temporarily set the plan role's `sub` condition to `repo:<you>/*`. From a *different* repo you own, assume it in a workflow.
- **Measure:** did it work? What's the impact if that other repo accepts outside PRs?
- **Result:**

### Experiment 5: Secret in an image layer
- **Procedure:** Add `ARG DB_PASSWORD` + `RUN echo $DB_PASSWORD > /tmp/x && rm /tmp/x` to a Dockerfile, build, then run `docker history --no-trunc` and inspect layers.
- **Measure:** can you recover the secret? What's the right way (`--mount=type=secret`)?
- **Result:**
