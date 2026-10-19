"""Run a Codex specialist for the current stage; never advances state."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from .cli import ROOT, STAGES, load

def run_codex(workspace, agent, *, dry_run=False, codex_bin="codex"):
    base, _, state = load(workspace)
    if state["pending_approval"]:
        raise ValueError("Human approval pending: " + state["pending_approval"])
    idx = state["current"]
    if idx >= len(STAGES):
        raise ValueError("Pipeline already complete")
    stage = STAGES[idx]
    profile = ROOT / "agents" / (agent + ".md")
    if not profile.is_file() or agent != profile.stem:
        raise ValueError("Unknown agent; see pipeline.cli agents")
    if idx and STAGES[idx-1]["id"] not in state["completed"]:
        raise ValueError("Previous stage incomplete")
    prior = STAGES[idx-1]["output"] if idx else None
    if prior and not (base / prior).is_file():
        raise ValueError("Missing prior artifact: " + prior)
    prompt = "\n".join([
        "You are the specialist agent described below.",
        profile.read_text(),
        f"Current stage: {stage['id']}.",
        f"Workspace: {base}.",
        f"Previous stage artifact: {prior or 'none; gather requirements from user materials'}.",
        f"Required stage report: {stage['output']}.",
        "Read the prior artifact and relevant project files. Respect AGENTS.md if present.",
        "Do not assume unapproved requirements, skip approval gates, or deploy.",
        "Write the stage report with evidence, changes, open questions and test results.",
        "If information is insufficient, record blockers rather than inventing facts.",
        "Do not modify .engineering-pipeline/state.json or claim approval.",
    ])
    cmd = [codex_bin, "exec", "--sandbox", "workspace-write", "--cd", str(base), prompt]
    if dry_run:
        print(json.dumps({"stage": stage["id"], "agent": agent, "command": cmd[:6], "prompt": prompt}, indent=2))
        return
    if not shutil.which(codex_bin):
        raise ValueError("Codex CLI not found; install and authenticate it first")
    (base / stage["output"]).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True)
    print("Codex finished. Review output; complete stage manually.")

def main():
    parser = argparse.ArgumentParser(description="Dispatch current stage to Codex")
    parser.add_argument("--project", default=".")
    parser.add_argument("--agent", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        run_codex(args.project, args.agent, dry_run=args.dry_run)
    except (ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"Error: {exc}\n")

if __name__ == "__main__":
    main()
