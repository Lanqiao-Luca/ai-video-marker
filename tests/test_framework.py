"""Behavior checks for new route initialization and optional planar compositing."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from init_project import create

try:
    import numpy as np
    from painted_world_reveal import reveal_painted_world
except ImportError:
    np = None


class FrameworkProjectTests(unittest.TestCase):
    def test_painting_project_has_resume_inputs_but_no_generated_media(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / 'painting'
            result = create('painting-world', 'blue-studio', out, 'reuse')
            state = json.loads((out / 'status.json').read_text())
            self.assertEqual(result['status'], 'INITIALIZED')
            self.assertEqual(state['workflow_status'], 'candidate')
            self.assertEqual(state['adoption'], 'PENDING')
            self.assertEqual(state['asset_strategy'], 'reuse')
            self.assertIsNone(state['current_unit'])
            self.assertEqual(state['pending_actions'], [])
            self.assertEqual(state['completed_units'], [])
            self.assertEqual(state['iterations_used'], 0)
            self.assertEqual(json.loads((out / 'artifacts.json').read_text())['artifacts'], [])
            self.assertTrue(all((out / f).is_file() for f in
                                ['plan.md', 'events.md', 'painting-world-brief.md']))
            self.assertEqual((out / 'painting-world-brief.md').read_bytes(),
                             (ROOT / 'templates/绘画世界穿行制作单.md').read_bytes())
            self.assertFalse(any(p.suffix in {'.mp4', '.png', '.wav'} for p in out.rglob('*')))


@unittest.skipIf(np is None, 'Optional requirements-painting.txt are not installed')
class PaintedWorldTests(unittest.TestCase):
    def setUp(self):
        self.inner = np.full((13, 19, 3), [220, 40, 70], dtype=np.uint8)
        self.outer = np.full((61, 81, 3), [10, 90, 180], dtype=np.uint8)
        self.quad = np.float32([[20, 15], [60, 15], [60, 45], [20, 45]])

    def test_endpoints_distinct_sizes_and_inputs_unchanged(self):
        original = [a.copy() for a in (self.inner, self.outer, self.quad)]
        first = reveal_painted_world(self.inner, self.outer, self.quad, 0)
        last = reveal_painted_world(self.inner, self.outer, self.quad, 1)
        np.testing.assert_allclose(first, np.broadcast_to(self.inner[0, 0] / 255., first.shape), atol=1e-6)
        np.testing.assert_allclose(last[30, 40], self.inner[0, 0] / 255., atol=1e-6)
        np.testing.assert_allclose(last[0, 0], self.outer[0, 0] / 255., atol=1e-6)
        for before, after in zip(original, (self.inner, self.outer, self.quad)):
            np.testing.assert_array_equal(before, after)
        self.assertEqual(first.shape, self.outer.shape)
        self.assertEqual(first.dtype, np.float32)

    def test_midpoint_has_intermediate_canvas_extent(self):
        frame = reveal_painted_world(self.inner, self.outer, self.quad, .5)
        np.testing.assert_allclose(frame[30, 15], self.inner[0, 0] / 255., atol=1e-6)
        np.testing.assert_allclose(frame[0, 0], self.outer[0, 0] / 255., atol=1e-6)
        self.assertTrue(np.isfinite(frame).all())
        self.assertGreaterEqual(float(frame.min()), 0)
        self.assertLessEqual(float(frame.max()), 1)

    def test_same_white_source_has_no_dark_double_alpha_edge(self):
        inner = np.ones_like(self.inner, dtype=np.float32)
        outer = np.ones_like(self.outer, dtype=np.float32)
        quad = np.float32([[15.3, 9.2], [65.4, 13.7], [59.8, 49.1], [19.1, 45.6]])
        for progress in (0, .31, .72, 1):
            np.testing.assert_allclose(reveal_painted_world(inner, outer, quad, progress), 1, atol=1e-6)

    def test_live_image_can_freeze_without_changing_geometry(self):
        live = np.full_like(self.inner, [20, 220, 50])
        still = reveal_painted_world(self.inner, self.outer, self.quad, 1)
        frozen = reveal_painted_world(self.inner, self.outer, self.quad, 1,
                                     live_inner_rgb=live, live_weight=0)
        np.testing.assert_array_equal(still, frozen)
        dynamic = reveal_painted_world(self.inner, self.outer, self.quad, 1,
                                      live_inner_rgb=live, live_weight=1)
        np.testing.assert_allclose(dynamic[30, 40], live[0, 0] / 255., atol=1e-6)
        np.testing.assert_array_equal(dynamic[0, 0], still[0, 0])
        with self.assertRaises(ValueError):
            reveal_painted_world(self.inner, self.outer, self.quad, 1, live_inner_rgb=live[:5])

    def test_bad_quad_is_rejected(self):
        invalid = [self.quad[::-1], np.roll(self.quad, 1, axis=0),
                   [[20, 15], [60, 45], [60, 15], [20, 45]],
                   [[20, 15], [60, 15], [30, 20], [20, 45]],
                   [[-1, 15], [60, 15], [60, 45], [20, 45]],
                   [[20, 15]] * 4,
                   [[float('nan'), 15], [60, 15], [60, 45], [20, 45]]]
        for quad in invalid:
            with self.subTest(quad=quad), self.assertRaises(ValueError):
                reveal_painted_world(self.inner, self.outer, quad, .5)

    def test_invalid_ranges_and_ambiguous_image_formats_fail(self):
        for progress in (float('nan'), float('inf'), -0.1, 1.1, True, '.5'):
            with self.subTest(progress=progress), self.assertRaises((ValueError, TypeError)):
                reveal_painted_world(self.inner, self.outer, self.quad, progress)
        bad_images = [np.zeros((5, 5, 4), np.uint8), np.zeros((1, 5, 3), np.uint8),
                      np.full((5, 5, 3), float('nan')), np.ones((5, 5, 3)) * 2,
                      np.ones((5, 5, 3), np.int32)]
        for image in bad_images:
            with self.subTest(shape=image.shape), self.assertRaises((ValueError, TypeError)):
                reveal_painted_world(image, self.outer, self.quad, .5)
        with self.assertRaises(ValueError):
            reveal_painted_world(self.inner, self.outer, self.quad, .5, live_weight=2)


if __name__ == '__main__':
    unittest.main()
