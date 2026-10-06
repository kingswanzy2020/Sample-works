# ADR-0006: GitHub-hosted vs self-hosted runners

- **Status:** Proposed
- **Date:**
- **Deciders:**

## Context

Hosted runners start clean every time but are fixed-size and cold. Self-hosted can be bigger and keep warm caches.

## Options considered

### Option 1: GitHub-hosted (starter default)
- **Pros:** Zero maintenance, isolated per job, free for public repos.
- **Cons:** Cold caches, limited CPU, minutes cost on private repos.

### Option 2: Self-hosted VMs / Kubernetes (Actions Runner Controller)
- **Pros:** Faster hardware, warm caches, access to private networks.
- **Cons:** You patch them. **Security:** a PR from a fork can run code on your infrastructure, so never use them on public repos without isolation.

### Option 3: Larger GitHub-hosted runners / third-party runner services
- **Pros:** Faster without maintenance.
- **Cons:** Cost per minute.

## Questions to answer before deciding

- What is the cost per month of each, at your current minutes?
- Who could run code on a self-hosted runner, and what could that code reach?

## Decision

We will use **___** because **___**.

## Consequences

- **What this gives us:**
- **What we give up:**
- **Revisit when:**

## Evidence


