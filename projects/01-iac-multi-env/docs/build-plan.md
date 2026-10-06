# Build plan: Project 01, multi-environment IaC with drift detection

This is a **guide for when you're stuck**, not a walkthrough. Each task tells you *what* to achieve
and how to know you're done. It doesn't tell you *how*. That part is yours.

**How to use the hints:** each task has hidden hints in three levels. Open only what you need.
- **Hint 1, a nudge:** a question or where to look.
- **Hint 2, the concept:** the name of the feature, command or idea you need.
- **Hint 3, the docs:** a link to official docs. Still not the answer.

Try for 20–30 minutes before opening a hint, then one level at a time. Note in your journal which hints
you needed. That's honest evidence of what you learned.

**Decisions:** the tasks work whichever option you pick in your ADRs. Where a choice changes the work,
a **"Depends on your ADR"** note tells you what to think about. It doesn't tell you what to type.

**Rough time:** 15–25 hours. **AWS cost** while staging exists: roughly $2–3/day. Destroy it when you stop.

---

## Phase 0: Setup

### Task 0.1: Tools installed
**Goal:** Terraform (a version that supports S3-native state locking), the AWS CLI and Git, all working.
**Done when:** each tool prints a version, and you know which Terraform version you need and *why*.

<details><summary>Hint 1</summary>Look at <code>required_version</code> in the starter and the <code>use_lockfile</code> line in <code>backend.tf</code>.</details>
<details><summary>Hint 2</summary>S3 lockfiles arrived in a specific Terraform minor release. Check the S3 backend docs for the version.</details>
<details><summary>Hint 3</summary>https://developer.hashicorp.com/terraform/language/backend/s3</details>

### Task 0.2: A safe AWS account
**Goal:** you work as a non-root identity with MFA, and you'll get an email before you overspend.
**Done when:** the CLI confirms you're *not* root, and a budget alert exists.

<details><summary>Hint 1</summary>Which AWS CLI command tells you "who am I"?</details>
<details><summary>Hint 2</summary>IAM Identity Center (SSO) is the recommended way to get a non-root admin. AWS Budgets handles alerts.</details>
<details><summary>Hint 3</summary>https://docs.aws.amazon.com/singlesignon/latest/userguide/getting-started.html, plus project 07's <code>terraform/budgets</code> as an example.</details>

### Task 0.3: Your own repo
**Goal:** this project lives in its own GitHub repo.
**Done when:** it's pushed and you can open a PR against it.

<details><summary>Hint 1</summary>The roadmap repo has a script for this in <code>scripts/</code>.</details>

---

## Phase 1: Understand the problem

### Task 1.1: Read before you touch
**Goal:** understand what every file creates and how the pieces connect.
**Done when:** you can explain, without notes, what each module creates, why the DB is in private subnets, and what the state bucket is for.

<details><summary>Hint 1</summary>Start from <code>envs/staging/main.tf</code> and follow each <code>module</code> block to its source.</details>
<details><summary>Hint 2</summary>Search for every <code>DECISION</code> comment. Each one is a choice you'll have to defend.</details>

### Task 1.2: Your version of the problem
**Goal:** rewrite "The problem" in the README with **your** constraints (team size, budget, risk).
**Done when:** someone who hasn't read this repo understands why the project exists.

### Task 1.3: Draw it
**Goal:** a diagram of the target architecture, including where CI and the state bucket fit.
**Done when:** the diagram is in `docs/` and linked from the README.

<details><summary>Hint 1</summary>Draw the network first (VPC, subnets per AZ, routes), then what lives inside it, then what sits outside it (state, CI).</details>

---

## Phase 2: Decide (before writing more code)

### Task 2.1: ADR-0001 (state layout) and ADR-0002 (environment separation)
**Goal:** both ADRs say `Accepted`, with your reasoning.
**Done when:** you answered every "Questions to answer before deciding" in writing, and someone else could disagree with your reasoning (not just your conclusion).

<details><summary>Hint 1</summary>Picking the starter default is allowed. The reasoning is what's graded, not originality.</details>
<details><summary>Hint 2</summary>For each option, imagine the worst mistake a tired person could make with it. Which option makes that mistake hardest?</details>

