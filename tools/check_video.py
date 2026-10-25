"""Read stream headers and completely decode a video; report only actual coverage."""
import argparse
import json
from pathlib import Path
import sys
from media import decode_audio,decode_frames,ffmpeg_path,probe,sha256


def inspect(video,ffmpeg,expected=None):
    actual=probe(video,ffmpeg)
    errors=[]
    if not actual['has_video']:raise ValueError('No video stream.')
    actual['decoded_frames']=decode_frames(video,ffmpeg)
    if actual['has_audio']:
        decode_audio(video,ffmpeg)
        actual['audio_decode']='PASS'
    else:actual['audio_decode']='NOT_PRESENT'
    expected=expected or {}
    for key in ('width','height'):
        if key in expected and actual[key]!=expected[key]:errors.append(f'{key}: expected {expected[key]}, got {actual[key]}')
    if 'frames' in expected and actual['decoded_frames']!=expected['frames']:
        errors.append(f'frames: expected {expected["frames"]}, got {actual["decoded_frames"]}')
    if 'fps' in expected and (actual['fps'] is None or abs(actual['fps']-expected['fps'])>.01):errors.append('Frame rate mismatch.')
    if 'duration' in expected and (actual['duration'] is None or abs(actual['duration']-expected['duration'])>.1):errors.append('Duration mismatch.')
    if 'audio' in expected and actual['has_audio']!=expected['audio']:errors.append('Audio presence mismatch.')
    return dict(status='PASS' if not errors else 'FAIL',video_sha256=sha256(video),actual=actual,errors=errors,
        coverage='stream headers and complete video decode; complete audio decode when present',
        full_realtime_review='NOT_RUN',audio_listening='NOT_RUN',adoption='PENDING')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video',type=Path)
    parser.add_argument('--manifest',type=Path)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--ffmpeg')
    args=parser.parse_args()
    if args.out and args.out.exists():raise FileExistsError('Report already exists; choose a new path.')
    expected={};manifest=None
    if args.manifest:
        manifest=json.loads(args.manifest.read_text(encoding='utf-8'))
        if manifest.get('status')!='RENDERED':raise ValueError('Manifest is not a completed render.')
        if manifest.get('video_sha256')!=sha256(args.video):raise ValueError('Video SHA does not match the render manifest.')
        expected=manifest['expected']
    result=inspect(args.video,ffmpeg_path(args.ffmpeg),expected)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        with args.out.open('x',encoding='utf-8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,RuntimeError,OSError,KeyError) as exc:
        print('ERROR:',exc,file=sys.stderr);raise SystemExit(1)
