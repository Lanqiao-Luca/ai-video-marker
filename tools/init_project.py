"""Create a new production directory using one catalog route, without overwriting."""
import argparse
import json
from pathlib import Path
import re
import shutil
import sys

ROOT=Path(__file__).resolve().parents[1]


def create(route_id,project_id,out,asset_mode=None):
    if asset_mode not in (None,'reuse','mixed','generate'):raise ValueError('Unknown asset mode.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',project_id):
        raise ValueError('Project ID needs 1..64 ASCII letters/digits/underscore/hyphen.')
    catalog=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))
    route=next((r for r in catalog['routes'] if r['id']==route_id),None)
    if not route:raise ValueError('Unknown workflow route.')
    out=out.expanduser().resolve()
    if out.exists():raise FileExistsError('Project directory already exists.')
    shutil.copytree(ROOT/'templates/project',out,ignore=shutil.ignore_patterns('README.md'))
    state=json.loads((out/'status.json').read_text(encoding='utf-8'))
    state.update(project_id=project_id,workflow=route_id,workflow_status=route['status'],asset_strategy=asset_mode)
    if asset_mode is None:state['next_action']='Confirm reuse, mixed or generate asset strategy before new asset production.'
    (out/'status.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if route_id=='pixel':shutil.copytree(ROOT/'templates/pixel',out/'worksheets',ignore=shutil.ignore_patterns('README.md'))
    if route_id=='painting-world':
        shutil.copy2(ROOT/'templates/绘画世界穿行制作单.md',out/'painting-world-brief.md')
    if route_id=='reference-comic':
        shutil.copy2(ROOT/'templates/参考音轨与AI漫画制作单.md',out/'reference-comic-brief.md')
    if route_id=='blender-layered':
        shutil.copy2(ROOT/'templates/Blender分层角色动画制作单.md',out/'blender-layered-brief.md')
    (out/'README.md').write_text('**目的**：定位本作当前状态与必要输入。\n\n# '+project_id+
        '\n\n制作路线：'+route['name']+'（'+route['status']+'）。\n\n填写 brief.md 和 shots.csv；实际进度见 status.json，反馈见 feedback.md。\n'+
        '本目录仅完成初始化，尚未制作视频或取得用户采用。\n',encoding='utf-8')
    return dict(project_id=project_id,workflow=route_id,status='INITIALIZED',output=str(out))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--route',required=True);parser.add_argument('--id',required=True)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--assets',choices=['reuse','mixed','generate'])
    a=parser.parse_args();print(json.dumps(create(a.route,a.id,a.out,a.assets),ensure_ascii=False,indent=2))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as exc:
        print('ERROR:',exc,file=sys.stderr);raise SystemExit(1)
