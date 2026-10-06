# Runbook: kafka

**Owner:** team-platform · **Tier:** 1 (platform) · **Last reviewed:** 2026-06-30

## Impact
Every streaming consumer depends on Kafka: price-feed, order-gateway, positions-api.
**When Kafka degrades, expect alerts from those services too. Treat them as one incident.**

## First checks
1. Under-replicated partitions? Offline partitions?
2. Which brokers are in the ISR for the busiest topics?
3. Consumer lag for `order-router` and `price-feed` groups.

## Actions
- One broker down, ISR shrunk, no offline partitions: no client impact expected. Restore the broker, watch ISR recover.
- Offline partitions: Sev1. Page platform-secondary. Do NOT restart all brokers at once.

## Escalation
platform-primary → platform-secondary → head of infrastructure.
