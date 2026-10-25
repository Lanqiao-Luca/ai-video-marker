"""Check the current environment without installing packages or contacting services."""
import argparse
import importlib.metadata
import json
import platform
import sys
from media import ffmpeg_path, run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ffmpeg')
    args = parser.parse_args()
    rows = [dict(name='Python', ok=sys.version_info >= (3, 9), detail=platform.python_version())]
    for name in ('Pillow', 'imageio-ffmpeg'):
        try:
            rows.append(dict(name=name, ok=True, detail=importlib.metadata.version(name)))
        except importlib.metadata.PackageNotFoundError:
            # imageio-ffmpeg is only needed when no system FFmpeg is available.
            rows.append(dict(name=name, ok=name == 'imageio-ffmpeg',
                             detail='Not installed; system FFmpeg can be used' if name == 'imageio-ffmpeg' else 'Missing'))
    try:
        exe = ffmpeg_path(args.ffmpeg)
        version = run([exe, '-version']).stdout.splitlines()[0]
        encoders = run([exe, '-hide_banner', '-encoders']).stdout
        rows.append(dict(name='FFmpeg/libx264', ok='libx264' in encoders, detail=version))
    except (OSError, ValueError, RuntimeError) as exc:
        rows.append(dict(name='FFmpeg/libx264', ok=False, detail=str(exc)))
    print(json.dumps(dict(platform=platform.system(), checks=rows), ensure_ascii=False, indent=2))
    return 0 if all(row['ok'] for row in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
