"""Make a distinct first video with bundled assets; no AI/API calls required."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import secrets
import sys
import tempfile

from garden_drawing import PALETTES,validate_garden
from harbor_drawing import PALETTES as HARBOR_PALETTES,validate_harbor
from render_pixel import main as render

ROOT=Path(__file__).resolve().parents[1]


def make_scene(seed,palette,theme='garden'):
    config=ROOT/('examples/harbor/scene.json' if theme=='harbor' else 'examples/first-video/scene.json')
    scene=json.loads(config.read_text(encoding='utf-8'))
    scene.update(seed=seed,palette=palette)
    return validate_harbor(scene) if theme=='harbor' else validate_garden(scene)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,help='NEW output directory; default is outputs/first-video-TIMESTAMP-SEED.')
    parser.add_argument('--seed',type=int,help='Recorded variation seed. Omit for a fresh arrangement.')
    parser.add_argument('--theme',choices=['harbor','garden'],default='harbor')
    parser.add_argument('--palette',choices=sorted(set(PALETTES)|set(HARBOR_PALETTES)))
    parser.add_argument('--list',action='store_true',help='List runnable stories and asset kits without rendering.')
    parser.add_argument('--start',type=float,default=0)
    parser.add_argument('--end',type=float)
    sound=parser.add_mutually_exclusive_group()
    sound.add_argument('--audio',type=Path)
    sound.add_argument('--silent',action='store_true')
    parser.add_argument('--ffmpeg')
    a=parser.parse_args(argv)
    if a.list:
        print(json.dumps({'default':'harbor','stories':[
            {'theme':'harbor','title':'小机器人与归航灯塔','character':'robot','duration':36,'assets':'assets/images/harbor','palettes':list(HARBOR_PALETTES)},
            {'theme':'garden','title':'月光风铃','character':'rabbit','duration':32,'palettes':list(PALETTES)},
            {'theme':'rooftop','title':'屋顶晒太阳','character':'rabbit','duration':44,'command':'python tools/render_pixel.py'}]},ensure_ascii=False,indent=2))
        return
    seed=secrets.randbelow(2**32) if a.seed is None else a.seed
    palette=a.palette or ('sunset' if a.theme=='harbor' else 'moon')
    scene=make_scene(seed,palette,a.theme)
    # Caller owns the output location, even when this script is installed elsewhere.
    out=(a.out or Path('outputs')/('first-video-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+str(seed))).expanduser().resolve()
    print(json.dumps({'starter':scene['title'],'theme':a.theme,'seed':seed,'palette':palette,
                      'variation_scope':'fixed story; seed changes water glints in harbor, star/flower positions in garden',
                      'ai_api_calls':0},ensure_ascii=False),flush=True)
    with tempfile.TemporaryDirectory(prefix='ai-video-scene-') as temporary:
        config=Path(temporary)/'scene.json';config.write_text(json.dumps(scene,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        duration=(scene['duration'] if a.end is None else a.end)-a.start
        args=['--scene',str(config),'--out',str(out),'--start',str(a.start),
              '--audio-fade-out',str(min(.8,duration/2))]
        if a.end is not None:args+=['--end',str(a.end)]
        if a.silent:args+=['--silent']
        if a.audio:args+=['--audio',str(a.audio)]
        if a.ffmpeg:args+=['--ffmpeg',a.ffmpeg]
        render(args)


if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,OSError,KeyError,TypeError) as exc:
        print('ERROR:',exc,file=sys.stderr);raise SystemExit(1)
