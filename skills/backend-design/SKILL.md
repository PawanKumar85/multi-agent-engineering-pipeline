---
name: backend-design
description: Use when designing backend services, HTTP APIs, middleware, and integrations.
---

# Backend API architecture

## Workflow

1. Read project context and identify existing conventions.
2. Clarify requirements, constraints, and acceptance criteria.
3. Break work into small verifiable steps with dependencies.
4. Implement the smallest safe change.
5. Run relevant checks and report results and remaining risks.

## Engineering rules

- Specify endpoints, schemas, authentication, authorization, and error contracts.
- Separate transport, domain logic, and persistence responsibilities.
- Validate inputs and enforce authorization server-side.
- Design idempotency, timeouts, retries, observability, and rate limiting where needed.
- Test business rules, failure paths, and integration boundaries.

## Output contract

For implementation tasks, provide: plan, changed files, tests executed, tradeoffs, and any unverified assumptions. Do not claim a test passed unless it was actually run.
