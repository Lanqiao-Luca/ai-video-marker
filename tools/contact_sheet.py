"""Extract actual encoded frames into a NEW contact sheet directory."""
import argparse
import json
from pathlib import Path
import sys
from PIL import Image,ImageDraw
from media import extract_frame,ffmpeg_path,probe,sha256


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video',type=Path)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--times',type=float,nargs='+')
    parser.add_argument('--ffmpeg')
    args=parser.parse_args();exe=ffmpeg_path(args.ffmpeg);info=probe(args.video,exe)
    if not info['has_video'] or not info['duration']:raise ValueError('Readable video duration required.')
    times=args.times or [info['duration']*v for v in (.02,.12,.24,.36,.5,.65,.78,.9,.98)]
    if any(not 0<=v<info['duration'] for v in times):raise ValueError('Sample times must lie inside the video.')
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=False)
    width=320;height=round(width*info['height']/info['width']);cols=3
    sheet=Image.new('RGB',(width*cols,(height+23)*((len(times)+cols-1)//cols)),'#17262a');draw=ImageDraw.Draw(sheet)
    for k,t in enumerate(times):
        p=out/f'frame-{k:02d}.png';extract_frame(args.video,t,p,exe)
        with Image.open(p) as im:thumb=im.convert('RGB').resize((width,height),Image.Resampling.NEAREST)
        x=(k%cols)*width;y=(k//cols)*(height+23)
        sheet.paste(thumb,(x,y));draw.text((x+5,y+height+4),f'{t:.2f}s',fill='white')
    sheet.save(out/'contact-sheet.png')
    (out/'samples.json').write_text(json.dumps(dict(video_sha256=sha256(args.video),times=times,
        coverage='encoded static samples only; not real-time review'),indent=2)+'\n',encoding='utf-8')
    print(out/'contact-sheet.png')


if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,OSError) as exc:
        print('ERROR:',exc,file=sys.stderr);raise SystemExit(1)
