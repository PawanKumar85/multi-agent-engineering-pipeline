"""Local, deterministic workflow gate manager; does not execute an AI model."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIGS = sorted((ROOT / 'pipeline/stages').glob('*.json'))
STAGES = [json.loads(p.read_text()) for p in CONFIGS]
BY_NAME = {s['id']: s for s in STAGES}


def paths(workspace):
    base = Path(workspace).resolve()
    return base, base / '.engineering-pipeline' / 'state.json'


def load(workspace):
    base, file = paths(workspace)
    if not file.is_file():
        raise ValueError('Project not initialized. Run init first.')
    return base, file, json.loads(file.read_text())


def save(file, state):
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(state, indent=2) + '\n')


def hook(event, stage):
    mapping = json.loads((ROOT/'pipeline/hooks.json').read_text())
    for rel in mapping.get(event, []):
        subprocess.run([sys.executable, str(ROOT/rel), stage], check=True)


def init(workspace):
    base, file = paths(workspace)
    if file.exists():
        raise ValueError('Already initialized; existing state left unchanged.')
    base.mkdir(parents=True, exist_ok=True)
    save(file, {'current': 0, 'completed': [], 'approved': [], 'pending_approval': None})
    print(f'Initialized: {base}')


def status(workspace):
    _, _, state = load(workspace)
    print(json.dumps(state, indent=2))
    if state['current'] < len(STAGES):
        print('Next:', STAGES[state['current']]['id'])
    else:
        print('All stages completed')


def next_stage(workspace):
    base, file, state = load(workspace)
    if state['pending_approval']:
        raise ValueError('Awaiting approval: ' + state['pending_approval'])
    idx = state['current']
    if idx >= len(STAGES):
        raise ValueError('Pipeline complete')
    stage = STAGES[idx]
    if idx and STAGES[idx-1]['id'] not in state['completed']:
        raise ValueError('Previous stage not completed')
    hook('before_stage', stage['id'])
    dest = base / stage['output']
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        prev = STAGES[idx-1]['output'] if idx else 'User chat, files, existing codebase'
        dest.write_text(f'# {stage["id"]}\n\nInput: {prev}\n\n## Evidence / decisions\n\nTODO\n\n## Requirement IDs and acceptance criteria\n\nTODO\n')
    print('Prepared:', dest)
    print('Skills:', ', '.join(stage['skills']))
    if stage['id'] == 'implementation':
        print('Select a specialist in agents/ based on task ownership.')
    print('Edit and validate this artifact, then run complete.')


def complete(workspace):
    base, file, state = load(workspace)
    if state['pending_approval']:
        raise ValueError('Awaiting human approval')
    idx = state['current']
    if idx >= len(STAGES):
        raise ValueError('Pipeline complete')
    stage = STAGES[idx]
    output = base/stage['output']
    if not output.is_file() or not output.read_text().strip():
        raise ValueError('Missing/empty output: ' + str(output))
    if 'TODO' in output.read_text():
        raise ValueError('Output still contains TODO placeholders')
    if stage['id'] not in state['completed']:
        state['completed'].append(stage['id'])
    hook('after_stage', stage['id'])
    if stage['requires_approval']:
        state['pending_approval'] = stage['id']
        print('Human approval required:', stage['id'])
    else:
        state['current'] += 1
    save(file, state)


def approve(workspace, stage_name):
    _, file, state = load(workspace)
    if state['pending_approval'] != stage_name:
        raise ValueError('No pending approval for ' + stage_name)
    hook('on_approval', stage_name)
    state['approved'].append(stage_name)
    state['pending_approval'] = None
    state['current'] += 1
    save(file, state)
    print('Approved:', stage_name)


def main():
    p = argparse.ArgumentParser(description='Human-gated engineering pipeline')
    p.add_argument('command', choices=['init','status','next','complete','approve','agents'])
    p.add_argument('--project', default='.', help='Target project directory')
    p.add_argument('--stage', help='Stage name for approve')
    args = p.parse_args()
    try:
        if args.command == 'init': init(args.project)
        elif args.command == 'status': status(args.project)
        elif args.command == 'next': next_stage(args.project)
        elif args.command == 'complete': complete(args.project)
        elif args.command == 'agents': print('\n'.join(p.stem for p in sorted((ROOT/'agents').glob('*.md'))))
        elif args.command == 'approve':
            if not args.stage: raise ValueError('--stage required')
            approve(args.project, args.stage)
    except (ValueError, subprocess.CalledProcessError) as exc:
        p.exit(2, f'Error: {exc}\n')

if __name__ == '__main__': main()
