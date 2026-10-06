# What I'd do differently at a different scale

## Now: 1 service, 1 person
- Which optimizations had the best time saved per hour of effort? Which weren't worth it?

## 10×: monorepo, ~10 services, ~20 engineers
- Build-graph tooling (Bazel / Pants / Nx) with a remote cache instead of hand-written path filters.
- Merge queue so `main` is always green without every PR rebasing.
- Flaky-test detection as a service (track pass/fail per test per commit).
- Reusable workflows / composite actions owned by a platform team.

## 100×: org-wide
- Self-hosted ephemeral runners on Kubernetes (ARC) with network isolation.
- Admission control in clusters: only signed images from CI identities can run (Kyverno / Sigstore policy-controller).
- SLSA level targets for provenance; central SBOM inventory to answer "where are we running log4j?" in minutes.

## The one-paragraph version for interviews

>
