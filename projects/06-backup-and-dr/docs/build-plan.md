# Build plan: Project 06, backup and disaster recovery

A **guide for when you're stuck**, not a walkthrough. Each task says *what* to achieve and how
you'll know it's done, never *how*. Open hints one level at a time, only after a real attempt (20–30 min):
**Hint 1** a nudge, **Hint 2** the concept or tool, **Hint 3** the docs.

**Decisions:** tasks work with any option you choose. **"Depends on your ADR"** notes say what to think about, not what to type.

**Rough time:** 15–25 hours. **Cost:** local parts free. RDS PITR restores cost roughly an hour of a small instance each time.

---

## Phase 0: Setup

### Task 0.1: The local stack runs
**Goal:** db, app and S3-compatible storage up, and a first backup + restore drill passing.
**Done when:** the drill report shows PASS, and the "rows lost" number matches what you expected.

<details><summary>Hint 1</summary>The README "Run" section has the order: seed, back up, seed again, drill. Why seed twice?</details>

---

## Phase 1: Measure the "before"

### Task 1.1: Agree the targets first
**Goal:** `docs/rpo-rto.md` filled in **before** you choose any strategy.
**Done when:** every data store has an RPO and RTO with a one-line justification in business terms.

<details><summary>Hint 1</summary>Ask "what does an hour of downtime cost?" and "what does losing an hour of data cost?" separately. They're often very different.</details>

### Task 1.2: Guess, then measure
**Goal:** write down your *guessed* RTO for a full DB loss, then run experiment 1 to measure it.
**Done when:** you have the guess and the real number side by side. The gap is your story.

---

## Phase 2: Decide

### Task 2.1: ADR-0001 (backup strategy)
**Goal:** accepted, and shown to meet the RPO/RTO you set.
**Done when:** the ADR says which failures your strategy does **not** protect against.

---

## Phase 3: Build

### Task 3.1: Backups that meet your RPO

> **Depends on your ADR-0001:**
> - **Scheduled dumps:** your RPO is the schedule interval. Choose a scheduler (cron, a CI schedule or a Kubernetes CronJob) and justify it.
> - **WAL archiving / PITR (pgBackRest or WAL-G):** you'll need a Postgres image with the tool, archive settings, a base backup, and a restore procedure that replays WAL to a target time.
> - **Managed PITR (RDS):** project 01 already enables automated backups. Check the retention per environment.
> - **Replica:** fine for availability, but pair it with one of the above. Why?

**Done when:** backups run automatically on a schedule, and you can show the newest backup is never older than your RPO.

<details><summary>Hint 1 (WAL-G / pgBackRest)</summary>Postgres decides how WAL leaves the server through two settings. Look for the "archive" settings in the Postgres docs.</details>
<details><summary>Hint 2 (WAL-G / pgBackRest)</summary>Restoring to a point in time needs a recovery target and a command that fetches WAL back, plus a signal file telling Postgres to recover.</details>
<details><summary>Hint 3 (WAL-G / pgBackRest)</summary>https://www.postgresql.org/docs/16/continuous-archiving.html, https://github.com/wal-g/wal-g, https://pgbackrest.org/user-guide.html</details>

### Task 3.2: Freshness alert
**Goal:** you're told when the newest backup is older than RPO. That's a different signal from "the backup job failed".
**Done when:** stopping backups triggers the alert.

<details><summary>Hint 1</summary>Why is "job failed" alerting not enough? Think about a job that never runs at all.</details>

### Task 3.3: Automated drill in CI
**Goal:** the weekly drill workflow runs in your repo and fails when it should.
**Done when:** one green run and one deliberately red run (e.g. an empty bucket) are both linked in the README.

### Task 3.4: Backups that survive you
**Goal:** a real S3 backup bucket where the backup writer can't delete, and history survives an admin mistake.
**Done when:** you've *tried* to delete a backup with the writer credentials and failed, and written what an admin can still do.

<details><summary>Hint 1</summary>The local Compose setup points the AWS CLI at SeaweedFS. How will the scripts reach real S3 instead? Make that configurable rather than editing it each time.</details>
<details><summary>Hint 2</summary>Object Lock can only be enabled when the bucket is created. Governance vs compliance mode is a real decision. Read both before applying.</details>
<details><summary>Hint 3</summary>A separate AWS account for backups uses AWS Organizations, plus a Terraform provider that assumes a role into that account.</details>

---

## Phase 4: Verify

**Goal:** a table of documented vs **measured** RPO/RTO for each tier.
**Done when:** every number in the table comes from a drill report or a postmortem.

---

## Phase 5: Break

**Goal:** every experiment in `docs/break-it.md`, each with a postmortem.

<details><summary>Exp 1: delete the DB</summary>The drill restores to a side DB. This time you restore the <em>primary</em>. What changes, and what did you have to figure out live?</details>
<details><summary>Exp 2: empty backup</summary>A zero-byte file can still upload successfully. What would catch that?</details>
<details><summary>Exp 4: region game day</summary>Plan it like a real incident: set a start time, keep a timeline as you go, and work only from what's in git and the backup account. Every hard-coded region or ARN you hit is a finding.</details>
<details><summary>Exp 5: bad DELETE</summary>You want the deleted rows back <em>without</em> losing later writes. Restore somewhere else first. Then what?</details>

---

## Phase 6: Decide again, then improve

### Task 6.1: ADR-0002 to ADR-0004 accepted, citing the game day and drills.

### Task 6.2: Back up everything you'd need to rebuild
**Goal:** Terraform state (project 01) and secrets (project 05) are covered.
**Done when:** you could rebuild using only git and the backup account. Prove it, or list exactly what's missing.

---

## Phase 7: Document

**Done when:**
- [ ] The documented vs measured table is in the README.
- [ ] The game day postmortem is written.
- [ ] You can answer: "What's your RPO and how do you know?", "Why isn't a replica a backup?", "Could ransomware delete your backups?"

---

## Stuck? Diagnose before you search

| Symptom | Ask yourself | Where to look |
|---------|--------------|---------------|
| Backup can't connect to storage | Is the object store actually ready yet, not just started? | `docker compose logs s3` |
| `pg_restore` errors "already exists" | Am I restoring into an empty database? | `pg_restore --help` (clean options) |
| `pg_restore` version error | Are `pg_dump` and the server the same major version? | Image tags |
| Drill PASS but data looks wrong | Does the validation check the right thing? | `restore-drill.sh` validation section |
| Can't find the volume to delete | What prefix does Compose add to volume names? | `docker volume ls` |
| PITR restore "succeeds" at the wrong time | Is the target time in UTC? Is it within retention? | RDS / Postgres recovery docs |
| Object Lock settings rejected | Was the bucket created with Object Lock enabled? | S3 Object Lock docs |

**Still stuck?** Write down what you expected, what happened, and the exact error, then ask.
