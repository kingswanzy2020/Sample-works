# What I'd do differently at a different scale

## Now: one person, a few services
- Honestly: was a platform justified? What was the smallest useful piece?

## 10×: ~5 teams, ~30 services
- A versioned template + reusable workflows + GitOps + policies in Audit is about right.
- One platform engineer per ~5–10 product teams; the platform has a roadmap and users.

## 100×: dozens of teams
- Dedicated platform team run as a product (PM, user research, SLAs).
- Higher abstraction (service spec → generated infra) for common cases; supported escape hatches for the rest.
- Multi-cluster GitOps, fleet-wide policy reporting, cost and scorecards per team in the portal.

## The one-paragraph version for interviews

>
