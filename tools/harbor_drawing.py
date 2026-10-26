"""Animate the original reusable harbor PNG kit in one continuous world."""
import copy
import hashlib
import json
import math
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets/harbor'
INK='#263e51'
PALETTES=('sunset','midnight','mist')


def q(t,a,b):return max(0,min(1,(t-a)/(b-a)))

def ease(x):return x*x*(3-2*x)

def lerp(a,b,t):return a+(b-a)*t

def point(a,b,t):return tuple(lerp(x,y,t) for x,y in zip(a,b))

def path(t,keys):
    for a,b in zip(keys,keys[1:]):
        if t<=b[0]:return point(a[1:],b[1:],ease(q(t,a[0],b[0])))
    return keys[-1][1:]

def finite(v):return type(v) in (float,int) and math.isfinite(v)


def validate_harbor(s):
    if s.get('schema_version')!=1 or s.get('id')!='robot-lighthouse':raise ValueError('Expected robot-lighthouse scene.')
    if s.get('logical_size')!=[360,640] or s.get('duration')!=36:raise ValueError('Harbor story uses a 360x640 world and 36-second timeline.')
    size=s.get('output_size')
    if (not isinstance(size,list) or len(size)!=2 or any(type(v) is not int or not 64<=v<=4096 or v%2 for v in size)
            or size[0]*640!=size[1]*360):raise ValueError('Output must be even and use a 9:16 aspect.')
    if type(s.get('fps')) is not int or not 1<=s['fps']<=60:raise ValueError('fps must be in [1,60].')
    if type(s.get('seed')) is not int or not 0<=s['seed']<2**32:raise ValueError('seed must be in [0,2**32).')
    if s.get('palette') not in PALETTES:raise ValueError('Unknown harbor palette.')
    for name,length in [('camera_keys',4),('robot_path',3)]:
        keys=s.get(name);previous=-1
        if not isinstance(keys,list) or len(keys)<2:raise ValueError('Missing '+name)
        for k in keys:
            if (not isinstance(k,list) or len(k)!=length or not all(finite(v) for v in k) or not previous<k[0]<=36
                    or not 0<=k[1]<=360 or not 0<=k[2]<=640 or (length==4 and not 0<k[3]<=360)):
                raise ValueError('Invalid '+name)
            previous=k[0]
        if keys[0][0]!=0 or keys[-1][0]!=36:raise ValueError('Path must cover complete story.')
    cells=s.get('cells')
    if not isinstance(cells,list) or len(cells)!=3:raise ValueError('Three energy cells required.')
    for c,asset,pick in zip(cells,['cell-amber.png','cell-coral.png','cell-teal.png'],[4,12,20]):
        if c.get('asset')!=asset or c.get('pick')!=pick or c.get('insert')!=pick+4:raise ValueError('Cell identity/timeline must be preserved.')
        for key in ('ground','slot'):
            p=c.get(key)
            if not isinstance(p,list) or len(p)!=2 or not all(finite(v) for v in p) or not 0<=p[0]<=360 or not 0<=p[1]<=640:
                raise ValueError('Invalid cell position.')
    return s


def arm(d,shoulder,target):
    sx,sy=shoulder;dx,dy=target[0]-sx,target[1]-sy;dist=math.hypot(dx,dy);reach=min(dist,53)
    if dist:dx,dy=dx/dist,dy/dist
    else:dx,dy=1,0
    hand=(sx+dx*reach,sy+dy*reach);h=math.sqrt(max(0,26.5**2-(reach/2)**2))
    elbow=(sx+dx*reach/2-dy*h,sy+dy*reach/2+dx*h)
    pts=[tuple(round(v) for v in p) for p in [shoulder,elbow,hand]]
    d.line(pts,fill=INK,width=9);d.line(pts,fill='#acb4a4',width=5)
    for x,y in (elbow,hand):d.rectangle((round(x-3),round(y-3),round(x+3),round(y+3)),fill='#ddbc91',outline=INK)
    return hand


