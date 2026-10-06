# Break-it experiments

### Experiment 1: Platform outage, five culprits
- **Procedure:** run project 12's `kafka-degraded` scenario for 15 minutes, then generate the report.
- **Measure:** without attribution, which teams look bad? With it, does the report tell the right story?
- **Result:**

### Experiment 2: The missing dependency
- **Procedure:** remove `kafka` from `positions-api`'s `depends_on`, repeat experiment 1.
- **Measure:** how does attribution change? How would you detect a missing edge?
- **Result:**

### Experiment 3: The overnight outage
- **Procedure:** if you can control timestamps (or simulate them), compare a fault during trading hours vs outside.
- **Measure:** does your report treat them as your ADR-0003 says it should?
- **Result:**

### Experiment 4: No data
- **Procedure:** stop the simulator for 10 minutes and regenerate the report.
- **Measure:** does a service with no data look like 100%? (It must not.)
- **Result:**
