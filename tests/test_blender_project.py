"""The Blender route creates only explicit project records, never a scene or media."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from init_project import create


class BlenderProjectTests(unittest.TestCase):
    def test_initialization_keeps_state_and_asset_choices_without_media_or_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            for strategy in (None, 'reuse', 'mixed', 'generate'):
                with self.subTest(strategy=strategy):
                    out = Path(temporary) / str(strategy)
                    result = create('blender-layered', 'layered-character', out, strategy)
                    state = json.loads((out / 'status.json').read_text())
                    self.assertEqual(result['status'], 'INITIALIZED')
                    self.assertEqual(state['workflow'], 'blender-layered')
                    self.assertEqual(state['workflow_status'], 'active')
                    self.assertEqual(state['status'], 'PLANNED')
                    self.assertEqual(state['adoption'], 'PENDING')
                    self.assertEqual(state['asset_strategy'], strategy)
                    self.assertEqual(state['artifacts'], [])
                    self.assertEqual(state['pending_actions'], [])
                    if strategy is None:
                        self.assertIn('Confirm reuse', state['next_action'])
                    self.assertEqual((out / 'blender-layered-brief.md').read_bytes(),
                                     (ROOT / 'templates/Blender分层角色动画制作单.md').read_bytes())
                    self.assertTrue(all((out / name).is_file() for name in
                                        ('public-defaults.md', 'delivery.md', 'plan.md', 'events.md')))
                    snapshot = {p.relative_to(out): p.read_bytes()
                                for p in out.rglob('*') if p.is_file()}
                    self.assertFalse(any(p.suffix.lower() in {'.png', '.mp4', '.wav', '.blend', '.py'}
                                         for p in snapshot))
                    with self.assertRaises(FileExistsError):
                        create('blender-layered', 'replacement', out, 'generate')
                    self.assertEqual(snapshot, {p.relative_to(out): p.read_bytes()
                                                for p in out.rglob('*') if p.is_file()})


if __name__ == '__main__':
    unittest.main()
