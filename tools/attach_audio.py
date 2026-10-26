"""Attach user-provided audio to a video without re-encoding its picture."""
import argparse
import json
import math
from pathlib import Path
import sys
from media import ffmpeg_path,probe,run,sha256


def attach(video,audio,output,offset,ffmpeg,fade_out=0):
    output=output.resolve();report=output.with_suffix('.source.json')
    if output.exists() or report.exists():raise FileExistsError('Output or source report already exists.')
    if not math.isfinite(offset) or offset<0:raise ValueError('Offset must be finite and nonnegative.')
    v=probe(video,ffmpeg);a=probe(audio,ffmpeg)
    if not v['has_video'] or not v['duration'] or not a['has_audio'] or not a['duration']:
        raise ValueError('Readable video and audio durations required.')
    if a['duration']-offset < v['duration']-.05:
        raise ValueError('Audio segment is shorter than video; provide a longer segment. No implicit looping.')
    if not math.isfinite(fade_out) or not 0<=fade_out<=v['duration']:
        raise ValueError('Audio fade must be finite and within the video duration.')
    output.parent.mkdir(parents=True,exist_ok=True)
    filters=['-af',f'afade=t=out:st={v["duration"]-fade_out}:d={fade_out}'] if fade_out else []
    run([ffmpeg,'-v','error','-nostdin','-n','-i',video,'-ss',str(offset),'-i',audio,
         '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k',
         *filters,'-t',str(v['duration']),'-movflags','+faststart',output])
    data=dict(video_sha256=sha256(video),audio_sha256=sha256(audio),source_start=offset,
              source_end=offset+v['duration'],output_sha256=sha256(output),
              processing='video stream copy; AAC audio encoding; no loudness normalization',audio_fade_out=fade_out,
              licensing='user-provided; tool does not infer rights',audio_listening='NOT_RUN',adoption='PENDING')
    with report.open('x',encoding='utf-8') as stream:json.dump(data,stream,ensure_ascii=False,indent=2);stream.write('\n')
    return data


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video',type=Path);parser.add_argument('audio',type=Path)
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--offset',type=float,default=0)
    parser.add_argument('--ffmpeg')
    a=parser.parse_args();print(json.dumps(attach(a.video,a.audio,a.out,a.offset,ffmpeg_path(a.ffmpeg)),indent=2))


if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,OSError) as exc:
        print('ERROR:',exc,file=sys.stderr);raise SystemExit(1)
