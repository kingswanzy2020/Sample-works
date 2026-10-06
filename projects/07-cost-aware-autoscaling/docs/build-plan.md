# Build plan: Project 07, cost-aware autoscaling

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how
you'll know it's done, never *how*. Open hints one level at a time, only after a real attempt (20–30 min):
**Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Decisions:** tasks work with any option you choose. **"Depends on your ADR"** notes say what to think about, not what to type.

**Rough time:** 15–25 hours. **Cost:** local parts free. EKS + Karpenter costs real money, so budget first.

> **Note on local results:** kind nodes share your laptop's CPU. Absolute numbers will differ from the cloud,
> but *relative* comparisons (A vs B on the same machine) are still valid. Say so in your write-up.

---

## Phase 0: Setup

### Task 0.1: Cluster with metrics
**Goal:** kind cluster, app deployed, and `kubectl top pods` works.
**Done when:** `kubectl top pods -n scale` shows numbers, and `kubectl get hpa -n scale` shows a real percentage (not `<unknown>`).

<details><summary>Hint 1</summary>The HPA manifest has a comment about a component it needs, and a kind-specific tweak.</details>

---

## Phase 1: Measure the "before"

### Task 1.1: Capacity per pod
**Goal:** the request rate one pod handles before p95 latency degrades.
**Done when:** you have a table (rate → p95 → error rate) and have named the "knee" in `docs/cost-model.md`.

<details><summary>Hint 1</summary>Turn autoscaling off and run exactly one replica. Otherwise you're measuring the autoscaler, not the pod.</details>
<details><summary>Hint 2</summary>k6's end-of-run summary covers the whole run, not each stage. For per-step numbers, consider running one constant-rate test per level.</details>

### Task 1.2: Scenario A, static sizing for peak
**Goal:** the "before" cost: enough fixed replicas for the spike, no autoscaling.
**Done when:** scenario A's row in the cost model is filled in, and the spike test passes with it.

---

## Phase 2: Decide

### Task 2.1: ADR-0001 (scaling signal) and ADR-0002 (requests and limits)
**Done when:** both cite your capacity measurement.

---

## Phase 3: Build

### Task 3.1: Autoscaling on your chosen signal

> **Depends on your ADR-0001:**
> - **CPU (HPA):** the starter. Its target is a percentage of *requests*, so ADR-0002 matters.
> - **Request rate (KEDA):** needs Prometheus in the cluster scraping the app, and only one autoscaler per Deployment.
> - **Schedule:** KEDA has a cron trigger. How will you handle traffic that doesn't follow the schedule?
> - **Queue depth:** only fits if you add a queue-driven worker. Scope it honestly.

**Goal:** the spike test passes your thresholds with autoscaling on.
**Done when:** you have a graph of replicas vs load vs p95 over the spike, from `watch-scaling.sh` plus k6 output.

<details><summary>Hint 1 (KEDA)</summary>KEDA creates its own HPA behind the scenes. What happens if the starter HPA is still there?</details>
<details><summary>Hint 2 (KEDA)</summary>The Prometheus address in the ScaledObject must match the Service your Prometheus install created.</details>
<details><summary>Hint 3</summary>https://keda.sh/docs/latest/scalers/prometheus/</details>
<details><summary>Hint (graphing)</summary>The script writes CSV. Any spreadsheet or a few lines of Python can plot it.</details>

### Task 3.2: Right-size from data
**Goal:** requests set from observed usage, not guesses.
**Done when:** you've compared before/after requests and re-run the capacity and spike tests with the new values.

<details><summary>Hint 1</summary>A VPA in recommendation-only mode gives advice without restarting pods. It needs time and traffic before it says anything useful.</details>
<details><summary>Hint 3</summary>https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler</details>

### Task 3.3: Spot, or a simulation of it

> **Depends on your ADR-0003:** with no cloud, simulate interruptions by draining nodes mid-spike. With EKS, look at Karpenter's getting-started guide and AWS Fault Injection Service.

**Done when:** you've measured errors and recovery time during an interruption under load.

### Task 3.4: Know who spends what
**Goal:** cost broken down by owner, and an alert *before* overspend.
**Done when:** a budget with a forecast alert exists, and you can show cost (or reserved resources) per team label.

<details><summary>Hint 2</summary>OpenCost runs in-cluster with Prometheus. In AWS, cost allocation tags must be activated before they show up in billing.</details>

---

## Phase 4: Verify

**Goal:** `docs/cost-model.md` complete for every scenario you ran, with a decision paragraph.
**Done when:** the decision paragraph states a % saving **and** the accepted risk.

<details><summary>Hint 1</summary>Get node prices from the AWS pricing pages for one region and date, and note both. Show your formula so a reader can check it.</details>

---

## Phase 5: Break

**Goal:** every experiment in `docs/break-it.md`, each with a postmortem.

<details><summary>Exp 1: memory too low</summary>Check the pod's last state. "OOMKilled" and "slow" are different failures. Which one do users see?</details>
<details><summary>Exp 2: CPU throttling</summary>Look at p99, not the average. Throttling hides in the tail.</details>
<details><summary>Exp 3: flapping</summary>Count scaling events. What setting in the HPA <code>behavior</code> block exists to stop this?</details>
<details><summary>Exp 5: runaway scaling</summary>If a dependency is slow, does adding pods help? What protects the bill?</details>

---

## Phase 6: Decide again, then improve

### Task 6.1: ADR-0003 and ADR-0004 accepted, with measured numbers.

### Task 6.2: Idle environments cost nothing
**Goal:** non-prod scales down outside working hours.
**Done when:** you've calculated the monthly saving, and shown it scaling down and back up.

<details><summary>Hint 2</summary>KEDA's cron scaler, or a CronJob that scales Deployments. Which one fails more safely?</details>

---

## Phase 7: Document

**Done when:**
- [ ] The cost model has a before/after chart.
- [ ] The interview story is filled in.
- [ ] You can answer: "Why not CPU limits?", "Why is your min replicas X?", "Which workloads are never on spot?", "How do you find who's spending?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| HPA targets `<unknown>` | Is metrics-server running and able to reach the kubelets? Do pods set CPU requests? | `kubectl -n kube-system logs deploy/metrics-server`; `kubectl describe hpa` |
| HPA never scales | Is the load actually reaching the pods? Is the host CPU saturated first? | `kubectl top`; k6 output |
| Pods `Pending` during scale-up | Do the nodes have enough allocatable resources for the *requests*? | `kubectl describe pod` (events) |
| Can't reach `localhost:8080` | Was the cluster created with the port mapping? | `kind/cluster.yaml` |
| Replicas jump up and down | What's the scale-down stabilization window? | HPA `behavior` |
| VPA shows no recommendation | Has it had enough time and traffic? Is the recommender running? | `kubectl describe vpa` |
| KEDA and HPA fighting | How many autoscalers target this Deployment? | `kubectl get hpa,scaledobject -n scale` |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
