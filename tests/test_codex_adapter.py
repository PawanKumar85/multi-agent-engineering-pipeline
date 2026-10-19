import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from pipeline.cli import init, next_stage, complete, load
from pipeline.codex_adapter import run_codex

class CodexAdapterTests(unittest.TestCase):
    def test_dry_run_does_not_advance(self):
        with tempfile.TemporaryDirectory() as tmp:
            init(tmp)
            next_stage(tmp)
            run_codex(tmp, "python", dry_run=True)
            self.assertEqual(load(tmp)[2]["current"], 0)

    def test_rejects_unknown_agent(self):
        with tempfile.TemporaryDirectory() as tmp:
            init(tmp)
            with self.assertRaises(ValueError):
                run_codex(tmp, "../../etc/passwd", dry_run=True)

    def test_pending_approval_blocks_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            init(tmp)
            next_stage(tmp)
            (Path(tmp)/"docs/requirements.md").write_text("REQ-001: Demo app")
            complete(tmp)
            next_stage(tmp)
            (Path(tmp)/"docs/validated-requirements.md").write_text("REQ-001 validated")
            complete(tmp)
            with self.assertRaisesRegex(ValueError, "approval pending"):
                run_codex(tmp, "python", dry_run=True)

    @patch("pipeline.codex_adapter.subprocess.run")
    @patch("pipeline.codex_adapter.shutil.which", return_value="/usr/bin/codex")
    def test_exec_does_not_auto_complete(self, _which, run):
        with tempfile.TemporaryDirectory() as tmp:
            init(tmp)
            run_codex(tmp, "python")
            cmd = run.call_args.args[0]
            self.assertEqual(cmd[:4], ["codex", "exec", "--sandbox", "workspace-write"])
            self.assertEqual(load(tmp)[2]["completed"], [])

if __name__ == "__main__":
    unittest.main()
