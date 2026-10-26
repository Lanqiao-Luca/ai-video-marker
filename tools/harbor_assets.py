"""Create the original reusable harbor PNG kit from editable drawing source.

Only Pillow is required. No image model, remote asset, font or private source.
Choose a NEW output directory; the generator never replaces an existing kit.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
from PIL import Image,ImageDraw

INK='#263e51'


def canvas(size):
    im=Image.new('RGBA',size,(0,0,0,0));return im,ImageDraw.Draw(im)


def rect(d,box,fill,outline=INK,width=1):d.rectangle(box,fill=fill,outline=outline,width=width)


def line(d,points,fill=INK,width=1):d.line(points,fill=fill,width=width)


def polygon(d,points,fill,outline=INK):
    d.polygon(points,fill=fill);d.line(points+[points[0]],fill=outline,width=1)


def background():
    im,d=canvas((360,640))
    for y in range(640):
        f=min(1,y/500);col=tuple(round(a+(b-a)*f) for a,b in zip((57,76,112),(226,166,143)))
        line(d,[(0,y),(360,y)],col)
    d.ellipse((39,117,104,182),fill='#f5cf9e')
    for x,y,r in [(24,95,24),(180,142,34),(288,91,30)]:
        for dx,dy,rr in [(-r,5,r*.6),(0,0,r),(r,6,r*.7)]:
            d.ellipse((x+dx-rr,y+dy-rr*.35,x+dx+rr,y+dy+rr*.35),fill='#c2a4aa')
    polygon(d,[(0,329),(33,295),(61,319),(108,281),(155,327),(202,301),(258,337),(314,300),(360,319),(360,470),(0,470)],'#8b8f9d',outline='#8b8f9d')
    rng=random.Random(932)
    for x in range(-20,360,35):
        y=rng.randrange(353,396);rect(d,(x,y,x+29,458),'#87939b',outline='#667a8d')
        polygon(d,[(x-4,y),(x+14,y-17),(x+33,y)],'#987e86')
        for yy in range(y+10,450,15):
            for xx in (x+5,x+18):rect(d,(xx,yy,xx+5,yy+7),'#d5bab0',outline='#5c7686')
    for y in range(449,640):
        f=(y-449)/191;col=tuple(round(a+(b-a)*f) for a,b in zip((78,133,151),(33,77,100)))
        line(d,[(0,y),(360,y)],col)
    for k in range(90):
        x=rng.randrange(360);y=rng.randrange(455,640)
        line(d,[(x,y),(x+rng.randrange(3,18),y)],rng.choice(['#6fa4ad','#91bac0','#527f95']))
    # Stone island and connected weathered jetty share a fixed ground plane.
    polygon(d,[(223,462),(340,462),(358,503),(338,542),(233,526),(215,498)],'#6b8090')
    for x,y,w in [(229,491,27),(269,510,35),(316,494,31),(236,518,21),(326,528,17)]:
        polygon(d,[(x,y),(x+w,y-4),(x+w+4,y+9),(x+2,y+13)],'#91a2a3')
    polygon(d,[(12,478),(237,478),(248,506),(2,506)],'#bc9690')
    rect(d,(2,506,248,514),'#6b6c7d',width=2)
    for y in (485,494,503):line(d,[(8,y),(242,y)],'#806e7f')
    for x in range(15,239,24):line(d,[(x,479),(x-4,505)],'#e2b8a0')
    for x in (22,94,176,232):
        rect(d,(x,514,x+7,583),'#6d707e',width=1);line(d,[(x+2,516),(x+2,582)],'#c1a79b',2)
        for yy in (529,547,565):line(d,[(x-2,yy),(x+10,yy)],'#5a7184',2)
    # Nets, coils, dock posts and a crab give this place a separate identity.
    for x in (17,133):
        rect(d,(x,449,x+6,482),'#8a7882');rect(d,(x-2,448,x+8,453),'#d4b19a')
        d.ellipse((x-3,455,x+10,464),outline='#e4c59f',width=2)
    for i in range(7):
        line(d,[(29+i*4,453),(47+i*4,477)],'#9badac')
        line(d,[(29,453+i*3),(72,453+i*3)],'#9badac')
    for r in (4,7,10):d.ellipse((148-r,490-r*.3,148+r,490+r*.3),outline='#d9bc9f')
    d.ellipse((39,523,49,529),fill='#df9b87',outline=INK)
    for side in (-1,1):line(d,[(44+side*4,526),(44+side*9,522),(44+side*11,525)],'#df9b87',2)
    return im


def robot_head():
    im,d=canvas((50,43))
    line(d,[(25,7),(25,2)],INK,3);rect(d,(23,0,27,4),'#dcb775')
    rect(d,(3,10,46,38),'#dbb885',width=2);rect(d,(6,8,43,34),'#efd7ae',width=2)
    rect(d,(7,10,42,13),'#fff0cc',outline='#fff0cc')
    rect(d,(10,16,39,29),'#304e62',width=2)
    for x in (16,31):
        rect(d,(x-2,19,x+2,23),'#a1e6dc',outline='#a1e6dc');rect(d,(x-1,18,x,19),'#e3fff0',outline='#e3fff0')
    line(d,[(22,26),(27,26)],'#75b8be')
    rect(d,(0,17,5,29),'#84aaa9',width=1);rect(d,(44,17,49,29),'#84aaa9')
    for x in (8,41):d.ellipse((x-1,31,x+1,33),fill='#8f7b70')
    line(d,[(18,38),(31,38)],'#728f94',3)
    return im


def robot_body():
    im,d=canvas((36,34))
    polygon(d,[(3,1),(31,1),(35,27),(30,32),(5,32),(0,27)],'#5c929b')
    rect(d,(5,3,29,25),'#87b8b7',width=2);rect(d,(8,6,26,19),'#c6bd99')
    rect(d,(11,8,23,16),'#3a5969');line(d,[(14,12),(20,12)],'#c9e1b7',2)
    for x in (8,16,24):rect(d,(x,26,x+3,28),'#d5b48e')
    rect(d,(1,7,4,18),'#dfa97f');rect(d,(30,7,33,18),'#dfa97f')
    return im


def lighthouse():
    im,d=canvas((116,350));cx=58
    polygon(d,[(39,76),(77,76),(103,334),(12,334)],'#e9cbb0')
    for y in (137,218,299):
        l=round(39-(y-76)*27/258);r=116-l
        polygon(d,[(l,y),(r,y),(r+4,y+32),(l-3,y+32)],'#ba7c7b')
        line(d,[(l+2,y+3),(r-2,y+3)],'#df9f8d',2)
    for y in range(92,333,12):
        l=round(39-(y-76)*27/258);r=116-l
        line(d,[(l+1,y),(r-1,y)],'#b19d98')
        for x in range(l+7+(y//12%2)*10,r-4,20):line(d,[(x,y),(x,y+10)],'#b9a5a0')
    for y in (115,197,275):
        rect(d,(49,y,66,y+29),'#3a5769',width=2);rect(d,(52,y+3,63,y+24),'#82a8ae')
        line(d,[(58,y+2),(58,y+26)],'#d8bfaa',2);rect(d,(46,y+28,69,y+32),'#ceb59f')
    # Unlit lantern room; the running scene owns the lens/light animation.
    rect(d,(28,30,88,74),'#91b2b3',width=2)
    rect(d,(32,34,84,68),'#314d66',width=1)
    for x in (33,58,83):line(d,[(x,31),(x,70)],'#c1bbaa',3)
    rect(d,(20,73,96,81),'#d8b69c',width=2)
    for x in range(22,97,9):line(d,[(x,62),(x,75)],'#526779',2)
    line(d,[(19,62),(97,62)],'#c0b49e',2)
    polygon(d,[(20,30),(58,4),(96,30)],'#a46f78')
    line(d,[(33,26),(59,10),(82,26)],'#ddac96',2)
    line(d,[(58,4),(58,0)],INK,2)
    rect(d,(7,334,108,345),'#b2ada0',width=2)
    return im


def console():
    im,d=canvas((46,96))
    polygon(d,[(7,2),(40,2),(45,90),(2,90)],'#937c78')
    rect(d,(8,8,37,81),'#d4b59a',width=2)
    for y in (20,41,62):
        rect(d,(12,y-5,33,y+12),'#3f5b68',width=1)
        for x in (14,29):rect(d,(x,y-3,x+1,y+9),'#8ca6a5',outline='#8ca6a5')
    rect(d,(0,88,45,95),'#b9a493',width=2)
    return im


def cell(color):
    im,d=canvas((15,20));rect(d,(5,0,9,2),'#e1c9a1')
    rect(d,(1,2,13,18),'#b2a388',width=1);rect(d,(3,4,11,15),color)
    line(d,[(5,5),(5,13)],'#fff0c7');rect(d,(4,17,10,19),'#5d7780')
    return im


def boat():
    im,d=canvas((76,62))
    line(d,[(37,5),(37,46)],INK,3);polygon(d,[(35,10),(8,38),(35,38)],'#f2d5b1')
    polygon(d,[(40,12),(40,38),(65,38)],'#a4c8c3');line(d,[(16,31),(32,14)],'#d5aa93')
    polygon(d,[(3,43),(73,43),(62,57),(17,57)],'#9a7377');line(d,[(8,47),(69,47)],'#e6b493',3)
    rect(d,(28,40,51,48),'#b7a999');rect(d,(32,41,38,46),'#4c6d80')
    d.ellipse((17,48,24,55),fill='#3d5969',outline='#b4c8bb');d.ellipse((55,48,62,55),fill='#3d5969',outline='#b4c8bb')
    return im


def robot_sprite(pose):
    im,d=canvas((90,110));x,y=45,105
    for side in (-1,1):
        line(d,[(x+side*9,y-25),(x+side*10,y-6)],INK,9)
        line(d,[(x+side*9,y-25),(x+side*10,y-6)],'#a8b0a0',5)
        rect(d,(x+side*10-9,y-9,x+side*10+8,y),'#c69a7a',width=2)
    im.alpha_composite(robot_body(),(27,48));im.alpha_composite(robot_head(),(20,10))
    d=ImageDraw.Draw(im)
    for side in (-1,1):
        target=(x+side*30,y-29);elbow=(x+side*31,y-44)
        if pose=='wave' and side==-1:target=(9,33);elbow=(7,57)
        if pose=='carry' and side==1:target=(75,65);elbow=(83,68)
        points=[(x+side*19,y-50),elbow,target]
        line(d,points,INK,9);line(d,points,'#acb4a4',5)
        rect(d,(target[0]-3,target[1]-3,target[0]+3,target[1]+3),'#ddbc91')
    if pose=='carry':im.alpha_composite(cell('#eac181'),(68,55))
    return im


def build(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    assets={'harbor-background.png':background(),'robot-head.png':robot_head(),'robot-body.png':robot_body(),
            'lighthouse.png':lighthouse(),'charging-console.png':console(),'sailboat.png':boat(),
            'cell-amber.png':cell('#eac181'),'cell-coral.png':cell('#e7a5a0'),'cell-teal.png':cell('#9acbc2'),
            **{'robot-'+pose+'.png':robot_sprite(pose) for pose in ('idle','carry','wave')}}
    manifest={'schema_version':1,'kit':'harbor-robot','origin':'Original code-native pixel artwork for ai-video-marker',
              'license':'MIT','generation':'Pillow only; no image-model API or external assets','files':{}}
    for name,im in assets.items():
        p=out/name;im.save(p);manifest['files'][name]={'size':list(im.size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    print(json.dumps(build(p.parse_args().out),ensure_ascii=False,indent=2))
