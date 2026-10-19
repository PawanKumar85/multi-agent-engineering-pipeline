---
name: database-design
description: Use when modeling relational data, writing SQL, migrations, and optimizing queries.
---

# Relational database architecture

## Workflow

1. Read project context and identify existing conventions.
2. Clarify requirements, constraints, and acceptance criteria.
3. Break work into small verifiable steps with dependencies.
4. Implement the smallest safe change.
5. Run relevant checks and report results and remaining risks.

## Engineering rules

- Start from entities, relationships, invariants, and access patterns.
- Define primary/foreign keys, constraints, and appropriate normalization.
- Choose indexes from measured query patterns and explain tradeoffs.
- Use transactions for multi-step invariants; account for concurrency.
- Plan backward-compatible migrations, backups, and query validation.

## Output contract

For implementation tasks, provide: plan, changed files, tests executed, tradeoffs, and any unverified assumptions. Do not claim a test passed unless it was actually run.
