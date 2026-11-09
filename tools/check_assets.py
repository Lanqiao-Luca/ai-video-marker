"""Read-only audit of the current public media baseline and module declarations."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import wave
from PIL import Image

if __package__:
    from .asset_library import load_pack
else:
    from asset_library import load_pack

ROOT = Path(__file__).resolve().parents[1]
MEDIA = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.wav', '.mp3', '.m4a', '.ogg', '.flac', '.aac'}
TOPIC = 'assets/images/蛊真人/幽魂魔尊/manifest.json'
TOPICS = (TOPIC, 'assets/images/蛊真人/柳贯一/manifest.json',
          'assets/images/guzhenren/huzidashu/manifest.json',
          'assets/images/guzhenren/road/manifest.json',
          'assets/images/guzhenren/huanglongjiang/manifest.json',
          'assets/images/guzhenren/kaiqiaodadian/manifest.json',
          'assets/images/guzhenren/sanwangshan/manifest.json',
          'assets/images/donghua/fengyun/manifest.json',
          'assets/images/guzhenren/sanwangshan/v2/manifest.json',
          'assets/images/donghua/xinjing/manifest.json',
          'assets/images/guzhenren/huigu/manifest.json')


def safe(root, relative):
    """Reject traversal and every symlink component, including metadata files."""
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError('Unsafe repository-relative path')
    root = Path(root).resolve()
    result = root / relative
    result.resolve().relative_to(root)
    for part in (result, *result.parents):
        if part == root:
            break
        if part.is_symlink():
            raise ValueError('Symlink is not an audit input: ' + relative)
    return result


def audit(root=ROOT, topic_manifests=TOPICS):
    root = Path(root).resolve()
    errors = []
    expected = {}
    declarations = []
    modules = {}
    digests = {}
    audio = {}

    def read(relative):
        return json.loads(safe(root, relative).read_text(encoding='utf-8'))

    def declare(path, sha, size=None, image=None, source=None):
        safe(root, path)
        if not path.startswith('assets/') or Path(path).suffix.lower() not in MEDIA:
            raise ValueError('Declared file is not an assets media file: ' + path)
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in '0123456789abcdef' for c in sha):
            raise ValueError('Invalid SHA: ' + path)
        spec = dict(sha256=sha, bytes=size, image=image, source=source)
        declarations.append((path, spec))
        if path in expected and expected[path]['sha256'] != sha:
            errors.append('Conflicting declared SHA: ' + path)
        else:
            expected.setdefault(path, spec)

    def module(path, purpose, notice):
        safe(root, path)
        if not safe(root, notice).is_file():
            raise ValueError('Missing module notice: ' + notice)
        modules[path] = dict(purpose=purpose, notice=notice, files=0, bytes=0)

    try:
        ledger = read('assets/migration-20261028.json')
        if len(ledger['files']) != ledger['media_count'] or sum(x['bytes'] for x in ledger['files']) != ledger['total_bytes']:
            errors.append('Migration baseline totals do not match its entries')
        ledger_paths = [x['path'] for x in ledger['files']]
        if len(ledger_paths) != len(set(ledger_paths)):
            errors.append('Duplicate migration path')
        for item in ledger['files']:
            declare(item['path'], item['sha256'], item['bytes'], item.get('image'), 'migration-20261028')
        # Current declarations are cross-checks, never replacements for the frozen baseline.
        library = read('assets/images/catalog.json')
        if library.get('image_count') is not None and sum(x['image_count'] for x in library['packs']) != library['image_count']:
            errors.append('Image library catalog total mismatch')
        for pack in library['packs']:
            safe(root, 'assets/images/' + pack['manifest'])
            directory, _, manifest = load_pack(pack['id'], root)
            module(directory.relative_to(root).as_posix(), 'reusable images; inspect full images/parts/atlas',
                   (directory / 'README.md').relative_to(root).as_posix())
            if len(manifest['files']) != pack['image_count']:
                errors.append('Image pack count mismatch: ' + pack['id'])
            for item in manifest['files']:
                path = (directory / item['file']).relative_to(root).as_posix()
                declare(path, item['sha256'], image=dict(width=item['size'][0], height=item['size'][1], format='PNG'), source=pack['manifest'])
        harbor = read('assets/images/harbor/manifest.json')
        for name, item in harbor['files'].items():
            declare('assets/images/harbor/' + name, item['sha256'], image=dict(width=item['size'][0], height=item['size'][1], format='PNG'), source='harbor manifest')
        for topic_path in topic_manifests:
            topic = read(topic_path)
            if len(topic['files']) != topic['image_count'] or sum(x['bytes'] for x in topic['files']) != topic['total_bytes']:
                errors.append('Topic module totals do not match its entries')
            names = [x['file'] for x in topic['files']]
            if len(names) != len(set(names)):
                errors.append('Duplicate topic image path')
            for item in topic['files']:
                declare(str(Path(topic_path).parent / item['file']), item['sha256'], item['bytes'], item, topic_path)
            module(str(Path(topic_path).parent), 'user-provided images; reuse license NOT_SEPARATELY_DECLARED', str(Path(topic_path).parent / 'README.md'))
        comic = read('examples/reference-comic/manifest.json')
        for key in ('video', 'poster'):
            item = comic[key]
            # This existing case deliberately uses ../../assets paths; resolve then revalidate.
            unresolved = root / 'examples/reference-comic' / item['path']
            for part in (unresolved, *unresolved.parents):
                if part.is_symlink():
                    raise ValueError('Symlink in comic media reference')
            path = unresolved.resolve().relative_to(root).as_posix()
            declare(path, item['sha256'], item.get('bytes'), item if key == 'poster' else None, 'comic manifest')
        audio = read('assets/audio/pixel-rooftop/source.json')
        declare('assets/audio/pixel-rooftop/' + audio['file'], audio['sha256'], source='audio source.json')
        module('assets/images/harbor', 'reusable original pixel assets', 'assets/images/harbor/README.md')
        for name in ('pixel-rooftop', 'garden', 'library', 'reference-comic'):
            module('assets/images/' + name, 'showcase/preview; not layered source artwork', 'assets/images/README.md')
        for name in ('pixel-rooftop', 'reference-comic'):
            module('assets/videos/' + name, 'completed showcase; not editable shots/project', 'assets/videos/README.md')
        module('assets/audio/pixel-rooftop', 'reusable original music', 'assets/audio/pixel-rooftop/NOTICE.md')
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError) as exc:
        errors.append('Declaration error: ' + str(exc))

    actual = set()
    for path in (root / 'assets').rglob('*'):
        if path.suffix.lower() in MEDIA and (path.is_file() or path.is_symlink()):
            relative = path.relative_to(root).as_posix()
            actual.add(relative)
    errors.extend('Unregistered media: ' + x for x in sorted(actual - expected.keys()))
    errors.extend('Missing media: ' + x for x in sorted(expected.keys() - actual))
    total = 0
    for relative in sorted(actual):
        try:
            path = safe(root, relative)
            content = path.read_bytes()
            total += len(content)
            digest = hashlib.sha256(content).hexdigest()
            digests.setdefault(digest, []).append(relative)
            key = path.parent.relative_to(root).as_posix()
            if key not in modules:
                errors.append('Unregistered module: ' + key)
            else:
                modules[key]['files'] += 1
                modules[key]['bytes'] += len(content)
            for declared_path, spec in declarations:
                if declared_path != relative:
                    continue
                if digest != spec['sha256']:
                    errors.append('SHA mismatch: ' + relative + ' (' + spec['source'] + ')')
                if spec['bytes'] is not None and spec['bytes'] != len(content):
                    errors.append('Byte count mismatch: ' + relative)
                if spec['image']:
                    with Image.open(path) as im:
                        dimensions = spec['image']
                        if [im.width, im.height] != [dimensions['width'], dimensions['height']]:
                            errors.append('Image dimensions mismatch: ' + relative)
                        if dimensions.get('frames') is not None and getattr(im, 'n_frames', 1) != dimensions['frames']:
                            errors.append('Image frame count mismatch: ' + relative)
                        if dimensions.get('format') and im.format != dimensions['format']:
                            errors.append('Image format mismatch: ' + relative)
            if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
                with Image.open(path) as im:
                    for frame in range(getattr(im, 'n_frames', 1)):
                        im.seek(frame)
                        im.load()
            elif path.suffix.lower() == '.wav':
                with wave.open(str(path), 'rb') as wav:
                    if (wav.getframerate(), wav.getnchannels(), wav.getnframes()) != (audio['sample_rate'], audio['channels'], round(audio['duration'] * audio['sample_rate'])):
                        errors.append('WAV source metadata mismatch: ' + relative)
        except (OSError, ValueError, KeyError, TypeError, wave.Error, EOFError) as exc:
            errors.append(relative + ': ' + type(exc).__name__ + ': ' + str(exc))
    return dict(status='FAIL' if errors else 'PASS', files=len(actual), bytes=total,
                modules=modules, duplicates=[v for v in digests.values() if len(v) > 1], errors=errors,
                coverage='Current baseline/module SHA and sizes, image frame decode/dimensions, WAV header; MP4 byte identity only. Not video/audio full decode, rights clearance or artistic approval.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    result = audit(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result['status'] != 'PASS'


if __name__ == '__main__':
    raise SystemExit(main())
