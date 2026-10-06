# Build plan: Project 08, internal developer platform ("paved road")

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how
you'll know it's done, never *how*. Open hints one level at a time, only after a real attempt (20–30 min):
**Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Decisions:** tasks work with any option you choose. **"Depends on your ADR"** notes say what to think about, not what to type.

**Rough time:** 20–35 hours. **Cost:** free (kind, public GitHub repos).
**Builds on:** 02 (CI), 03 (manifests), 05 (signing identity), 07 (requests and labels).

---

## Phase 0: Setup

### Task 0.1: Repos and cluster
**Goal:** decide your repo layout (platform repo, GitOps repo, service repos) and create them. Also a kind cluster.
**Done when:** the repos exist, and you've replaced every `REPLACE_ORG` / `REPLACE_REPO` placeholder you need.

<details><summary>Hint 1</summary><code>grep -rn REPLACE_ .</code> lists every placeholder.</details>
<details><summary>Hint 2</summary>A personal GitHub account works. Your username stands in for "org".</details>

---

## Phase 1: Measure the "before"

### Task 1.1: Create a service the hard way
**Goal:** create a brand-new service manually (code, Dockerfile, CI, manifests, deploy) and time it.
**Done when:** you've recorded the total time and a list of every step and decision you had to make. That list is your platform's backlog.

---

## Phase 2: Decide

### Task 2.1: ADR-0001 (abstraction level), ADR-0002 (GitOps vs push), ADR-0005 (portal)
**Done when:** all three are accepted, and each refers to your Phase 1 list.

---

## Phase 3: Build

### Task 3.1: The golden CI pipeline is shared and versioned
**Goal:** `service-ci.yml` lives in your platform repo, released as a version that services call.
**Done when:** a service repo calls it by version tag, and CI passes.

<details><summary>Hint 1</summary>Reusable workflows are referenced as <code>owner/repo/.github/workflows/file.yml@ref</code>. What should the ref be, and what does moving it do to callers?</details>
<details><summary>Hint 2</summary>If the platform repo is private, other repos need explicit permission to use its workflows (repo Settings → Actions).</details>
<details><summary>Hint 3</summary>https://docs.github.com/actions/sharing-automations/reusing-workflows</details>

### Task 3.2: Deploys happen from git

> **Depends on your ADR-0002:**
> - **GitOps (Argo CD / Flux):** install the controller, point it at your GitOps repo, and let folders define apps.
> - **CI push:** CI needs cluster credentials. Decide how they're scoped and stored (project 05), and how you'll detect drift without a controller.

**Goal:** `sample-service` runs in staging because of a commit, and rolling back is a commit too.
**Done when:** you've deployed and rolled back using only git operations.

<details><summary>Hint 1 (Argo CD)</summary>The ApplicationSet derives app names and namespaces from folder path segments. Check that your folder structure produces the names you expect.</details>
<details><summary>Hint 2 (Argo CD)</summary>The cluster must be able to pull both the GitOps repo and the image. Public is simplest; private needs credentials for each.</details>
<details><summary>Hint 3</summary>https://argo-cd.readthedocs.io/en/stable/getting_started/, https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Git/</details>

### Task 3.3: New service from the template

> **Depends on your ADR-0005:**
> - **Backstage:** scaffold an app, register `template.yaml` in its catalog config, and give it a GitHub integration token.
> - **No portal:** a script or CLI that copies the skeleton and fills in the values.
> - **Commercial portal:** follow the vendor's template import.

**Goal:** a new service is generated from `backstage/skeleton`, gets a repo, passes CI and appears in staging.
**Done when:** you've timed it end to end, and it scores 9/9 on `scripts/scorecard.sh`.

<details><summary>Hint 1</summary>The skeleton uses Backstage's template syntax <code>${{ values.x }}</code>, which looks exactly like GitHub Actions expressions. What happens if you add a GitHub expression to a skeleton file?</details>
<details><summary>Hint 2</summary>Backstage templating is Nunjucks. Look up how to make it leave text alone ("raw" blocks).</details>
<details><summary>Hint 3</summary>https://backstage.io/docs/features/software-templates/writing-templates</details>

### Task 3.4: Promotion is a pull request
**Goal:** after a successful build, a PR updates the image digest in the GitOps repo for staging. Prod gets a separate, reviewed PR.
**Done when:** a merge in a service repo results in a digest-bump PR, without you touching it.

<details><summary>Hint 1</summary>A workflow's default token can't push to a <em>different</em> repo. What can?</details>
<details><summary>Hint 2</summary>A GitHub App token or a fine-grained PAT, scoped to the GitOps repo only. <code>kustomize edit set image</code> updates a digest cleanly.</details>

### Task 3.5: Guardrails in Audit mode
**Goal:** policies installed in Audit, with violations visible.
**Done when:** you can list current violations across the cluster, and say which are real.

<details><summary>Hint 2</summary>Kyverno writes PolicyReports. They're Kubernetes resources you can <code>kubectl get</code>.</details>

---

## Phase 4: Verify

### Task 4.1: The new-joiner test
**Goal:** someone who hasn't seen the platform ships a service to staging using only your docs.
**Done when:** you have their time, and every question they asked logged as an issue.

---

## Phase 5: Break

**Goal:** every experiment in `docs/break-it.md`, each with a postmortem.

<details><summary>Exp 1: breaking the shared workflow</summary>How do real projects publish breaking changes? Think about major version tags and deprecation windows.</details>
<details><summary>Exp 2: Enforce on day one</summary>Before enforcing, check which namespaces the policies apply to. Should they apply to the platform's own system components?</details>
<details><summary>Exp 3: kubectl vs self-heal</summary>If self-heal reverts your incident hotfix, what should the incident procedure be?</details>

---

## Phase 6: Decide again, then improve

### Task 6.1: ADR-0003 (guardrails) and ADR-0004 (measuring) accepted.

### Task 6.2: Measure the platform
**Goal:** DORA-style numbers before and after.
**Done when:** you have lead time, deploy frequency, change failure rate and time to restore, with each method written down.

<details><summary>Hint 1</summary>With GitOps, every deploy is a commit to an environment path. Git history is already a deploy log.</details>
<details><summary>Hint 2</summary><code>git log</code> with a path filter and a date format gives you deploy times. Reverts are your failures. Postmortems give time to restore.</details>

### Task 6.3: Move policies to Enforce
**Goal:** at least one policy enforced, with a documented exception process.
**Done when:** a violating deploy is blocked with a clear message, and an approved exception works.

---

## Phase 7: Document

**Done when:**
- [ ] A one-page platform product brief (users, problem, success metrics, out of scope).
- [ ] The interview story is filled in with time-to-first-deploy before/after.
- [ ] You can answer: "How do teams escape the paved road?", "How do you ship a breaking change to the platform?", "How do you know it's worth it?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| ApplicationSet creates no apps | Do the directory globs match your real paths? | ApplicationSet controller logs; generator docs |
| Argo CD can't fetch the repo | Is it private? Has Argo CD got credentials? | Argo CD repository settings |
| `ImagePullBackOff` from GHCR | Is the package public, or is there a pull secret? | Package visibility; `kubectl describe pod` |
| "workflow was not found" | Does the ref exist? Is access to the platform repo's workflows allowed? | Tags; repo Actions settings |
| Template output has broken `${{ }}` | Did Nunjucks render something meant for GitHub? | Rendered file vs skeleton |
| Policies flag system pods | Which namespaces should be excluded? | Policy `exclude` / match blocks |
| Promotion PR job can't push | Which token is it using, and what can that token access? | Workflow token permissions |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