class HarborRenderer:
    def __init__(self,scene,asset_root=None):
        self.scene=copy.deepcopy(validate_harbor(scene));base=Path(asset_root or ASSETS)
        self.manifest=json.loads((base/'manifest.json').read_text(encoding='utf-8'));self.assets={}
        for name,record in self.manifest['files'].items():
            if Path(name).name!=name:raise ValueError('Asset name must stay inside the kit.')
            p=base/name
            if hashlib.sha256(p.read_bytes()).hexdigest()!=record['sha256']:raise ValueError('Harbor asset SHA mismatch: '+name)
            with Image.open(p) as im:self.assets[name]=im.convert('RGBA')
        required={'harbor-background.png','robot-head.png','robot-body.png','lighthouse.png','charging-console.png',
                  'sailboat.png','cell-amber.png','cell-coral.png','cell-teal.png'}
        if not required.issubset(self.assets):raise ValueError('Incomplete harbor kit.')
        self.base=self.assets['harbor-background.png'].copy()
        if scene['palette']=='midnight':self.base=Image.blend(self.base,Image.new('RGBA',self.base.size,'#173853'),.4)
        if scene['palette']=='mist':self.base=Image.blend(self.base,Image.new('RGBA',self.base.size,'#a4bcbd'),.22)

    def paste(self,im,name,x,y):im.alpha_composite(self.assets[name],(round(x),round(y)))

    def frame(self,t):
        if not finite(t) or not 0<=t<36:raise ValueError('Frame time must lie inside the story.')
        s=self.scene;im=self.base.copy();d=ImageDraw.Draw(im)
        power=ease(q(t,24,26));lamp=(278,190)
        boat_x=lerp(35,153,ease(q(t,26,34)));boat_y=lerp(556,537,ease(q(t,26,34)))+math.sin(t*2)*1.2
        if power:
            layer=Image.new('RGBA',(360,640));ld=ImageDraw.Draw(layer)
            sweep=math.sin(t*1.1)*.12*(1-ease(q(t,26,31)))
            target=(boat_x+38,boat_y+45);dx,dy=target[0]-lamp[0],target[1]-lamp[1]
            xx=lamp[0]+dx*1.25+sweep*150;yy=lamp[1]+dy*1.25
            ld.polygon([lamp,(xx-26,yy),(xx+26,yy)],fill=(255,225,167,round(38*power)))
            im=Image.alpha_composite(im,layer)
        self.paste(im,'lighthouse.png',220,140);d=ImageDraw.Draw(im)
        if power:
            for y in (190,197,204):d.line([(262,y),(293,y)],fill='#efd59c',width=2)
            d.ellipse((271,182,285,198),fill='#fff0b3',outline=INK)
            for k in range(3):
                phase=(t*1.5+k/3)%1;r=12+phase*8
                d.arc((lamp[0]-r,lamp[1]-r,lamp[0]+r,lamp[1]+r),100,260,fill='#d9c7a2')
        # Individual channels remain lit when each real cell is inserted.
        inserted=sum(t>=c['insert'] for c in s['cells'])
        for i,c in enumerate(s['cells']):
            col=('#eac181','#e7a5a0','#9acbc2')[i] if t>=c['insert'] else '#687d86'
            pts=[tuple(c['slot']),(254,c['slot'][1]),(254,225+i*6),(278,225+i*6)]
            d.line(pts,fill=INK,width=5);d.line(pts,fill=col,width=2)
        self.paste(im,'charging-console.png',207,394)
        # Robot body/head are reusable PNGs; jointed limbs follow real targets.
        x,y=path(t,s['robot_path']);moving=any(a[0]<t<b[0] and a[1]!=b[1] for a,b in zip(s['robot_path'],s['robot_path'][1:]))
        step=math.sin(t*9)*4 if moving else 0
        d=ImageDraw.Draw(im);d.ellipse((x-23,y-3,x+23,y+3),fill='#7c7882')
        for side in (-1,1):
            foot_x=x+side*10+side*step
            d.line([(round(x+side*9),round(y-25)),(round(foot_x),round(y-6))],fill=INK,width=9)
            d.line([(round(x+side*9),round(y-25)),(round(foot_x),round(y-6))],fill='#a8b0a0',width=5)
            d.rectangle((round(foot_x-9),round(y-9),round(foot_x+8),round(y)),fill='#c69a7a',outline=INK,width=2)
            d.line([(round(foot_x-5),round(y-3)),(round(foot_x+5),round(y-3))],fill='#f2cb9c')
        self.paste(im,'robot-body.png',x-18,y-57)
        self.paste(im,'robot-head.png',x-25,y-95-(abs(step)*.22))
        idle=(x+30,y-29);target=idle
        for c in s['cells']:
            pick,put=c['pick'],c['insert']
            if pick-1<=t<pick:target=point(idle,c['ground'],ease(q(t,pick-1,pick)))
            elif pick<=t<pick+.6:target=point(c['ground'],idle,ease(q(t,pick,pick+.6)))
            elif pick+.6<=t<put-1:target=idle
            elif put-1<=t<put:target=point(idle,c['slot'],ease(q(t,put-1,put)))
            elif put<=t<put+.6:target=point(c['slot'],idle,ease(q(t,put,put+.6)))
        d=ImageDraw.Draw(im);hand=arm(d,(x+19,y-50),target)
        other=(x-29,y-27) if t<30 else (x-33,y-73+math.sin(t*6)*4)
        arm(d,(x-19,y-50),other)
        cell_states=[]
        for c in s['cells']:
            state='ground' if t<c['pick'] else ('carried' if t<c['insert'] else 'installed')
            pos=c['ground'] if state=='ground' else (hand if state=='carried' else c['slot'])
            self.paste(im,c['asset'],pos[0]-7,pos[1]-10)
            cell_states.append({'asset':c['asset'],'state':state,'world':list(pos)})
        # Sailing is a response to the working beacon, not a reset or new shot.
        self.paste(im,'sailboat.png',boat_x,boat_y)
        d=ImageDraw.Draw(im);flag_y=boat_y+6
        d.polygon([(round(boat_x+38),round(flag_y)),(round(boat_x+50),round(flag_y+math.sin(t*5)*2+3)),
                   (round(boat_x+38),round(flag_y+7))],fill='#d99d87',outline=INK)
        for k in range(5):
            xx=boat_x+7+k*13;yy=boat_y+60+math.sin(t*3+k)
            d.line([(round(xx),round(yy)),(round(xx+9),round(yy))],fill='#a4c7c4')
        for k in range(7):
            xx=12+(k*53+s['seed']%37)%330;yy=523+(k*17)%108
            if math.sin(t*2+k)>.2:d.line([(xx,yy),(xx+9,yy)],fill='#9dc4c5')
        # Fixed landmark world and a single continuous camera for all actions.
        cx,cy,cw=path(t,s['camera_keys']);ch=cw*640/360
        left=max(0,min(360-cw,cx-cw/2));top=max(0,min(640-ch,cy-ch/2))
        box=tuple(round(v) for v in (left,top,left+cw,top+ch));bbox=[x-39,y-99,x+40,y+3]
        out=im.convert('RGB').crop(box).resize(tuple(s['output_size']),Image.Resampling.NEAREST)
        return out,{'t':t,'world':'HARBOR-STARTER','camera':[left,top,cw,ch],
                    'robot_world_bbox':bbox,'robot_normalized_bbox':[(bbox[0]-left)/cw,(bbox[1]-top)/ch,(bbox[2]-left)/cw,(bbox[3]-top)/ch],
                    'right_hand_world':list(hand),'requested_hand_world':list(target),'cells':cell_states,
                    'inserted_cells':inserted,'beacon_power':power,'boat_world':[boat_x,boat_y]}
