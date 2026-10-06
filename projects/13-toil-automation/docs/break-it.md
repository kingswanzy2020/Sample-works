# Break-it experiments

### Experiment 1: Wrong target
- **Procedure:** make an action's target selection subtly wrong (e.g. a filter that matches too much) and run it with `--execute`.
- **Measure:** which guardrail stopped it, if any? What would have happened in production?
- **Result:**

### Experiment 2: Partial failure
- **Procedure:** make `apply()` fail on the 2nd of 3 targets.
- **Measure:** what state are the targets left in? Does the output and audit log make that obvious? Can you re-run safely?
- **Result:**

### Experiment 3: The scheduled job that silently stopped
- **Procedure:** schedule market-readiness, then break its credentials or environment.
- **Measure:** how long until anyone notices it hasn't run?
- **Result:**

### Experiment 4: Automation during an incident
- **Procedure:** run a game day (project 12) while `restart-stuck-consumer` runs on a schedule.
- **Measure:** did automation help, or make diagnosis harder (restarts hiding the real cause)?
- **Result:**
