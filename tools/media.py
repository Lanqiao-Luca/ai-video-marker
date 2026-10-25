"""Small FFmpeg adapter shared by rendering and verification. No shell invocation."""
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def ffmpeg_path(explicit=None):
    candidate = explicit or os.environ.get('FFMPEG_BINARY') or shutil.which('ffmpeg')
    if not candidate:
        try:
            import imageio_ffmpeg
            candidate = imageio_ffmpeg.get_ffmpeg_exe()
        except (ImportError, RuntimeError) as exc:
            raise RuntimeError('FFmpeg unavailable: install requirements.txt or pass --ffmpeg.') from exc
    resolved = shutil.which(str(candidate)) or str(Path(candidate).expanduser().resolve())
    if not Path(resolved).is_file():
        raise ValueError('FFmpeg executable does not exist: ' + resolved)
    return resolved


def run(args):
    result = subprocess.run([str(x) for x in args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-6000:])
    return result


def probe(path, ffmpeg):
    """Read actual FFmpeg stream headers; ffprobe is optional, not required."""
    result = subprocess.run([ffmpeg, '-hide_banner', '-i', str(path)],
                            capture_output=True, text=True)
    log = result.stderr
    if 'Input #0' not in log:
        raise ValueError('Unable to read media: ' + log[-2000:])
    duration = re.search(r'Duration: (\d+):(\d+):(\d+(?:\.\d+)?)', log)
    seconds = (int(duration[1]) * 3600 + int(duration[2]) * 60 + float(duration[3])) if duration else None
    video_line = next((line for line in log.splitlines() if 'Stream #' in line and 'Video:' in line), '')
    audio_line = next((line for line in log.splitlines() if 'Stream #' in line and 'Audio:' in line), '')
    size = re.search(r'\b(\d{2,5})x(\d{2,5})\b', video_line)
    fps = re.search(r'(\d+(?:\.\d+)?) fps', video_line)
    return dict(duration=seconds, width=int(size[1]) if size else None,
                height=int(size[2]) if size else None, fps=float(fps[1]) if fps else None,
                has_video=bool(video_line), has_audio=bool(audio_line),
                video_stream=video_line.strip(), audio_stream=audio_line.strip())


def decode_frames(path, ffmpeg):
    result = run([ffmpeg, '-v', 'error', '-nostdin', '-i', path, '-map', '0:v:0',
                  '-an', '-progress', 'pipe:1', '-nostats', '-f', 'null', '-'])
    counts = re.findall(r'^frame=(\d+)$', result.stdout, re.M)
    if not counts or 'progress=end' not in result.stdout:
        raise RuntimeError('Full decode produced no completed frame count.')
    if result.stderr.strip():
        raise RuntimeError('Decoder reported errors: ' + result.stderr[-2000:])
    return int(counts[-1])


def extract_frame(path, second, output, ffmpeg):
    run([ffmpeg, '-v', 'error', '-nostdin', '-n', '-ss', str(second), '-i', path,
         '-frames:v', '1', str(output)])


def decode_audio(path, ffmpeg):
    result=run([ffmpeg,'-v','error','-nostdin','-i',path,'-map','0:a:0','-vn','-f','null','-'])
    if result.stderr.strip():raise RuntimeError('Audio decoder reported errors: '+result.stderr[-2000:])
