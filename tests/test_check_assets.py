"""Audit behavior on tiny declared fixtures, without rendering or real media copies."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import wave
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from check_assets import audit, safe, TOPIC


class AssetAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.image = self.root / Path(TOPIC).parent / 'one.png'
        self.image.parent.mkdir(parents=True)
        Image.new('RGB', (3, 2), 'red').save(self.image)
        raw = self.image.read_bytes()
        self.topic = dict(image_count=1, total_bytes=len(raw),
                          license={'image_reuse_license': 'NOT_SEPARATELY_DECLARED'},
                          files=[dict(file='one.png', sha256=hashlib.sha256(raw).hexdigest(),
                                      bytes=len(raw), width=3, height=2, format='PNG')])
        self.write(TOPIC, self.topic)
        self.write('assets/migration-20261028.json', dict(media_count=0, total_bytes=0, files=[]))
        self.write('assets/images/catalog.json', dict(packs=[], license='MIT'))
        self.write('assets/images/harbor/manifest.json', dict(files={}))
        self.write('assets/audio/pixel-rooftop/source.json', dict(file='music.wav', sha256='0' * 64))
        # Leave audio/poster/video absent: tests assert focused errors, not a fixture PASS.
        self.write('examples/reference-comic/manifest.json', dict(
            video=dict(path='../../assets/videos/reference-comic/preview.mp4', sha256='0' * 64),
            poster=dict(path='../../assets/images/reference-comic/poster.jpg', sha256='0' * 64)))
        for name in ('assets/images/harbor/README.md', str(Path(TOPIC).parent / 'README.md'),
                     'assets/images/README.md', 'assets/videos/README.md', 'assets/audio/pixel-rooftop/NOTICE.md'):
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('fixture notice')

    def write(self, relative, data):
        p = self.root / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data))

    def errors(self):
        return audit(self.root, (TOPIC,))['errors']

    def test_complete_declared_fixture_passes_without_changing_any_input(self):
        video = self.root / 'assets/videos/reference-comic/preview.mp4'
        video.parent.mkdir(parents=True)
        video.write_bytes(b'byte-identity-only-not-a-real-video')
        poster = self.root / 'assets/images/reference-comic/poster.jpg'
        poster.parent.mkdir(parents=True)
        Image.new('RGB', (2, 2), 'blue').save(poster)
        audio = self.root / 'assets/audio/pixel-rooftop/music.wav'
        with wave.open(str(audio), 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(8)
            wav.writeframes(b'\0' * 16)
        def spec(p):
            raw = p.read_bytes()
            return dict(path=p.relative_to(self.root).as_posix(),
                        sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
        self.write('assets/migration-20261028.json', dict(media_count=3,
            total_bytes=sum(p.stat().st_size for p in (video, poster, audio)),
            files=[spec(p) for p in (video, poster, audio)]))
        self.write('assets/audio/pixel-rooftop/source.json', dict(file='music.wav',
            sha256=spec(audio)['sha256'], sample_rate=8, channels=1, duration=1))
        self.write('examples/reference-comic/manifest.json', dict(
            video=dict(path='../../' + spec(video)['path'], sha256=spec(video)['sha256']),
            poster=dict(path='../../' + spec(poster)['path'], sha256=spec(poster)['sha256'], width=2, height=2)))
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = audit(self.root, (TOPIC,))
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['files'], 4)
        self.assertIn('MP4 byte identity only', result['coverage'])
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes()
                                  for p in self.root.rglob('*') if p.is_file()})

    def test_module_license_remains_separate_and_missing_files_are_reported(self):
        result = audit(self.root, (TOPIC,))
        module = result['modules'][str(Path(TOPIC).parent)]
        self.assertIn('NOT_SEPARATELY_DECLARED', module['purpose'])
        self.assertEqual(module['files'], 1)
        self.assertTrue(any('Missing media: assets/videos/' in x for x in result['errors']))
        self.assertFalse(any('one.png' in x for x in result['errors']))

    def test_unregistered_and_changed_media_are_reported(self):
        (self.image.parent / 'extra.png').write_bytes(self.image.read_bytes())
        self.assertTrue(any('Unregistered media:' in x for x in self.errors()))
        self.image.write_bytes(b'corrupt')
        self.assertTrue(any('SHA mismatch:' in x for x in self.errors()))
        self.assertTrue(any('cannot identify image' in x for x in self.errors()))
        (self.root / 'assets/audio/pixel-rooftop/music.wav').write_bytes(b'RIFF')
        self.assertTrue(any('EOFError' in x for x in self.errors()))

    def test_current_metadata_conflict_cannot_replace_frozen_sha(self):
        raw = self.image.read_bytes()
        self.write('assets/migration-20261028.json', dict(media_count=1, total_bytes=len(raw),
            files=[dict(path=self.image.relative_to(self.root).as_posix(), sha256='1' * 64, bytes=len(raw))]))
        self.assertTrue(any('Conflicting declared SHA' in x for x in self.errors()))
        self.topic['files'][0]['width'] = 7
        self.write(TOPIC, self.topic)
        self.assertTrue(any('dimensions mismatch' in x for x in self.errors()))

    def test_catalog_and_manifest_symlinks_counts_and_bad_size_fail_cleanly(self):
        catalog_path = self.root / 'assets/images/catalog.json'
        backup = catalog_path.with_name('catalog-backup.json')
        backup.write_bytes(catalog_path.read_bytes())
        catalog_path.unlink()
        catalog_path.symlink_to(backup)
        self.assertTrue(any('Symlink' in x for x in self.errors()))
        catalog_path.unlink()
        self.write('assets/images/catalog.json', dict(packs=[], license='MIT', image_count=1))
        self.assertTrue(any('catalog total mismatch' in x for x in self.errors()))
        self.write('assets/images/catalog.json', dict(license='MIT', image_count=1,
            packs=[dict(id='demo', manifest='demo/manifest.json', image_count=1)]))
        self.write('assets/images/demo/real.json', dict(id='demo', license='MIT',
            files=[dict(file='test.png', sha256='0' * 64, size=[])]))
        manifest = self.root / 'assets/images/demo/manifest.json'
        manifest.symlink_to(manifest.with_name('real.json'))
        self.assertTrue(any('Symlink' in x for x in self.errors()))
        manifest.unlink()
        manifest.write_bytes(manifest.with_name('real.json').read_bytes())
        manifest.with_name('README.md').write_text('fixture')
        self.assertTrue(any('Declaration error:' in x for x in self.errors()))

    def test_second_topic_module_is_checked_independently(self):
        from check_assets import TOPICS
        second = TOPICS[1]
        image = self.root / Path(second).parent / 'second.png'
        image.parent.mkdir(parents=True)
        image.write_bytes(self.image.read_bytes())
        image.with_name('README.md').write_text('separate module notice')
        topic = dict(self.topic, module='second', files=[dict(self.topic['files'][0], file='second.png')])
        self.write(second, topic)
        result = audit(self.root)
        self.assertFalse(any('second.png' in x for x in result['errors']))
        self.assertIn('NOT_SEPARATELY_DECLARED', result['modules'][str(Path(second).parent)]['purpose'])
        image.write_bytes(b'broken')
        result = audit(self.root)
        self.assertTrue(any('SHA mismatch:' in x and 'second.png' in x for x in result['errors']))
        self.assertFalse(any('one.png' in x for x in result['errors']))

    def test_additional_modules_have_independent_identity_and_notice(self):
        from check_assets import TOPICS
        for path in TOPICS[1:]:
            image = self.root / Path(path).parent / 'new.png'
            image.parent.mkdir(parents=True)
            image.write_bytes(self.image.read_bytes())
            image.with_name('README.md').write_text('independent notice')
            self.write(path, dict(self.topic, files=[dict(self.topic['files'][0], file='new.png')]))
        for path in TOPICS[2:]:
            with self.subTest(module=path):
                result = audit(self.root)
                module = str(Path(path).parent)
                self.assertEqual(result['modules'][module]['files'], 1)
                self.assertIn('NOT_SEPARATELY_DECLARED', result['modules'][module]['purpose'])
                self.assertFalse(any(module in x for x in result['errors']))
                image = self.root / module / 'new.png'
                original = image.read_bytes()
                image.write_bytes(b'broken-additional-module')
                result = audit(self.root)
                self.assertTrue(any('SHA mismatch:' in x and module in x for x in result['errors']))
                self.assertFalse(any('one.png' in x for x in result['errors']))
                image.write_bytes(original)

    def test_traversal_and_internal_symlink_are_rejected(self):
        for path in ('../outside.png', '/tmp/outside.png', ''):
            with self.subTest(path=path), self.assertRaises(ValueError):
                safe(self.root, path)
        link = self.root / 'assets/link'
        link.symlink_to(self.image.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            safe(self.root, 'assets/link/one.png')
        self.topic['files'][0]['file'] = '../outside.png'
        self.write(TOPIC, self.topic)
        self.assertTrue(any('Declaration error:' in x for x in self.errors()))


if __name__ == '__main__':
    unittest.main()
