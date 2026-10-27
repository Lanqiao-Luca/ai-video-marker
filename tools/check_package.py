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


def check_video_contracts(root,catalog):
    """Check declared handoffs and this release's property scope, not execution."""
    errors=[]
    defaults=catalog.get('framework',{}).get('video_defaults',{})
    required=defaults.get('required_atoms',[])
    skill=root/defaults.get('skill','MISSING')
    role=root/defaults.get('role','MISSING')
    template=root/defaults.get('record_template','MISSING')
    for p in (skill,role,template):
        if not p.is_file():errors.append('Missing public-default contract: '+str(p.relative_to(root)))
    if skill.is_file():
        text=skill.read_text(encoding='utf-8')
        rows=re.findall(r'^\|\[([A-Z]+\d+) ',text,re.M)
        if len(required)!=15 or len(set(required))!=15 or rows!=required:
            errors.append('Public-default atom IDs must match the 15 declared conditional rows.')
    if role.is_file() and skill.is_file():
        expected=(Path('..')/skill.relative_to(root)).as_posix()+'#methods'
        if expected not in role.read_text(encoding='utf-8'):
            errors.append('Public video role must consume the adjacent default skill.')
    for route in catalog.get('routes',[]):
        workflow=root/route['workflow']
        if not workflow.is_file():continue
        text=workflow.read_text(encoding='utf-8')
        if defaults.get('workflow_anchor') not in anchors(text):
            errors.append('Missing public-entry handoff: '+route['id'])
        if '../agents/制作视频.md#public-entry' not in text:
            errors.append('Video workflow must hand off to the public role: '+route['id'])
        for mode in ('流程候选接入','当前制作/续作','美术阶段','后期/交付'):
            if '| '+mode not in text:
                errors.append('Missing mode/stage responsibility '+mode+': '+route['id'])
    allowed={'principle','method','operation','acceptance'}
    for rel in catalog.get('framework',{}).get('property_targets',[]):
        p=root/rel
        if not p.is_file():errors.append('Missing classified contract: '+rel);continue
        text=p.read_text(encoding='utf-8')
        match=re.match(r'^---\n(.*?)\n---\n',text,re.S)
        if not match:errors.append('NEEDS_PROPERTIES: '+rel);continue
        fields={}
        for key,value in re.findall(r'^\s*(atom_\w+|maintenance_role):\s*(.+)$',match[1],re.M):
            try:fields[key]=json.loads(value)
            except ValueError:fields[key]=value
        needed={'atom_property_schema','atom_nature','atom_secondary_natures',
                'atom_applicability','atom_scope_detail','maintenance_role'}
        if not needed.issubset(fields):errors.append('NEEDS_PROPERTIES: '+rel);continue
        secondary=fields['atom_secondary_natures'];primary=fields['atom_nature']
        if fields['atom_property_schema']!='APROP01-v1' or not isinstance(primary,str) or primary not in allowed:
            errors.append('Invalid atom schema/nature: '+rel)
        if (not isinstance(secondary,list) or any(not isinstance(x,str) or x not in allowed for x in secondary)
                or len(secondary)!=len(set(secondary)) or primary in secondary):
            errors.append('Invalid/duplicate primary-secondary nature: '+rel)
        scope=fields['atom_applicability']
        if not isinstance(scope,str) or scope not in {'general','domain'} or (scope=='domain' and not fields.get('atom_domain')):
            errors.append('Invalid/missing atom domain: '+rel)
        if not isinstance(fields['maintenance_role'],str) or fields['maintenance_role'] not in {'canonical','portable_replica'}:
            errors.append('Invalid atom maintenance identity: '+rel)
        if '<!-- ATOM_PROPERTIES:BEGIN -->' not in text or '<!-- ATOM_PROPERTIES:END -->' not in text:
            errors.append('Missing visible atom property block: '+rel)
        groups=fields.get('atom_nature_map',[])
        if not isinstance(groups,list):
            errors.append('Atom group map must be an array: '+rel)
            continue
        for group in groups:
            if not isinstance(group,dict):
                errors.append('Atom group entry must be an object: '+rel)
                continue
            selector=group.get('selector','')
            if not isinstance(selector,str) or not selector.startswith('#') or text.splitlines().count(selector)!=1:
                errors.append('Invalid/nonunique atom group selector: '+rel)
            gp=group.get('primary');ga=group.get('applicability')
            if not isinstance(gp,str) or gp not in allowed or not isinstance(ga,str) or ga not in {'domain','general'}:
                errors.append('Invalid atom group classification: '+rel)
            gs=group.get('secondary',[])
            if (not isinstance(gs,list) or any(not isinstance(x,str) or x not in allowed for x in gs)
                    or len(gs)!=len(set(gs)) or group.get('primary') in gs):
                errors.append('Invalid atom group secondary nature: '+rel)
            if group.get('applicability')=='domain' and not group.get('domain'):
                errors.append('Missing atom group domain: '+rel)
    return errors


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
    errors.extend(check_video_contracts(root,catalog))
    provenance=json.loads((root/'docs/provenance.json').read_text(encoding='utf-8'))
    for entry in provenance['files']:
        path=root/entry['target']
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=entry['target_sha256']:
            errors.append('Adaptation identity changed: '+entry['target'])
    return dict(status='PASS' if not errors else 'FAIL',files=len(files),routes=len(routes),
        formal_routes=sum(r['status']=='active' for r in routes),candidate_routes=sum(r['status']=='candidate' for r in routes),
        errors=errors,coverage='static links/syntax/catalog/provenance, declared public handoffs/property scope and narrow leak scan; not semantic/media/rights approval')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    a=parser.parse_args();result=check(a.root);print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
