# What I'd do differently at a different scale

Write this **after** the break-it experiments, in your own words. The prompts below are a starting point.

## Now: 1 person, 2 environments

- What was enough, and what would have been over-engineering?

## 10×: a team of ~10, several services

- State split by component (ADR-0001 option 3)? Terragrunt or remote-state wiring?
- Apply via Atlantis / Terraform Cloud so the reviewed plan is the applied plan.
- Policy as code (OPA/Conftest, Checkov) as a required check: e.g. "no `0.0.0.0/0` ingress", "all resources tagged".
- Versioned modules in their own repo, consumed by tag.

## 100×: an organization, many teams and accounts

- An account per environment / per team (AWS Organizations, SCPs) instead of VPC-level separation.
- A platform team owns the modules; product teams own thin root modules.
- Drift: prevented with SCPs and read-only console, not just detected.
- Cost: one NAT per AZ per account adds up. Consider shared egress VPC / Transit Gateway.

## The one-paragraph version for interviews

>
