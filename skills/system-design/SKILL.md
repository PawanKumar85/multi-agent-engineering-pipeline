---
name: system-design
description: Use when designing scalable systems and evaluating architecture decisions.
---

# System architecture and tradeoff analysis

## Workflow

1. Read project context and identify existing conventions.
2. Clarify requirements, constraints, and acceptance criteria.
3. Break work into small verifiable steps with dependencies.
4. Implement the smallest safe change.
5. Run relevant checks and report results and remaining risks.

## Engineering rules

- Clarify functional requirements, scale, SLOs, and constraints.
- Draw components, data flow, ownership, and failure boundaries.
- Compare alternatives with explicit latency, cost, reliability, and complexity tradeoffs.
- Plan capacity, caching, queues, consistency, security, and observability.
- Identify failure modes, rollout strategy, and validation metrics.

## Output contract

For implementation tasks, provide: plan, changed files, tests executed, tradeoffs, and any unverified assumptions. Do not claim a test passed unless it was actually run.
