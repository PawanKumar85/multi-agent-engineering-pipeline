# Architecture and trust boundaries

The CLI is a deterministic local coordinator. `pipeline/stages/*.json` defines stage order, output paths, skills, and approval flags. `agents/*.md` defines specialist responsibilities. `hooks/*.py` are example synchronous event hooks. The target workspace stores `docs/` artifacts and `.engineering-pipeline/state.json`.

**Handoff:** Stage N writes its output; the next stage reads that output as its primary input, together with approved upstream documents. Humans approve six checkpoints. Hook failure blocks transitions. The CLI does not check document semantics, authenticate approvers, schedule parallel agents, or call LLMs; these are future integration points.

**Future adapters:** LLM provider/runtime integration; PDF/DOCX/image extraction; task DAG scheduler with dependencies; approval identity and audit trail; git change review; secure MCP tool policy; observability.
