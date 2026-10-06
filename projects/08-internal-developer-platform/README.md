# Project 08: An internal developer platform ("paved road")

> **Problem:** Every new service takes a week to set up. Each one does CI, logging,
> deploys and security differently, so every incident starts with "how does *this* one work?"

This is the capstone: it packages the decisions from projects 01–07 so other teams get them by default.
It is the most senior-sounding project, because it is about **other engineers' experience**, not just infrastructure.

**Need help while building?** See [`docs/build-plan.md`](docs/build-plan.md): tasks with a goal and a "done when" check, hints hidden in levels (nudge → concept → docs), and a diagnosis table. It never gives you the full solution.

## Decisions this project proves you can make

1. **How much to abstract:** templates, a platform, or a full PaaS. Where can teams leave the defaults?
2. **Delivery model:** GitOps (pull) vs CI pushes to the cluster.
3. **Mandatory vs optional:** which defaults are guardrails (enforced) and which are suggestions.
4. **Platform as a product:** how you measure whether anyone benefits.
5. **Build vs buy:** Backstage vs a commercial portal vs a README and a template repo.

## Success criteria

- [ ] A new service goes from nothing to **running in staging in under 30 minutes**, measured with someone who didn't build the platform.
- [ ] Every service from the template passes CI, is signed, has probes/requests/owner, and shows up in the catalog.
- [ ] Policies run in Audit, then Enforce, with a documented exception process.
- [ ] Deploys and rollbacks are git commits (GitOps). Manual `kubectl edit` is reverted automatically.
- [ ] You can show DORA-style numbers before and after (lead time, deploy frequency, change failure rate, time to restore).

## Prerequisites and cost

- Local: kind, kubectl, Argo CD, Kyverno. Backstage is optional: the skeleton works with `cookiecutter`-style copying too.
- Builds on: 02 (CI), 03 (deploy manifests), 04 (metrics), 05 (signing identity), 07 (requests/labels).

## Starter layout

```
backstage/template.yaml                # scaffolder template: form → repo → catalog
backstage/skeleton/                    # what every new service starts with (scores 9/9 on the scorecard)
reusable-workflows/.github/workflows/service-ci.yml   # versioned golden pipeline, called with `uses:`
gitops/argocd/applicationset.yaml      # one Argo CD app per gitops/apps/<svc>/<env> folder
gitops/apps/sample-service/            # base + staging/prod overlays pinned by digest
policies/kyverno/                      # owner label, requests+probes, no :latest, signed images only
scripts/scorecard.sh                   # how far is a repo from the paved road?
```

## Milestones

### Build
- [ ] Install Argo CD on kind, point the ApplicationSet at your repo, and deploy `sample-service` to staging by commit.
- [ ] Put `service-ci.yml` in a `platform` repo, tag it `v1`, and call it from a generated service.
- [ ] Generate a service from the skeleton (Backstage, or replace `${{ values.* }}` by hand) and time it.

### Test
- [ ] **Usability test:** ask someone else to create and deploy a service with only the README. Note every question they ask. Each question is a platform bug.
- [ ] Run `scripts/scorecard.sh` on project 03's repo, and on a generated service.

### Break
- [ ] [`docs/break-it.md`](docs/break-it.md): breaking change to the reusable workflow, Enforce mode on day one, `kubectl edit` vs self-heal, escape-hatch abuse.

### Decide
- [ ] ADR-0001 to ADR-0005.

### Improve
- [ ] Add a "promote to prod" flow: a PR that bumps the digest in `gitops/apps/<svc>/prod`.
- [ ] Add scorecards to the Backstage catalog (or a weekly report across repos).

### Document
- [ ] A one-page "platform product brief": users, problem, success metrics, what's **out** of scope.

## ADRs

| # | Decision | Status |
|---|----------|--------|
| [0001](docs/adr/0001-level-of-abstraction.md) | Templates vs platform vs PaaS | Proposed |
| [0002](docs/adr/0002-gitops-vs-push.md) | GitOps pull vs CI push | Proposed |
| [0003](docs/adr/0003-guardrails-vs-gates.md) | What's mandatory, and how it's enforced | Proposed |
| [0004](docs/adr/0004-measuring-the-platform.md) | How we know the platform helps | Proposed |
| [0005](docs/adr/0005-build-vs-buy-portal.md) | Backstage vs commercial vs none | Proposed |

## Interview story

> "Setting up a service took ___ days and every one was different. I built a paved road: a template,
> a versioned CI workflow, GitOps deploys and policies. Time to first deploy went from ___ to ___.
> The first version enforced ___ on day one and blocked ___ teams, so I changed to ___.
> I'd buy instead of build when ___."
