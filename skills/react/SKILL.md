---
name: react
description: Use when designing, implementing, testing, or optimizing React components and hooks.
---

# React component engineering

## Workflow

1. Read project context and identify existing conventions.
2. Clarify requirements, constraints, and acceptance criteria.
3. Break work into small verifiable steps with dependencies.
4. Implement the smallest safe change.
5. Run relevant checks and report results and remaining risks.

## Engineering rules

- Prefer composable, accessible components with clear props.
- Keep derived state derived; avoid unnecessary effects and duplicated state.
- Respect hook rules and effect dependency correctness.
- Consider rendering cost, memoization only after identifying a bottleneck.
- Test user-visible behavior and loading/error/empty states.

## Output contract

For implementation tasks, provide: plan, changed files, tests executed, tradeoffs, and any unverified assumptions. Do not claim a test passed unless it was actually run.
