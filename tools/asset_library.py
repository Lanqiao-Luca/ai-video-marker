"""List, verify or preview the bundled reusable still-image library, offline."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from PIL import Image,ImageDraw,ImageOps

ROOT=Path(__file__).resolve().parents[1]


def child(base,relative):
    relative=Path(relative)
    if relative.is_absolute() or '..' in relative.parts:raise ValueError('Library paths must be relative and stay inside the library.')
    target=base/relative
    if target.is_symlink():raise ValueError('Library symlinks are not supported.')
    target.resolve().relative_to(base.resolve())
    return target


def catalog(root=ROOT):
    base=Path(root)/'assets/images';data=json.loads((base/'catalog.json').read_text(encoding='utf-8'))
    ids=[]
    for pack in data['packs']:
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}',pack['id']):raise ValueError('Invalid library pack ID.')
        ids.append(pack['id']);child(base,pack['manifest'])
    if len(set(ids))!=len(ids):raise ValueError('Duplicate library pack ID.')
    return base,data


def load_pack(pack_id,root=ROOT):
    base,data=catalog(root);pack=next((p for p in data['packs'] if p['id']==pack_id),None)
    if pack is None:raise ValueError('Unknown library pack: '+pack_id)
    path=child(base,pack['manifest']);manifest=json.loads(path.read_text(encoding='utf-8'))
    if manifest['id']!=pack_id:raise ValueError('Catalog/manifest identity mismatch.')
    if manifest['license']!=data['license']:raise ValueError('Catalog/manifest license mismatch.')
    for f in manifest['files']:child(path.parent,f['file'])
    return path.parent,pack,manifest


def verify(root=ROOT,pack_id=None):
    _,data=catalog(root);selected=[p for p in data['packs'] if pack_id is None or p['id']==pack_id]
    if not selected:raise ValueError('Unknown library pack: '+str(pack_id))
    errors=[];count=total=0
    for p in selected:
        base,_,manifest=load_pack(p['id'],root);seen=set()
        if len(manifest['files'])!=p['image_count']:errors.append(p['id']+': image count mismatch')
        for f in manifest['files']:
            name=f['file'];label=p['id']+'/'+name
            if name in seen:errors.append(label+': duplicate image');continue
            seen.add(name);path=child(base,name);count+=1
            if not path.is_file():errors.append(label+': missing image');continue
            content=path.read_bytes();total+=len(content)
            if hashlib.sha256(content).hexdigest()!=f['sha256']:errors.append(label+': SHA mismatch');continue
            try:
                with Image.open(path) as im:
                    im.load()
                    if list(im.size)!=f['size']:errors.append(label+': dimension mismatch')
                    if im.format!='PNG':errors.append(label+': expected PNG')
            except OSError:errors.append(label+': image decode failed')
    if pack_id is None and count!=data['image_count']:errors.append('Catalog total image count mismatch')
    return {'status':'FAIL' if errors else 'PASS','packs':len(selected),'images':count,'bytes':total,
            'errors':errors,'coverage':'catalog identity, path safety, image bytes, SHA, dimensions and PNG decode; not animation or artistic adoption'}


def preview(pack_id,out,root=ROOT):
    result=verify(root,pack_id)
    if result['status']!='PASS':raise ValueError('Pack verification failed: '+str(result['errors']))
    out=Path(out).expanduser().resolve()
    if out.exists():raise FileExistsError('Preview output already exists; choose a new filename.')
    base,pack,manifest=load_pack(pack_id,root);cols=3;width=310;height=220
    sheet=Image.new('RGB',(cols*width,36+((len(manifest['files'])+cols-1)//cols)*height),'#182b36');draw=ImageDraw.Draw(sheet)
    draw.text((12,11),pack_id+' / asset contact sheet',fill='#d6e2df')
    for index,f in enumerate(manifest['files']):
        x=index%cols*width;y=36+index//cols*height
        # Checkerboard makes alpha and whole-frame backgrounds distinguishable.
        tile=Image.new('RGB',(width-12,height-34),'#b1b6b3');td=ImageDraw.Draw(tile)
        for yy in range(0,tile.height,12):
            for xx in range(0,tile.width,12):
                if (xx//12+yy//12)%2:td.rectangle((xx,yy,xx+11,yy+11),fill='#d5d8d0')
        with Image.open(child(base,f['file'])) as im:
            thumb=ImageOps.contain(im.convert('RGBA'),tile.size,Image.Resampling.LANCZOS)
        tile.paste(thumb,((tile.width-thumb.width)//2,(tile.height-thumb.height)//2),thumb)
        sheet.paste(tile,(x+6,y+4));draw.text((x+8,y+height-24),f['file'],fill='#d6e2df')
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('xb') as stream:sheet.save(stream,format='PNG')
    return {'pack':pack_id,'images':len(manifest['files']),'output':str(out),'kind':'static asset contact sheet, not a video'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    sub.add_parser('list');v=sub.add_parser('verify');v.add_argument('--pack')
    p=sub.add_parser('preview');p.add_argument('--pack',required=True);p.add_argument('--out',required=True,type=Path)
    a=parser.parse_args(argv)
    if a.action=='list':
        _,data=catalog();result={'packs':data['packs'],'image_count':data['image_count'],'selection':data['selection']}
    elif a.action=='verify':result=verify(pack_id=a.pack)
    else:result=preview(a.pack,a.out)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result.get('status')=='FAIL' else 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print('ERROR:',exc,file=sys.stderr);raise SystemExit(1)
