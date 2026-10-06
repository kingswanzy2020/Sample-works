# Build plan: Project 11, Ansible for a hybrid fleet

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how you'll know it's done.
Open hints one level at a time, after a real attempt (20–30 min): **Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Rough time:** 15–25 hours.

---

## Phase 0: Setup

### Task 0.1: The lab fleet answers
**Goal:** 6 lab servers up; `playbooks/ping.yml` passes for all.
**Done when:** every host reports `ok` with no failures.

<details><summary>Hint 1</summary>Ansible connects as the <code>ops</code> user with the key the lab script generated. Where is that configured?</details>

### Task 0.2: Know what Ansible knows
**Goal:** list the facts Ansible gathers about one host.
**Done when:** you can name 5 facts that would help a fleet report (OS, kernel, CPU count…).

<details><summary>Hint 2</summary>The <code>setup</code> module; ad-hoc commands with <code>-m</code>.</details>

---

## Phase 1: Measure the "before"

### Task 1.1: Fleet report
**Goal:** one command that prints OS, kernel and key package versions for every server.
**Done when:** the output is a readable table or file, not raw JSON.

<details><summary>Hint 1</summary>Facts are per host. How do you collect them into one place at the end of a play?</details>
<details><summary>Hint 2</summary>Look at running a task once (<code>run_once</code>) on the control node (<code>delegate_to: localhost</code>) with <code>hostvars</code>.</details>

### Task 1.2: Seed drift and see it (without reading the script)
**Done when:** you have a list of what you *think* changed, before writing any roles.

---

## Phase 2: Decide

### Task 2.1: ADR-0001 and ADR-0002
**Done when:** ADR-0001 states the Terraform/Ansible boundary in one sentence.

---

## Phase 3: Build

### Task 3.1: The baseline role
**Goal:** a role that defines the baseline for every server.
**Done when:** a fresh server converges, and a second run reports 0 changed.

<details><summary>Hint 1</summary>Prefer modules that describe a <em>state</em> over <code>command</code>/<code>shell</code>. Why are those two the usual cause of non-idempotence?</details>
<details><summary>Hint 2</summary>When you must use <code>command</code>, look at <code>creates</code>, <code>changed_when</code> and <code>check_mode</code>.</details>
<details><summary>Hint 3</summary>https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html</details>

### Task 3.2: Drift detection
**Goal:** a scheduled or on-demand run that reports drift without changing anything.
**Done when:** after `seed-drift.sh`, the report lists the changes your role manages.

<details><summary>Hint 1</summary>A role can only detect drift in things it manages. What about things that were <em>added</em> (a new user, a cron file)?</details>
<details><summary>Hint 2</summary>Check mode plus diff output; or tasks that list "what exists" and compare with "what should exist".</details>

### Task 3.3: Safe rollout
> **Depends on your ADR-0003:** batches only need play keywords. A health gate needs a task that checks something meaningful between batches.

**Done when:** experiment 3 stops after the first batch.

<details><summary>Hint 2</summary>Play keywords: <code>serial</code>, <code>max_fail_percentage</code>. Task: <code>wait_for</code> / <code>uri</code> / <code>assert</code> as a gate.</details>

### Task 3.4: Role tests
> **Depends on your ADR-0004:** Molecule needs its own scenario directory per role. Check mode needs a way to fail CI on unexpected changes.

**Done when:** a CI job (or a local command) converges, checks idempotence, and verifies the baseline.

<details><summary>Hint 3</summary>https://ansible.readthedocs.io/projects/molecule/</details>

### Task 3.5: Latency tuning role on VMs
**Goal:** project 10's tuning list as `roles/latency_tuning`, applied to real VMs.
**Done when:** a verify step proves each setting is active (not just "the task ran").

<details><summary>Hint 1</summary>Some settings need a reboot to take effect. How does your role handle that safely, one host at a time?</details>
<details><summary>Hint 2</summary>Modules: <code>ansible.posix.sysctl</code>, <code>ansible.builtin.reboot</code>, <code>handlers</code>.</details>

---

## Phase 4: Verify
**Done when:** every success criterion has evidence (run output, the report, the stopped rollout).

## Phase 5: Break
**Goal:** all experiments in `docs/break-it.md`, each with a postmortem.

## Phase 6: Decide again, then improve
- [ ] ADR-0003 to ADR-0005 accepted with evidence.
- [ ] Secrets: no plaintext secrets in the repo (Ansible Vault or a lookup to your project 05 store).

## Phase 7: Document
- [ ] Interview story with numbers.
- [ ] You can answer: "What makes a task idempotent?", "How do you roll out a risky change to 500 servers?", "Ansible or Packer?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| `UNREACHABLE` | Is the container up? Right port? Right key? | `docker compose ps`; `ansible -vvv` |
| Host key warnings after rebuild | Did the server get a new host key? | `ansible.cfg` host key checking (lab only) |
| `Missing sudo password` | Does the user have passwordless sudo? Did you set `become`? | Play `become:` |
| Changed on every run | Which module is reporting change, and why? | `--diff`; task type |
| sysctl fails in the lab | Is this a container? | README note about kernel settings |
| "Non-blocking IO" error when piping output | Is stdout a pipe in your terminal or CI? | Run without piping, or redirect stdin from `/dev/null` |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
