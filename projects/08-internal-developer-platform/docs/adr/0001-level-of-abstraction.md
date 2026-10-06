# ADR-0001: Level of abstraction

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Teams need to ship services without becoming Kubernetes, CI and security experts. Too little abstraction means chaos;
too much means teams fight the platform or work around it.

## Options considered

### Option 1: Docs + example repo ("copy this")
- **Pros:** Cheap. Full flexibility.
- **Cons:** Copies diverge on day two. Improvements never reach existing services.

### Option 2: Templates + shared, versioned building blocks (starter: skeleton + reusable workflow + GitOps)
- **Pros:** Fast start. Shared parts update centrally by version bump. Teams still see and own their YAML.
- **Cons:** Template output diverges over time. Versioned workflows need a deprecation process.

### Option 3: Full abstraction (a PaaS: a `service.yaml` spec → everything generated, e.g. Score, KubeVela, Heroku-like)
- **Pros:** Smallest cognitive load for product teams.
- **Cons:** Every unusual need becomes a platform feature request. The platform team becomes a bottleneck.

## Questions to answer before deciding

- Where is the escape hatch, and what does using it cost the team? (They then own what they changed.)
- How many teams/services? Option 3 pays off only at scale.

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


