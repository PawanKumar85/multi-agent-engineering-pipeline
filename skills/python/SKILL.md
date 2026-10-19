---
name: python
description: Use when writing, reviewing, debugging, or testing Python applications.
---

# Python engineering for reliable applications

## Workflow

1. Read project context and identify existing conventions.
2. Clarify requirements, constraints, and acceptance criteria.
3. Break work into small verifiable steps with dependencies.
4. Implement the smallest safe change.
5. Run relevant checks and report results and remaining risks.

## Engineering rules

- Use Python 3 type annotations; favor explicit data models and small functions.
- Handle errors deliberately; use context managers for resources.
- Use pytest with unit and integration tests; isolate external dependencies.
- For async code, distinguish blocking operations from awaitable I/O.
- Document dependency and packaging decisions.

## Output contract

For implementation tasks, provide: plan, changed files, tests executed, tradeoffs, and any unverified assumptions. Do not claim a test passed unless it was actually run.
