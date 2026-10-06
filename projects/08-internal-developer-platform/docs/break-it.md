# Break-it experiments

### Experiment 1: Breaking change to the reusable workflow
- **Procedure:** In the platform repo, make `service-ci.yml` require a new input, and push it to the `v1` tag (moving the tag).
  What happens to every service on its next push? Then do it properly: release `v2`, keep `v1` working, announce a deprecation date.
- **Measure:** number of services broken; time to notice.
- **Result:**

### Experiment 2: Enforce on day one
- **Procedure:** Switch all Kyverno policies to `Enforce` with project 03 and 07 workloads running. Trigger a rollout.
- **Measure:** what was blocked? What error does a developer see? Is it clear how to fix it?
- **Result:**

### Experiment 3: `kubectl edit` vs self-heal
- **Procedure:** During a "pretend incident", scale prod with `kubectl scale --replicas=8`. Watch Argo CD revert it.
- **Measure:** how long until it reverted? What's the right incident procedure in a GitOps world?
- **Result:**

### Experiment 4: Escape-hatch abuse
- **Procedure:** Generate a service, then delete its use of the reusable workflow and the probes. Run `scripts/scorecard.sh`.
- **Measure:** would anyone notice without the scorecard? How would you report this across 50 repos?
- **Result:**

### Experiment 5: The new-joiner test
- **Procedure:** Ask someone who has never seen the platform to ship a new endpoint to staging using only the docs.
- **Measure:** time, number of questions, where they got stuck. Each one becomes an issue.
- **Result:**
