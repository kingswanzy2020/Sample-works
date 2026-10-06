# Build plan: Project 05, secrets management and rotation

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how
you'll know it's done, never *how*. Open hints one level at a time, only after a real attempt (20–30 min):
**Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Decisions:** tasks work with any option you choose. **"Depends on your ADR"** notes say what to think about, not what to type.

**Rough time:** 15–25 hours. **Cost:** local parts free. AWS parts cost cents (the OIDC role, secrets).

---

## Phase 0: Setup

### Task 0.1: Tools
**Goal:** Docker Compose, an AWS account (from project 01), gitleaks and pre-commit. Optional: the Vault CLI, sops and age.
**Done when:** each tool runs. You can also run Vault commands inside the Vault container instead of installing the CLI.

---

## Phase 1: Measure the "before"

### Task 1.1: Where does a static password end up?
**Goal:** run the app with a plain password in an env var, then find **every** place that password can be read.
**Done when:** a table in `docs/` lists each location and who could read it.

<details><summary>Hint 1</summary>Think beyond the <code>.env</code> file: container metadata, the process itself, shell history, CI logs, image layers.</details>
<details><summary>Hint 2</summary><code>docker inspect</code>; <code>/proc/&lt;pid&gt;/environ</code> inside the container; <code>docker history</code>.</details>

---

## Phase 2: Decide

### Task 2.1: ADR-0001 (where secrets live) and ADR-0002 (static vs dynamic)
**Goal:** both accepted.
**Done when:** ADR-0001 includes a walk-through of offboarding one engineer under your chosen option.

---

## Phase 3: Build

### Task 3.1: Rotation without downtime

> **Depends on your ADR-0001 / ADR-0002.** Build the path you chose:
> - **Vault dynamic credentials (starter):** run the stack and understand every step it performs.
> - **Cloud secrets manager:** the RDS-managed secret from project 01 has built-in rotation. Note that the database is in *private* subnets, so think about where your test client runs.
> - **SOPS in git:** rotation is manual. Research "alternating users" (two DB users) rotation and implement that.
> - **IAM database auth:** the app needs a fresh token per connection. That changes how `database_url()` works.

**Goal:** the app's DB credentials change while it serves traffic, with 0 failed requests.
**Done when:** `rotation-under-load.sh` (or your equivalent) shows a credential change **during** the run with 0 failures, and you can prove the credential actually changed.

<details><summary>Hint 1 (Vault)</summary>Watch the database roles in Postgres while the test runs. When does the username change, and when only the expiry?</details>
<details><summary>Hint 2 (Vault)</summary>Lease <em>renewal</em> and credential <em>rotation</em> are different things. Look at <code>default_ttl</code> vs <code>max_ttl</code>.</details>
<details><summary>Hint 3 (Vault)</summary>https://developer.hashicorp.com/vault/docs/secrets/databases/postgresql</details>
<details><summary>Hint 1 (alternating users)</summary>If two users are both valid, you can change the password of the one <em>not</em> in use. What tells the app which one to use?</details>

### Task 3.2: CI reaches AWS without stored keys
**Goal:** project 01/02 workflows use OIDC roles, and no long-lived AWS keys remain in GitHub.
**Done when:** a PR plan works, an apply works only from the protected `prod` environment, and repo secrets contain no AWS keys.

<details><summary>Hint 1</summary>Read the two trust policies in <code>terraform/github-oidc</code>. What differs between them, and why?</details>
<details><summary>Hint 2</summary>The <code>sub</code> claim has a different format for a PR, a branch push and an environment job.</details>
<details><summary>Hint 3</summary>https://docs.github.com/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect#example-subject-claims</details>

### Task 3.3: Secrets can't sneak into git
**Goal:** a secret is blocked at commit time, and caught in CI if commit-time checks were skipped.
**Done when:** you've seen both layers stop a fake secret, including one buried in an *old* commit.

<details><summary>Hint 1</summary>Pre-commit hooks only run if installed, and can be skipped. That's why CI exists as a backstop.</details>
<details><summary>Hint 2</summary>A scan of only the latest commit misses history. Check how deep the CI checkout goes.</details>

---

## Phase 4: Verify

**Goal:** every success criterion has evidence, including your written answer to "Vault (or your store) is down: can we serve? Can we deploy?"
**Done when:** each box is ticked with a link.

---

## Phase 5: Break

**Goal:** every experiment in `docs/break-it.md`, each with a postmortem.

<details><summary>Exp 1: store down</summary>Predict the time-to-failure from the TTL settings before you run it. Then compare. Also: what did a restart do to dev-mode Vault's data?</details>
<details><summary>Exp 2: lease revoked</summary>Revoking leases is how you'd contain a leak. How long until the app recovers on its own, and why?</details>
<details><summary>Exp 3: leaked secret</summary>Deleting the line in a new commit doesn't remove it from history. In a real leak, what do you do <em>first</em>?</details>
<details><summary>Exp 5: secret in image layer</summary>Look up BuildKit secret mounts. They make a secret available during one step without storing it in any layer.</details>

---

## Phase 6: Decide again, then improve

### Task 6.1: ADR-0003 to ADR-0005 accepted, citing evidence.

### Task 6.2: No token on disk
**Goal:** the workload authenticates to the secrets store using its own identity, not a stored token.
**Done when:** the lab's token-file shortcut is gone.

<details><summary>Hint 2</summary>Vault's Kubernetes auth method (with your project 03 cluster), or AWS IAM auth. Both swap "something you store" for "something you are".</details>

### Task 6.3: Least privilege for the apply role
**Goal:** replace the broad managed policy with one that grants only what your Terraform needs.
**Done when:** apply still works, and the policy is noticeably smaller.

<details><summary>Hint 2</summary>IAM Access Analyzer can generate a policy from CloudTrail activity.</details>

### Task 6.4: Offboarding runbook, timed
**Goal:** `docs/offboarding-runbook.md` completed, and timed in a dry run.

---

## Phase 7: Document

**Done when:**
- [ ] A trust-chain diagram (GitHub → AWS role → secrets store → DB).
- [ ] The interview story is filled in.
- [ ] You can answer: "What's secret zero, and how did you solve it?", "What happens when your secrets store is down?", "Someone leaked a key on GitHub. What's your first action?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| App 503s right after start | Has the secret file been rendered yet? | `vault-agent` logs; `ls` the shared volume |
| Agent "permission denied" writing the file | Which user does the agent run as, and who owns the directory? | Container user; volume ownership |
| `vault-setup` fails on GRANT | Do the tables exist yet? | Compose `depends_on` order; migrate logs |
| Everything broke after restarting Vault | What does dev mode keep across restarts? | Vault dev-server docs |
| Username never changes | Renewal or rotation? | `default_ttl` / `max_ttl` |
| `EntityAlreadyExists` for the OIDC provider | Does your account already have one? | Terraform `import` docs |
| CI can't assume role | Does the token's `sub` match exactly? Does the job request an ID token? | Trust policy; workflow `permissions:` |
| gitleaks flags a harmless value | Is it truly harmless? Then how do you document an exception? | `.gitleaks.toml` allowlist |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
