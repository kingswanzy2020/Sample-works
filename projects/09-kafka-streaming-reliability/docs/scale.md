# What I'd do differently at a different scale

## Now: one topic, one consumer group, a laptop
- What settings did the evidence support? What was overkill?

## 10×: many topics and teams
- Topic creation through code review (Terraform provider / GitOps), naming and retention standards.
- Quotas per client, so one team can't starve the others.
- Schema registry so a producer change can't break consumers.

## 100×: firm-wide streaming platform
- Multi-cluster: separate latency-critical and analytics clusters; replication between sites (MirrorMaker 2 / cluster linking).
- Tiered storage for long retention without huge broker disks.
- A platform team with SLOs for the platform itself (projects 16/17).

## The one-paragraph version for interviews

>
