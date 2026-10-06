# Break-it experiments (game days)

Each game day is an experiment. Write the hypothesis (e.g. "we'll detect a Kafka issue in under 5 minutes"),
run it blind, then compare the timeline with `game_master.py reveal`.

### Game day 1: Your first blind incident
- **Procedure:** a random scenario with your process as written.
- **Measure:** time to detect, time to identify root-cause service, time to mitigate, number of wrong turns, time to first status update.
- **Result:**

### Game day 2: The unowned service
- **Procedure:** `--id risk-engine-down`.
- **Measure:** who was paged? Who decided what to do? How long did that take?
- **Result:**

### Game day 3: Silent degradation
- **Procedure:** `--id slow-postgres`.
- **Measure:** did anyone notice? How? (This feeds project 15's coverage audit.)
- **Result:**

### Game day 4: Two incidents at once
- **Procedure:** `--id double-trouble`.
- **Measure:** did you treat it as one incident or two? Was the second one found?
- **Result:**

### Game day 5: The bad runbook
- **Procedure:** any scenario involving price-feed. Follow its runbook literally.
- **Measure:** what happened? Write what the runbook should say.
- **Result:**

### Game day 6: Handoff mid-incident
- **Procedure:** halfway through, the IC hands over to someone else (or to "future you" after a 10-minute break, using only the written notes).
- **Measure:** what was lost in the handoff?
- **Result:**
