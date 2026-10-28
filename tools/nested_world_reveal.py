"""Continuous nested planar reveals, sampling each original layer once.

Sibling painted_world_reveal supplies the existing RGB/quad validators. This
module adds a timeline and nested composition without changing that API.
Images must already share an explicitly prepared canvas. No image generation,
resizing, music, captions, installation, or application-project writes occur.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import cv2
import numpy as np

if __package__:
    from .painted_world_reveal import _rgb, _quad, _homography
else:
    from painted_world_reveal import _rgb, _quad, _homography


class NestedWorldReveal:
    """Layers are ordered inner to outer; event i inserts layer i into i+1.

    ``quad`` coordinates refer to the prepared common canvas, TL/TR/BR/BL.
    A provider(i, t) may supply per-layer live RGB pixels. It must retain the
    same canvas and source identity; effects are then projected with that layer.
    Outputs are float32 RGB [0,1]. Inputs are never mutated.
    """

    def __init__(self, images, events):
        if len(images) < 2 or len(events) != len(images) - 1:
            raise ValueError("Require N >= 2 images and exactly N-1 reveal events")
        self.images = tuple(_rgb(im, f"image[{i}]").copy() for i, im in enumerate(images))
        shape = self.images[0].shape
        if any(im.shape != shape for im in self.images):
            raise ValueError("Prepare all images to one canvas explicitly; no implicit stretching")
        self.height, self.width = shape[:2]
        self.rect = np.float32([[0, 0], [self.width-1, 0],
                               [self.width-1, self.height-1], [0, self.height-1]])
        self.events = []
        self.insertions = []
        previous_end = 0.0
        for i, event in enumerate(events):
            start, end = float(event['start']), float(event['end'])
            if not all(math.isfinite(x) for x in (start, end)) or start < previous_end or end <= start:
                raise ValueError("Reveal times must be finite, nonnegative, ordered and nonoverlapping")
            quad = _quad(event['quad'], self.width, self.height)
            self.events.append((start, end, quad.copy()))
            self.insertions.append(_homography(self.rect, quad))
            previous_end = end
        self.alpha = np.ones(shape[:2], np.float32)

    def state(self, t):
        t = float(t)
        if not math.isfinite(t) or t < 0:
            raise ValueError("time must be finite and nonnegative")
        for i, (start, end, quad) in enumerate(self.events):
            if t < start:
                return i, np.eye(3)
            if t < end:
                u = (t-start)/(end-start)
                eased = u*u*u*(u*(u*6-15)+10)
                target = self.rect*(1-eased) + quad*eased
                return i+1, _homography(quad, target)
        return len(self.events), np.eye(3)

    def frame(self, t, layer_provider=None):
        top, view = self.state(t)

        def layer(i):
            if layer_provider is None:
                return self.images[i]
            rgb = _rgb(layer_provider(i, float(t)), f"live layer[{i}]")
            if rgb.shape != self.images[i].shape:
                raise ValueError("Live layer must retain its prepared canvas dimensions")
            return rgb

        out = cv2.warpPerspective(layer(top), view, (self.width, self.height),
                                  flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        mapping = view
        for i in range(top-1, -1, -1):
            # Do NOT shrink a precomposed picture into a tiny carrier and then
            # enlarge it. Accumulate transforms, sample original pixels once.
            mapping = mapping @ self.insertions[i]
            rgb = cv2.warpPerspective(layer(i), mapping, (self.width, self.height),
                                      flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            alpha = cv2.warpPerspective(self.alpha, mapping, (self.width, self.height),
                                        flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            # Warped RGB already contains coverage; don't multiply it twice.
            out = out*(1-alpha[:, :, None]) + rgb
        return np.clip(out, 0, 1).astype(np.float32, copy=False)


def load_cue(path):
    path = Path(path).resolve()
    cue = json.loads(path.read_text())
    width, height = cue['canvas_size']
    if any(type(v) is not int or v < 2 for v in (width, height)):
        raise ValueError("canvas_size must be two integer pixel dimensions >= 2")
    fps, duration = float(cue['fps']), float(cue['duration'])
    if not all(math.isfinite(v) and v > 0 for v in (fps, duration)):
        raise ValueError("fps and duration must be positive and finite")
    if abs(duration*fps-round(duration*fps)) > 1e-6:
        raise ValueError("duration must represent a whole number of frames at fps")
    images, sources = [], []
    for name in cue['assets']:
        source = (path.parent / name).resolve()
        pixels = cv2.imread(str(source), cv2.IMREAD_UNCHANGED)
        if pixels is None:
            raise ValueError(f"Unable to read asset: {source}")
        if pixels.shape != (height, width, 3) or pixels.dtype != np.uint8:
            raise ValueError(f"{source}: require prepared {width}x{height} 8-bit RGB; record crop/fit before rendering")
        images.append(cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB))
        sources.append({'path': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    renderer = NestedWorldReveal(images, cue['reveals'])
    if renderer.events[-1][1] > duration:
        raise ValueError("Last reveal ends beyond video duration")
    return cue, renderer, sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cue', required=True, type=Path)
    parser.add_argument('--output', type=Path, help='new silent MP4 path; never overwritten')
    parser.add_argument('--ffmpeg', default='ffmpeg', help='executable name or explicit path')
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--start', type=float, default=0.0, help='probe interval start in full cue time')
    parser.add_argument('--end', type=float, help='probe interval end in full cue time')
    args = parser.parse_args()
    cue, renderer, sources = load_cue(args.cue)
    if args.check_only:
        print(json.dumps({'input_contract': 'PASS', 'layers': len(sources), 'reveals': len(renderer.events),
                          'visual_review': 'NOT_RUN', 'sources': sources}, ensure_ascii=False))
        return
    if args.output is None:
        parser.error('--output is required unless --check-only')
    start, end, fps = args.start, args.end if args.end is not None else float(cue['duration']), float(cue['fps'])
    if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end <= float(cue['duration'])):
        parser.error('probe interval must lie inside cue duration')
    if any(abs(t*fps-round(t*fps)) > 1e-6 for t in (start, end)):
        parser.error('probe endpoints must be aligned to the output frame grid')
    output = args.output.resolve()
    record_path = output.with_suffix('.render.json')
    if renderer.width % 2 or renderer.height % 2:
        raise ValueError('H.264 yuv420p output requires an even prepared canvas width and height')
    if output.exists() or record_path.exists():
        raise FileExistsError('Choose new output and record paths; existing files are preserved')
    if not output.parent.is_dir():
        raise FileNotFoundError('Create an authorized output directory before rendering')
    frames = round((end-start)*fps)
    command = [args.ffmpeg, '-hide_banner', '-nostdin', '-loglevel', 'error', '-n',
               '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{renderer.width}x{renderer.height}',
               '-r', str(fps), '-i', 'pipe:0', '-an',
               '-vf', 'scale=in_range=full:out_range=tv:out_color_matrix=bt709',
               '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
               '-color_range', 'tv', '-color_primaries', 'bt709', '-color_trc', 'iec61966-2-1',
               '-colorspace', 'bt709', '-movflags', '+faststart', str(output)]
    cv2.setNumThreads(1)
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for i in range(frames):
            process.stdin.write(np.rint(renderer.frame(start+i/fps)*255).astype(np.uint8).tobytes())
        process.stdin.close()
        if process.wait() != 0:
            raise RuntimeError('ffmpeg failed; any partial output is not a valid delivery')
    except BaseException:
        process.kill()
        process.wait()
        raise
    record = {'output': str(output), 'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'cue': str(args.cue.resolve()), 'cue_sha256': hashlib.sha256(args.cue.read_bytes()).hexdigest(),
              'implementation_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'validator_sha256': hashlib.sha256(Path(__file__).with_name('painted_world_reveal.py').read_bytes()).hexdigest(),
              'sources': sources, 'fps': fps, 'requested_frames': frames, 'source_interval': [start, end],
              'method': 'single-sample nested planar reveal; static source layers',
              'audio': 'NONE; preserve music speed in downstream finishing',
              'encoded_decode_check': 'NOT_RUN', 'normal_speed_visual_review': 'NOT_RUN',
              'owner_adoption': 'PENDING'}
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2))
    print(json.dumps(record, ensure_ascii=False))


if __name__ == '__main__':
    main()
