"""Render a supported pixel scene into a NEW output directory."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import sys
from media import ffmpeg_path,probe,sha256
from attach_audio import attach
from pixel_engine import PixelRenderer,load_scene

ROOT=Path(__file__).resolve().parents[1]


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene',type=Path,default=ROOT/'examples/pixel/scene.json')
    parser.add_argument('--out',type=Path,default=ROOT/'outputs/pixel-rooftop')
    parser.add_argument('--start',type=float,default=0)
    parser.add_argument('--end',type=float)
    parser.add_argument('--ffmpeg')
    sound=parser.add_mutually_exclusive_group()
    sound.add_argument('--audio',type=Path,help='Use this audio file instead of the bundled example track.')
    sound.add_argument('--silent',action='store_true',help='Render a silent master without reading any audio file.')
    parser.add_argument('--audio-offset',type=float,default=0,help='Source audio start; subclip start is added automatically.')
    parser.add_argument('--audio-fade-out',type=float,default=0,help='Optional audio fade duration at clip end.')
    args=parser.parse_args(argv)
    raw=json.loads(args.scene.read_text(encoding='utf-8'))
    if raw.get('id')=='moonlight-chimes':
        from garden_drawing import GardenRenderer,validate_garden
        scene=validate_garden(raw);renderer=GardenRenderer(scene)
        drawing=ROOT/'tools/garden_drawing.py'
    else:
        scene=load_scene(args.scene);renderer=PixelRenderer(scene)
        drawing=ROOT/'tools/pixel_drawing.py'
    start=args.start;end=scene['duration'] if args.end is None else args.end;fps=scene['fps']
    if not math.isfinite(start) or not math.isfinite(end) or not 0<=start<end<=scene['duration']:
        raise ValueError('Need 0 <= start < end <= scene duration.')
    if any(abs(v*fps-round(v*fps))>1e-6 for v in (start,end)):
        raise ValueError('Start and end must fall on exact frame boundaries.')
    exe=ffmpeg_path(args.ffmpeg)
    bundled=not args.silent and args.audio is None
    audio=None if args.silent else (args.audio or ROOT/'examples/pixel/audio/music.wav')
    if not math.isfinite(args.audio_offset) or args.audio_offset<0:
        raise ValueError('Audio offset must be finite and nonnegative.')
    if not math.isfinite(args.audio_fade_out) or not 0<=args.audio_fade_out<=end-start:
        raise ValueError('Audio fade must be finite and within the clip duration.')
    if audio is not None:
        if not audio.is_file():raise ValueError('Audio missing. Supply --audio FILE or use --silent.')
        if bundled:
            record=json.loads((ROOT/'examples/pixel/audio/source.json').read_text(encoding='utf-8'))
            if sha256(audio)!=record['sha256']:raise ValueError('Bundled audio SHA mismatch.')
        audio_info=probe(audio,exe)
        if not audio_info['has_audio'] or audio_info['duration'] is None or audio_info['duration']<args.audio_offset+end-.05:
            raise ValueError('Audio does not cover the requested segment; provide a longer file or use --silent.')
    out=args.out.expanduser().resolve();out.mkdir(parents=True,exist_ok=False)
    width,height=scene['output_size'];count=round((end-start)*fps)
    video=out/'video.mp4';master=out/'silent.mp4' if audio is not None else video;partial=out/'video.partial.mp4'
    identity=dict(schema_version=1,project='ai-video-marker',example=scene['id'],status='RUNNING',
        source_work=scene['work_id'],scene_sha256=sha256(args.scene),renderer_sha256=sha256(Path(__file__)),
        engine_sha256=sha256(ROOT/'tools/pixel_engine.py'),drawing_sha256=sha256(drawing),
        shared_assets_sha256=sha256(ROOT/'tools/pixel_drawing.py'),
        expected=dict(width=width,height=height,fps=fps,frames=count,duration=count/fps,audio=audio is not None),
        source_start=start,source_end=end,adoption='PENDING',
        music_status='BUNDLED_PROJECT_ORIGINAL' if bundled else ('USER_PROVIDED' if audio is not None else 'SILENT'),
        audio_sha256=sha256(audio) if audio is not None else None,
        audio_source_start=args.audio_offset+start if audio is not None else None,
        audio_fade_out=args.audio_fade_out if audio is not None else None,
        music_redistribution=record['redistribution_status'] if bundled else 'NOT_INFERRED',full_realtime_review='NOT_RUN')
    def save():
        (out/'run.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    save()
    command=[exe,'-hide_banner','-v','error','-nostdin','-n','-f','rawvideo','-vcodec','rawvideo',
        '-pix_fmt','rgb24','-s',f'{width}x{height}','-r',str(fps),'-i','pipe:0','-an',
        '-vf','scale=in_range=full:out_range=limited:out_color_matrix=bt709,format=yuv420p',
        '-c:v','libx264','-preset','fast','-crf','17','-colorspace','bt709',
        '-color_primaries','bt709','-color_trc','iec61966-2-1','-color_range','tv',
        '-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=13:matrix_coefficients=1:video_full_range_flag=0',
        '-movflags','+faststart',str(partial)]
    trace=[]
    try:
        with (out/'render.log').open('w',encoding='utf-8') as log:
            proc=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=log)
            try:
                for index in range(count):
                    image,observed=renderer.frame(start+index/fps)
                    proc.stdin.write(image.tobytes());trace.append(observed)
                    if index in (0,count//2,count-1):image.save(out/f'frame-{index:04d}.png')
                proc.stdin.close();code=proc.wait()
            except BaseException:
                if proc.poll() is None:proc.kill()
                proc.wait();raise
        if code:raise RuntimeError(f'FFmpeg failed ({code}); see render.log')
        partial.rename(master)
        if audio is not None:attach(master,audio,video,args.audio_offset+start,exe,fade_out=args.audio_fade_out)
        (out/'scene.json').write_text(json.dumps(scene,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (out/'trace.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        identity.update(status='RENDERED',video='video.mp4',video_sha256=sha256(video));save()
        print(json.dumps(dict(output=str(out),frames=count,source_work=scene['work_id'],
            audio='bundled project-original track' if bundled else ('user-provided' if audio is not None else 'silent')),ensure_ascii=False,indent=2))
    except BaseException as exc:
        identity.update(status='FAILED',error=str(exc));save();raise


if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,OSError,KeyError,TypeError) as exc:
        print('ERROR:',exc,file=sys.stderr);raise SystemExit(1)
