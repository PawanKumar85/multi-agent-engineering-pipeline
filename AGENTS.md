# Multi-Agent Engineering Project Rules

1. Gather requirements first from chat and supplied files (PDF, DOCX, Markdown, images, codebase). Ask clarifying questions and record requirement IDs and acceptance criteria.
2. Do not begin design or implementation until the human explicitly approves validated requirements. Preserve approvals in the pipeline state.
3. Read each prior stage artifact as the next stage's input. Never silently fill in unresolved business decisions.
4. At implementation, route each task to the matching specialist in `agents/`. Use `skills/` instructions when applicable.
5. Run tests and report actual evidence; do not claim execution or deployment without performing it.
6. Hooks are event handlers, not substitutes for human approval. Follow the stage gates in `pipeline/cli.py`.
7. Require explicit human approval before production deployment or irreversible changes.