### Task 2.2: Make the code match your decision
**Goal:** the repo layout reflects your ADRs.
**Done when:** `terraform init` and `terraform validate` pass in every root module you have.

> **Depends on your ADR:**
> - Splitting state by component? Then you need a way for one state to read another's outputs, and an order to apply them in.
> - Using workspaces? Then per-environment values need a new home, and you need a way to *see* which workspace you're in.
> - Using Terragrunt? Then work out what it generates for you, and pin its version.

<details><summary>Hint 1 (split state)</summary>How does the database module learn the VPC ID if the network lives in a different state file?</details>
<details><summary>Hint 2 (split state)</summary>Look up the <code>terraform_remote_state</code> data source, and its alternatives (SSM parameters, data lookups by tag).</details>
<details><summary>Hint 1 (workspaces)</summary>What does <code>terraform.workspace</code> return, and how could you use it as a key?</details>
<details><summary>Hint 3 (Terragrunt)</summary>https://terragrunt.gruntwork.io/docs/features/state-backend/</details>

---

## Phase 3: Build

### Task 3.1: The state bucket exists
**Goal:** a versioned, encrypted, private S3 bucket for remote state, created from `bootstrap/`.
**Done when:** the bucket exists, and you've decided (and written down) what happens to bootstrap's *own* state file.

<details><summary>Hint 1</summary>Bucket names are global. Yours needs to be unique.</details>
<details><summary>Hint 2</summary>Bootstrap uses local state on purpose. You can keep that file somewhere safe, or migrate it into the bucket afterwards. Look up <code>-migrate-state</code>.</details>

### Task 3.2: Environments use the remote backend
**Goal:** `envs/*` store state in your bucket under separate keys.
**Done when:** after `init`, you can see the state object in the S3 console.

<details><summary>Hint 1</summary>Backend blocks can't use variables. So how do you avoid hard-coding the bucket name in every file?</details>
<details><summary>Hint 2</summary>Look up "partial backend configuration" and <code>-backend-config</code>.</details>

### Task 3.3: Staging is running, built only from code
**Goal:** staging applied from a saved plan.
**Done when:** the outputs show a VPC and a DB endpoint, and you read **every line** of the plan before applying.

<details><summary>Hint 1</summary>Why apply a saved plan file instead of running <code>apply</code> directly? What could change between the two?</details>
<details><summary>Hint 2</summary>RDS creation takes several minutes. That's normal, not a hang.</details>

### Task 3.4: Prod proven without paying for it
**Goal:** prod's configuration is shown to be valid.
**Done when:** `plan` succeeds for prod, and the README says whether you applied prod, and why or why not.

<details><summary>Hint 1</summary>Compare the prod and staging tfvars. Which settings make prod cost more?</details>

### Task 3.5: Plans appear on pull requests
**Goal:** opening a PR posts a plan for each environment, using short-lived credentials.
**Done when:** a PR shows plan comments, and there are **no** AWS keys in GitHub secrets.

<details><summary>Hint 1</summary>The workflow expects a repository *variable*. Find its name in <code>terraform-plan.yml</code>.</details>
<details><summary>Hint 2</summary>GitHub OIDC federation lets Actions assume an AWS role. Project 05 has Terraform for exactly this, so you can do that part now.</details>
<details><summary>Hint 3</summary>https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services</details>

> **Depends on your ADR:** if you use workspaces or Terragrunt, the plan job must select the right workspace or call the right tool. The matrix idea still works.

### Task 3.6: Static checks in CI
**Goal:** a linter and a security/misconfiguration scanner run on every PR.
**Done when:** they run in CI, and `docs/static-checks.md` lists what they flagged and what you decided about each finding.

<details><summary>Hint 1</summary>One tool finds Terraform mistakes and bad practice. Another finds insecure configuration. You want one of each.</details>
<details><summary>Hint 2</summary>Look at tflint, and at checkov or trivy (config scanning). All three have GitHub Actions.</details>
<details><summary>Hint 3</summary>Decide whether findings should fail the build or only report them. That's a mini-decision worth a sentence in the doc.</details>

### Task 3.7: Drift detection runs
**Goal:** the scheduled drift job runs green when nothing has drifted.
**Done when:** one manual run passes with no issue opened, and you can explain the three exit codes the script relies on.

