# Break-it experiments

### Experiment 1: Alert storm
- **Procedure:** inject a Kafka fault in the landscape (or `scripts/replay.sh` a large fixture).
- **Measure:** how many notifications reached a human? How many groups? Was Kafka identified as probable cause?
- **Result:**

### Experiment 2: Triage down
- **Procedure:** stop the triage service, then inject a tier-1 fault.
- **Measure:** did a page still reach a human? How long until anyone noticed triage was down?
- **Result:**

### Experiment 3: False merge
- **Procedure:** run project 12's `double-trouble` scenario.
- **Measure:** one group or two? If one, what rule caused it?
- **Result:**

### Experiment 4: Stale catalog
- **Procedure:** change an owner in `catalog.yaml` to a team that no longer exists, and remove a `depends_on` edge.
- **Measure:** where did the page go? Did correlation still work?
- **Result:**

### Experiment 5: Slow dependency during enrichment
- **Procedure:** make a diagnostic call hang (e.g. point it at a port that never answers).
- **Measure:** how long was the page delayed? Did your timeouts work?
- **Result:**
