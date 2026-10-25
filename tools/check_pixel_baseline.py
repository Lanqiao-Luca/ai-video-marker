"""Compare every pre-encode RGB frame against the preserved source fixture."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
from pixel_engine import PixelRenderer,load_scene

ROOT=Path(__file__).resolve().parents[1]


def verify(scene_path,baseline_path):
    scene=load_scene(scene_path);data=json.loads(baseline_path.read_text(encoding='utf-8'))
    drawing=ast.parse((ROOT/'tools/pixel_drawing.py').read_text(encoding='utf-8'))
    names=data['drawing_function_names']
    funcs={node.name:node for node in drawing.body if isinstance(node,ast.FunctionDef)}
    fingerprint=hashlib.sha256('\n'.join(ast.dump(funcs[name],include_attributes=False) for name in names).encode()).hexdigest()
    renderer=PixelRenderer(scene);mismatches=[]
    same_spec=(scene['fps']==data['fps'] and scene['output_size']==data['size'] and round(scene['duration']*scene['fps'])==data['frames'])
    if not same_spec:raise ValueError('Scene specification differs from the frozen source baseline.')
    for index,expected in enumerate(data['frame_rgb_sha256']):
        image,_=renderer.frame(index/data['fps'])
        if hashlib.sha256(image.tobytes()).hexdigest()!=expected:mismatches.append(index)
    return dict(status='PASS' if not mismatches and fingerprint==data['source_drawing_ast_sha256'] else 'FAIL',
        source_work=data['source_work'],frames_checked=data['frames'],mismatched_frames=mismatches,
        source_drawing_functions_unchanged=fingerprint==data['source_drawing_ast_sha256'],
        coverage='all original RGB drawing frames before video encoding; not audio or artistic adoption',
        baseline_sha256=hashlib.sha256(baseline_path.read_bytes()).hexdigest())


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene',type=Path,default=ROOT/'examples/pixel/scene.json')
    parser.add_argument('--baseline',type=Path,default=ROOT/'examples/pixel/source-frame-baseline.json')
    parser.add_argument('--out',type=Path)
    a=parser.parse_args()
    if a.out and a.out.exists():raise FileExistsError('Report already exists.')
    result=verify(a.scene,a.baseline)
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        with a.out.open('x',encoding='utf-8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,RuntimeError,OSError,KeyError) as exc:
        print('ERROR:',exc,file=sys.stderr);raise SystemExit(1)