<details><summary>Hint 1</summary>Read <code>scripts/drift-check.sh</code>. What does <code>-detailed-exitcode</code> change?</details>
<details><summary>Hint 2</summary>Scheduled workflows can also be triggered by hand. Look for the trigger that allows it.</details>

---

## Phase 4: Verify

**Goal:** every success criterion in the README has **evidence**: a link, screenshot, log or number.
**Done when:** each box in the README is ticked, with a link next to it.

<details><summary>Hint 1</summary>"It works" isn't evidence. A PR link, an issue opened by the drift job, or a timed rebuild is.</details>

---

## Phase 5: Break

**Goal:** run every experiment in `docs/break-it.md` and write a postmortem for each.
**Done when:** each experiment has a hypothesis written *before* the run, a result, and a postmortem in `docs/postmortems/`.

Per-experiment nudges (open only when stuck):
<details><summary>Exp 1: console drift</summary>After the job flags drift you have two choices: make reality match the code, or make the code match reality. Which is right depends on <em>why</em> the change was made.</details>
<details><summary>Exp 3: stuck lock / bad state</summary>The lock error message contains something you'll need. For a bad state file, remember what you turned on for the bucket in bootstrap.</details>
<details><summary>Exp 4: rename without destroy</summary>Terraform has a block that tells it "this resource moved, it isn't new". Search the language docs for it.</details>
<details><summary>Exp 5: rebuild from nothing</summary>Every step you had to remember instead of read is a README bug. Fix the README, not your memory.</details>

---

## Phase 6: Decide again, then improve

### Task 6.1: ADR-0003 (who can apply) and ADR-0004 (drift policy)
**Goal:** both accepted, citing your break-it results as evidence.
**Done when:** each ADR links at least one postmortem. If an experiment changed your mind about an earlier ADR, a **new** ADR supersedes it.

> **Depends on your ADR-0003:** CI apply needs a second, more powerful role, a trigger, and a human approval gate for prod. A tool like Atlantis needs hosting. Laptop-only needs a written convention, and an honest note about its weakness.

<details><summary>Hint 1 (CI apply)</summary>GitHub "environments" can require a reviewer before a job runs. How could you use that for prod?</details>
<details><summary>Hint 2 (CI apply)</summary>The <code>sub</code> claim in the OIDC token can name an environment. Use that to restrict which job can assume the apply role.</details>

### Task 6.2: Drift alerts reach a human
**Goal:** drift notifies you somewhere you'll actually see it.
**Done when:** you've received a real notification from a real drift.

---

## Phase 7: Document

**Goal:** the README tells the story: problem, decisions, what broke, what changed, what you'd do at scale.
**Done when:**
- [ ] The interview story at the bottom of the README is filled in.
- [ ] `docs/scale.md` is written in your words.
- [ ] You can answer these out loud: "Why not workspaces?", "What if two people apply at once?", "How do you recover a corrupted state?"

---

## Teardown

**Goal:** you're not paying for idle infrastructure.
**Done when:** staging (and prod, if applied) are destroyed. The state bucket stays, because it holds your history and costs cents.

<details><summary>Hint 1</summary>Prod destroy will fail. Read the error. The friction is intentional; work out which setting causes it.</details>

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| Bucket name rejected | Is the name unique across *all* of AWS? | S3 naming rules |
| `use_lockfile` not recognized | Which Terraform version am I running? | `terraform version` vs `required_version` |
| "Error acquiring the state lock" | Is another run actually active, or did one crash? | The error message (it has an ID) |
| "No valid credential sources" | Has my login session expired? Which profile am I using? | `aws sts get-caller-identity` |
| CI can't assume the role | Does the token's `sub` match the trust policy? Does the job have permission to request a token? | Workflow `permissions:`; IAM role trust policy; GitHub OIDC docs on `sub` formats |
| CI plan can't read state | What does the plan role allow on the bucket? | IAM policy simulator |
| Drift reported every night with no human change | Is something *other than* Terraform changing the resource? | The drift diff; the `lifecycle` meta-argument |
| Bill is higher than expected | Which resources bill by the hour even when idle? | Cost Explorer, grouped by service |

**Still stuck after hints and this table?** Write down: what you expected, what happened, and the exact error.
Writing it down solves half of all problems. Bring that write-up to whoever you ask, me included.
