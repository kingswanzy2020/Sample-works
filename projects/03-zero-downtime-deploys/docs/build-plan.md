# Build plan: Project 03, zero-downtime deployments

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how
you'll know it's done, never *how*. Open hints one level at a time, only after a real attempt (20–30 min):
**Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Decisions:** tasks work with any option you choose. **"Depends on your ADR"** notes say what to think about, not what to type.

**Rough time:** 15–25 hours. **Cost:** free (local kind cluster). Needs ~4 GB RAM.

---

## Phase 0: Setup

### Task 0.1: Local cluster tools
**Goal:** Docker, kind, kubectl and k6 installed.
**Done when:** you can create and delete a kind cluster, and k6 can run a trivial script.

### Task 0.2: The app runs in the cluster
**Goal:** the starter deploys (rolling variant), migrations have run, and `localhost:8080/items` answers.
**Done when:** `curl localhost:8080/version` returns `v1`, and `/items` returns a JSON list.

<details><summary>Hint 1</summary>Read the Makefile targets in order. What has to exist before the app pod can become ready?</details>
<details><summary>Hint 2</summary>kind nodes can't see images on your laptop unless you load them in. Port mappings are fixed when the cluster is created.</details>

---

## Phase 1: Measure the "before"

### Task 1.1: Make it naive, then measure
**Goal:** a deliberately bad config: no `preStop`, a looser `maxUnavailable`, and both probes on the liveness endpoint. Then deploy v1 → v2 under load.
**Done when:** the README results table has a "Rolling (naive)" row with failed requests and p99, averaged over **3 runs**.

<details><summary>Hint 1</summary>To deploy "again", the cluster must be on the other version first. How do you switch back without the script?</details>
<details><summary>Hint 2</summary>The load script reports failures and p99 in its summary. <code>deploy-under-load.sh</code> prints both.</details>

### Task 1.2: Understand *why* requests fail
**Goal:** a written timeline of what happens when a pod is told to stop.
**Done when:** you can draw: SIGTERM → endpoints updated → kube-proxy updates → process exits, and say where the race is.

<details><summary>Hint 1</summary>Watch the Service's endpoints change during a rollout, in a second terminal.</details>
<details><summary>Hint 2</summary>Look up <code>EndpointSlice</code>, and the pod termination lifecycle.</details>
<details><summary>Hint 3</summary>https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination</details>

---

## Phase 2: Decide

### Task 2.1: ADR-0001 (strategy) and ADR-0003 (what "healthy" means)
**Goal:** both accepted. ADR-0003 must contain your exact, measurable definition of "zero downtime".
**Done when:** your definition matches the thresholds in the load script, or you've changed the thresholds to match it.

---

## Phase 3: Build

### Task 3.1: Rolling update with zero failed requests
**Goal:** the tuned rolling config gets 0 failed requests over 3 runs.
**Done when:** the "Rolling (tuned)" row shows 0 failures, and you can justify every number in the Deployment spec.

<details><summary>Hint 1</summary>If you still see failures, which of these is wrong: traffic sent to a pod that's not ready, or to a pod that's leaving?</details>
<details><summary>Hint 2</summary>The <code>preStop</code> sleep, <code>terminationGracePeriodSeconds</code> and the app's own graceful-shutdown timeout must fit inside each other.</details>

### Task 3.2: Your chosen strategy beyond rolling

> **Depends on your ADR-0001.** Build the strategy you chose. (If you chose rolling, still build *one* other one so you have evidence for the ADR.)

**Blue/green. Goal:** switch v1 → v2 by flipping the Service, under load, with zero failures, and roll back the same way.
<details><summary>Hint 1</summary>The rolling and blue-green manifests both define a Service called <code>app</code>. What do you need to remove before applying the other?</details>
<details><summary>Hint 2</summary>Careful: deleting a kustomization that includes <code>base</code> deletes the namespace too.</details>

