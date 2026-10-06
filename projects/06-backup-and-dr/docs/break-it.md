# Break-it experiments

Each experiment should end with a postmortem that compares **documented** vs **measured** recovery.

### Experiment 1: Delete the production database
- **Hypothesis:** I can restore within my RTO target, losing at most RPO worth of data.
- **Procedure:** `docker compose down` then `docker volume rm <project>_pgdata` (the primary is gone). Restore **into the primary**, not the drill DB:
  bring up an empty `db`, restore the latest dump, point the app at it, verify via the API.
- **Measure:** total time from "it's gone" to "API returns data", and rows lost. Note every manual step you had to figure out.
- **Result:**

### Experiment 2: Corrupted / empty backup
- **Procedure:** Make `backup.sh` produce an empty file (e.g. wrong DB name with `|| true`). Does the backup "succeed"? Does the drill catch it?
- **Measure:** how long would this have gone unnoticed with only job-success monitoring?
- **Result:**

### Experiment 3: Ransomware the bucket
- **Procedure (cloud, governance mode):** with the writer role, try to delete a backup. Then with an admin role. Then try to overwrite one.
- **Measure:** what succeeded? What does versioning/object lock leave you with?
- **Result:**

### Experiment 4: Region loss game day
- **Procedure:** Pretend `us-east-1` is gone. Using only the backup account and git: stand up project 01 in another region, restore data, deploy the app.
- **Measure:** wall-clock time; list every hard-coded region, AMI, ARN or secret that broke.
- **Result:**

### Experiment 5: The bad `DELETE`
- **Procedure:** `DELETE FROM items WHERE id > 10;` at a known time. Recover only the deleted rows without losing writes made afterwards.
- **Measure:** possible with dumps? With PITR (restore to a side instance, then copy the rows back)?
- **Result:**
