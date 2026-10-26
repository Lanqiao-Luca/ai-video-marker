"""Offline public-package check: links, syntax, route states, provenance and leaks."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote,urlsplit

EXCLUDE={'.venv','.git','__pycache__','outputs','work','.pytest_cache','.DS_Store'}


def public_files(root):
    return sorted(p for p in root.rglob('*') if p.is_file() and not any(x in EXCLUDE for x in p.relative_to(root).parts))


def anchors(text):
    text=re.sub(r'```.*?```','',text,flags=re.S)
    found=set(re.findall(r'<a\s+id=["\']([^"\']+)',text));counts={}
    for heading in re.findall(r'^#{1,6}\s+(.+)$',text,re.M):
        slug=re.sub(r'[^\w\- ]','',heading.lower()).replace(' ','-')
        n=counts.get(slug,0);counts[slug]=n+1
        found.add(slug if not n else slug+'-'+str(n))
    return found


def check(root):
    root=root.resolve();errors=[];files=public_files(root)
    for p in files:
        rel=p.relative_to(root).as_posix()
        if p.is_symlink():errors.append(rel+': symbolic links are not packaged');continue
        if p.suffix=='.py':
            try:ast.parse(p.read_text(encoding='utf-8'),filename=rel)
            except SyntaxError as exc:errors.append(str(exc))
        if p.suffix not in {'.md','.py','.json','.txt','.csv','.yml','.yaml'} and p.name not in {'AGENTS.md','CLAUDE.md'}:continue
        s=p.read_text(encoding='utf-8-sig')
        # Concrete private machine locations or secret material must not be exported.
        for pattern in ('/'+r'Users/[^\s`<>\"\']+','/'+r'home/[^\s`<>\"\']+',r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',r'\bsk-[A-Za-z0-9]{20,}'):
            if re.search(pattern,s):errors.append(rel+': private-path/secret pattern')
        if p.suffix=='.json':
            try:json.loads(s)
            except ValueError as exc:errors.append(rel+': '+str(exc))
        if p.suffix!='.md':continue
        content=re.sub(r'```.*?```','',s,flags=re.S)
        for match in re.finditer(r'\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))\)',content):
            target=match[1] or match[2];url=urlsplit(target)
            if url.scheme:continue
            path=unquote(url.path);anchor=unquote(url.fragment)
            dest=(p.parent/path).resolve() if path else p
            try:dest.relative_to(root)
            except ValueError:errors.append(rel+': link escapes package '+target);continue
            if not dest.is_file():errors.append(rel+': missing link '+target)
            elif anchor and dest.suffix=='.md' and anchor not in anchors(dest.read_text(encoding='utf-8')):
                errors.append(rel+': missing anchor '+target)
    catalog=json.loads((root/'catalog.json').read_text(encoding='utf-8'))
    routes=catalog['routes']
    if not routes or len({r['id'] for r in routes})!=len(routes):errors.append('Catalog needs unique production routes.')
    framework=catalog.get('framework',{})
    layers=framework.get('layers',[])
    if layers!=['graphs','loops','workflows','agents','skills','standards']:
        errors.append('Catalog must declare the six method layers in handoff order.')
    for layer in layers:
        if not (root/layer/'README.md').is_file():errors.append('Missing method layer entry: '+layer)
    for route in routes:
        if route.get('status') not in {'active','candidate'}:errors.append('Unknown route status: '+route['id'])
        p=root/route['workflow']
        if not p.is_file():errors.append('Missing workflow '+str(p));continue
        status=re.search(r'^status: (\w+)$',p.read_text(encoding='utf-8'),re.M)
        if not status or status[1]!=route['status']:errors.append('Catalog status mismatch: '+route['id'])
        if route.get('implementation') not in {'documented_workflow','runnable_demo'}:
            errors.append('Unknown implementation scope: '+route['id'])
        if route.get('template') and not (root/route['template']).is_file():errors.append('Missing route template: '+route['id'])
    provenance=json.loads((root/'docs/provenance.json').read_text(encoding='utf-8'))
    for entry in provenance['files']:
        path=root/entry['target']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=entry['target_sha256']:
            errors.append('Adaptation identity changed: '+entry['target'])
    return dict(status='PASS' if not errors else 'FAIL',files=len(files),routes=len(routes),
        formal_routes=sum(r['status']=='active' for r in routes),candidate_routes=sum(r['status']=='candidate' for r in routes),
        errors=errors,coverage='static package links/syntax/catalog/provenance and narrow leak scan; not media or rights approval')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    a=parser.parse_args();result=check(a.root);print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
