import tempfile
import unittest
from pathlib import Path
from pipeline.cli import init, next_stage, complete, approve, load, STAGES

class PipelineTests(unittest.TestCase):
    def test_requirements_and_approval_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            init(tmp)
            next_stage(tmp)
            req = Path(tmp)/STAGES[0]['output']
            req.write_text('# Requirements\nREQ-001: application requirements gathered from user.\n')
            complete(tmp)
            next_stage(tmp)
            analysis = Path(tmp)/STAGES[1]['output']
            analysis.write_text('# Analysis\nREQ-001 validated.\n')
            complete(tmp)
            with self.assertRaises(ValueError): next_stage(tmp)
            with self.assertRaises(ValueError): approve(tmp, 'system-design')
            approve(tmp, 'analysis')
            next_stage(tmp)
            self.assertTrue((Path(tmp)/STAGES[2]['output']).exists())
    def test_no_empty_or_placeholder_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            init(tmp); next_stage(tmp)
            with self.assertRaises(ValueError): complete(tmp)
            _,_,state=load(tmp)
            self.assertEqual(state['current'],0)

if __name__ == '__main__': unittest.main()
