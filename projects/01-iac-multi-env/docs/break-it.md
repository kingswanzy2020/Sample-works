# Break-it experiments

Run each one on **staging**. Before you start, write your hypothesis. Afterwards, write a
postmortem in [`postmortems/`](postmortems/) using `templates/postmortem-template.md`.

---

### Experiment 1: Console drift on a security group

- **Hypothesis:** If I widen the Postgres security group to `0.0.0.0/0` in the console, the nightly drift job opens an issue within 24h.
- **Blast radius:** Staging DB briefly reachable from the internet (it is still not publicly accessible, but note this in your write-up).
- **Procedure:**
  1. In the AWS console, add an inbound rule `0.0.0.0/0:5432` to `sample-staging-db`.
  2. Trigger `drift-detection` manually (`workflow_dispatch`).
  3. Then decide: revert with `apply`, or codify it? Record why.
- **Measure:** time from change to detection. Did the alert reach a human?
- **Result:**
- **Follow-up:** ADR-0004

### Experiment 2: Apply to the wrong environment

- **Hypothesis:** With directory-per-env, running `apply` in `envs/prod` by mistake is (prevented / possible) because ___.
- **Procedure:** Try to apply a staging-only change to prod with the credentials you normally use. What stopped you, if anything?
- **Measure:** number of guardrails hit.
- **Result:**
- **Follow-up:** ADR-0002, ADR-0003

### Experiment 3: Stuck lock and corrupted state

- **Hypothesis:** If an `apply` is killed mid-run, the lock stays and the next run fails until I ___.
- **Procedure:**
  1. Start `terraform apply` on staging, then `kill -9` it during resource creation.
  2. Try another `plan`. Read the error.
  3. Recover with `terraform force-unlock`. Explain why that is dangerous.
  4. Bonus: upload a truncated state file, then recover from an S3 object version.
- **Measure:** time to recover; did any resource become orphaned (exists in AWS, not in state)?
- **Result:**
- **Follow-up:** ADR-0001

### Experiment 4: Accidental destroy of the database

- **Hypothesis:** `deletion_protection` in prod blocks a destroy; in staging, the DB is gone and ___.
- **Procedure:** Rename the `aws_db_instance` resource in staging without a `moved {}` block and read the plan carefully. Then add the `moved {}` block and compare.
- **Measure:** did the plan say "destroy"? Would a reviewer have noticed in a 200-line plan?
- **Result:**
- **Follow-up:** ADR-0001 (does the DB deserve its own state?)

### Experiment 5: Rebuild staging from nothing

- **Hypothesis:** I can `destroy` then rebuild staging in under ___ minutes using only the README.
- **Procedure:** Destroy staging fully. Rebuild from the README only, without relying on memory.
- **Measure:** wall-clock time; every undocumented step you had to remember.
- **Result:**