**Canary. Goal:** v2 gets ~25% of traffic, then you promote or abort, under load.
<details><summary>Hint 1</summary>Without Prometheus (project 04), the analysis step can't run. What can replace it for now?</details>
<details><summary>Hint 2</summary>Argo Rollouts has a kubectl plugin for watching, promoting and aborting.</details>
<details><summary>Hint 3</summary>https://argo-rollouts.readthedocs.io/en/stable/getting-started/</details>
<details><summary>Hint (load script)</summary><code>deploy-under-load.sh</code> drives a Deployment. A Rollout is a different kind. Adapting the script is part of the task.</details>

**Done when:** the results table has a row for the strategy, including rollback time and extra capacity used.

### Task 3.3: Rename a column with zero downtime
**Goal:** `items.name` → `items.title` across several deploys, under load, with zero failures.
**Done when:** the old column is gone, no request failed at any step, and you can say which app version was running at each step.

<details><summary>Hint 1</summary>Read <code>migrations-expand-contract/README.md</code>. The table tells you <em>what</em> each step must achieve, not how to write the app code.</details>
<details><summary>Hint 2</summary>Migrations ship inside the image, and the migration Job references an image tag. Jobs can't be edited once created.</details>
<details><summary>Hint 3</summary>Each step is: build an image (code + migration), run the migration, roll out, verify. Then the next step.</details>

---

## Phase 4: Verify

**Goal:** the results table is complete (3 runs per row), and every success criterion has evidence.
**Done when:** you can show a k6 summary with 0 failed requests for your chosen strategy.

---

## Phase 5: Break

**Goal:** every experiment in `docs/break-it.md`, each with a postmortem.

<details><summary>Exp 1: breaking migration</summary>Measure how long the errors last. What decides that duration?</details>
<details><summary>Exp 3: liveness on the DB</summary>Count restarts during and after the DB outage. Which probe should notice a dead dependency, and what should it do?</details>
<details><summary>Exp 4: bad canary</summary>Try an error rate just under your threshold too. What does that tell you about thresholds and traffic volume?</details>
<details><summary>Exp 5: drain during deploy</summary>A PodDisruptionBudget limits voluntary disruptions. Is a rollout one?</details>

---

## Phase 6: Decide again, then improve

### Task 6.1: ADR-0002 (migrations) and ADR-0004 (rollback)
**Done when:** both cite break-it results. If a migration can't be rolled back safely, ADR-0004 says what that means for automatic rollback.

### Task 6.2: Metric-based analysis
**Goal:** the canary is analysed against real error-rate metrics.
**Done when:** a bad canary aborts automatically, and you measured how long it took.

<details><summary>Hint 1</summary>You need Prometheus scraping the app inside the cluster. Project 04 does it with Compose; here, look at the kube-prometheus-stack Helm chart.</details>
<details><summary>Hint 2</summary>The analysis template's Prometheus address must match the Service your install actually created. List the Services and check.</details>

### Task 6.3: Connect to project 02
**Goal:** a merge to main can trigger this deployment.
**Done when:** you've written down how the cluster would get the new digest. If you don't automate it, say why.

---

## Phase 7: Document

**Done when:**
- [ ] Results table complete; termination timeline diagram in `docs/`.
- [ ] The interview story is filled in.
- [ ] You can answer: "Why preStop sleep?", "Why not run migrations in an init container?", "When is canary pointless?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| `ErrImageNeverPull` / `ImagePullBackOff` | Is the image inside the kind nodes? | `kind load docker-image`; `kubectl describe pod` |
| `localhost:8080` refuses connections | Does the cluster have the port mapping? (Only set at creation.) | `kind/cluster.yaml`; `docker ps` |
| Pods never become ready | What does the readiness endpoint check? Is that dependency up? | `kubectl describe pod`, `kubectl logs` |
| `/items` fails, `/healthz` works | Did migrations run? | `kubectl -n zdd get jobs`, job logs |
| Job "field is immutable" | Can a Job be changed after it's created? | Kubernetes Job docs |
| Still a few failures after tuning | Which side of the termination race is losing? | Watch endpoints during a rollout |
| `kubectl drain` hangs | Is a PDB doing its job? | `kubectl get pdb` |
| Rollout stuck at a step | Is it waiting for a pause, or for analysis? | `kubectl argo rollouts get rollout ...` |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
