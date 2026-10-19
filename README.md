# Multi-Agent Engineering Pipeline

A starter repository for **requirements-first, human-gated, multi-agent software engineering**. Includes 11 installable agent skills (8 original + task planning, testing, deployment), 10 specialist agent profiles, 9 pipeline stages, hook examples, and a working Python standard-library workflow CLI.

**Status:** Runnable workflow scaffold. It does **not** autonomously invoke Codex, Claude Code, or an LLM. Specialist profiles are instructions for a compatible agent runtime; external MCP servers and deployments are not automatically connected.

## Quick start

Requires Python 3.10+ (no pip dependencies).

```bash
python3 -m pipeline.cli init --project ./demo-app
python3 -m pipeline.cli next --project ./demo-app
# Edit demo-app/docs/requirements.md, replacing TODO sections with real user requirements.
python3 -m pipeline.cli complete --project ./demo-app
python3 -m pipeline.cli next --project ./demo-app
# Edit demo-app/docs/validated-requirements.md
python3 -m pipeline.cli complete --project ./demo-app
python3 -m pipeline.cli approve --stage analysis --project ./demo-app
python3 -m pipeline.cli status --project ./demo-app
python3 -m pipeline.cli agents
python3 -m unittest discover -s tests -v
```

`next` prepares an artifact with its upstream input reference. `complete` checks that the artifact exists, is nonempty, and has no TODO placeholders. **These are basic structural checks, not semantic validation.** `approve` records a local approval event, but does not authenticate the human approver; for production use add identity and audit logging.

## Workflow

1. Requirements: chat, PDF, DOCX, Markdown, screenshots, codebase → `docs/requirements.md`.
2. Analysis: reconcile gaps and confirm intent → `docs/validated-requirements.md` **(approval)**.
3. System design → `docs/system-design.md` **(approval)**.
4. Database design → `docs/database-design.md` **(approval)**.
5. Task planning → `docs/task-plan.md` **(approval)**.
6. Implementation: delegate tasks to language/database specialists → `docs/implementation-report.md`.
7. Testing → `docs/test-report.md` **(approval)**.
8. Deployment → `docs/deployment-report.md` **(approval)**.
9. Feedback → `docs/feedback.md`, informing the next iteration.

A stage output is an input to the next stage. Stage-specific hooks are defined in `pipeline/hooks.json` and run synchronously. Any nonzero hook exit blocks that command. Avoid putting secrets in stage files. The CLI does not itself extract PDF/DOCX content; your coding agent or an ingestion adapter must read those sources and consolidate the findings into requirements.

## Skills CLI (after publishing your fork/repo)

```bash
npx skills add YOUR_USERNAME/multi-agent-engineering-pipeline --list
npx skills add YOUR_USERNAME/multi-agent-engineering-pipeline --skill '*' -a codex
```

Install skills inside your target project; put the repository's `AGENTS.md` in the project root to apply its overall workflow rules. The Skills CLI installs skills, not this pipeline CLI, hook execution, or autonomous agents. Use this repository alongside your agent runtime.

## Safety and quality

- No architecture before requirements are approved.
- Do not treat generated output as verified solely because a file exists.
- Humans review high-impact changes and production deployment.
- Keep secrets out of logs, prompts, artifacts and version control.
- All coding agents report test evidence and unresolved issues.
- MCP connections are optional and configured in the actual host agent, not here.

## Codex specialist dispatch

Install and authenticate the Codex CLI on your own machine. Dispatch a specialist for the current stage using:

```bash
python3 -m pipeline.cli init --project ./demo-app
python3 -m pipeline.cli next --project ./demo-app
python3 -m pipeline.codex_adapter --project ./demo-app --agent python --dry-run
python3 -m pipeline.codex_adapter --project ./demo-app --agent python
# Review the generated stage report and changes before completing:
python3 -m pipeline.cli complete --project ./demo-app
```

List available specialists with `python3 -m pipeline.cli agents`. The adapter runs one selected specialist in Codex's `workspace-write` sandbox, references the preceding stage's artifact, and leaves state advancement and human approval to the existing workflow CLI. This does not yet implement parallel delegation, semantic artifact validation, authenticated approvals, or automatic deployment. Codex must be installed and logged in separately.
