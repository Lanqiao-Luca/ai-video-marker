"""PIXEL-010 drawing logic, extracted without changing its drawing functions.

This renderer reproduces one existing short; it is not an arbitrary-story engine.
Source and function identities are recorded in examples/pixel/source-frame-baseline.json.
"""
from pathlib import Path
import hashlib, math, random
from PIL import Image, ImageDraw

S = {}
W = H = FPS = 0
INK = '#323447'
BASE = None


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def q(t,a,b): return max(0,min(1,(t-a)/(b-a)))

def e(v): return v*v*(3-2*v)

def mix(a,b,v): return a+(b-a)*v

def path(t,keys):
    if t<=keys[0][0]: return keys[0][1:]
    for a,b in zip(keys,keys[1:]):
        if t<=b[0]: return [mix(x,y,e(q(t,a[0],b[0]))) for x,y in zip(a[1:],b[1:])]
    return keys[-1][1:]

def pts(v):return [(round(x),round(y)) for x,y in v]

def rec(d,b,c,o=None,w=1):d.rectangle(tuple(round(x) for x in b),fill=c,outline=o,width=w)

def ell(d,b,c,o=None,w=1):d.ellipse(tuple(round(x) for x in b),fill=c,outline=o,width=w)

def line(d,p,c,w=1):d.line(pts(p),fill=c,width=w,joint='curve')

def poly(d,p,c,o=INK,w=1):
    p=pts(p);d.polygon(p,fill=c)
    if o:d.line(p+[p[0]],fill=o,width=w,joint='curve')

def obj(i):return S['objects'][i]

def gear(d,x,y,r,a,c='#d7ac6c'):
    pp=[]
    for k in range(48):
        z=a+k*math.tau/48;rr=r if k%4 in (0,1) else r-3
        pp.append((x+rr*math.cos(z),y+rr*math.sin(z)))
    poly(d,pp,c,INK,2);ell(d,(x-r/2,y-r/2,x+r/2,y+r/2),'#65596a',INK)
    for k in range(4):
        z=a+k*math.pi/2
        line(d,[(x+4*math.cos(z),y+4*math.sin(z)),(x+(r-6)*math.cos(z),y+(r-6)*math.sin(z))],'#f8d798',2)
    ell(d,(x-3,y-3,x+3,y+3),'#f8dcad',INK)

def background():
    im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im)
    for y in range(H):
        c=tuple(round(mix(a,b,y/H)) for a,b in zip((83,100,139),(224,173,164)))
        line(d,[(0,y),(W,y)],c)
    rng=random.Random(107)
    # Pixel clouds, mountain silhouettes, distant balconies and tiled roofs.
    for x,y,r in [(22,115,23),(290,95,32),(310,258,21),(-10,304,30)]:
        for dx,dy,rr in [(-r,7,r*.65),(0,0,r),(r,10,r*.7)]:
            ell(d,(x+dx-rr,y+dy-rr/2,x+dx+rr,y+dy+rr/2),'#a6a9bd')
    poly(d,[(0,340),(44,270),(72,305),(124,257),(178,325),(241,286),(299,332),(360,278),(360,470),(0,470)],'#8d91aa',None)
    for x in range(-20,380,39):
        y=rng.randrange(345,410);col=rng.choice(['#8b8b9d','#a194a7','#a3a2ae'])
        rec(d,(x,y,x+32,540),col)
        rec(d,(x-2,y,x+34,y+4),'#666f89')
        for yy in range(y+12,535,20):
            for xx in (x+6,x+20):
                rec(d,(xx,yy,xx+6,yy+9),'#cfbfbb');rec(d,(xx,yy,xx+6,yy+2),'#626c86')
                line(d,[(xx-2,yy+10),(xx+8,yy+10)],'#656c86')
    # Permanent rooftop architecture. Floor and facade share this one world.
    rec(d,(18,476,342,640),'#716b84',INK,2)
    rec(d,(18,484,342,501),'#a88694',INK,2)
    rec(d,(18,501,342,507),'#dec0b0',INK)
    for yy in range(512,640,12):
        line(d,[(20,yy),(340,yy)],'#665f79')
        for xx in range(20+(yy//12%2)*12,342,24):line(d,[(xx,yy),(xx,yy+12)],'#665f79')
    for x in (62,157,252):
        rec(d,(x,539,x+47,604),'#454d69',INK,2)
        rec(d,(x+3,542,x+44,599),'#e4b59b',INK)
        rec(d,(x+7,548,x+40,594),'#c4abb3')
        line(d,[(x+23,544),(x+23,599)],'#6e6b84',3)
        line(d,[(x+5,571),(x+42,571)],'#6e6b84',3)
        rec(d,(x-4,600,x+52,608),'#be9ca4',INK)
        for sy in range(543,600,6):
            line(d,[(x-9,sy),(x-4,sy)],'#4b536c',2);line(d,[(x+51,sy),(x+56,sy)],'#4b536c',2)
    # Side rails and roof tiles.
    for yy in range(450,493,8):line(d,[(20,yy),(340,yy)],'#806d82')
    for xx in range(25,342,19):line(d,[(xx,450),(xx+8,491)],'#b99a9c')
    for x in range(23,345,23):
        line(d,[(x,447),(x,478)],'#555b72',3)
        ell(d,(x-2,445,x+2,449),'#e1c1a7',INK)
    line(d,[(20,451),(340,451)],'#c2a3aa',3)
    # Left stairhouse, no signs, letters, or clock numerals.
    rec(d,(25,304,69,446),'#b2b0b9',INK,2)
    poly(d,[(20,306),(46,288),(74,307)],'#ac7c83',INK,2)
    rec(d,(35,368,60,445),'#6a718a',INK,2)
    rec(d,(39,373,56,413),'#c0c7c5',INK)
    rec(d,(53,426,55,429),'#e4bf85')
    ell(d,(36,327,58,349),'#ebca9b',INK,2)
    line(d,[(47,330),(47,339),(53,342)],'#676078',2)
    rec(d,(22,443,74,449),'#d0b0a9',INK)
    # Front climbing ivy and tiny roof ornaments.
    for x in (28,332):
        for yy in range(492,621,13):
            line(d,[(x,yy),(x+math.sin(yy)*4,yy+14)],'#426c68',2)
            ell(d,(x-7,yy,x,yy+8),'#5f8d77',INK)
            ell(d,(x,yy+5,x+6,yy+11),'#83aa88',INK)
    for x in (83,288,316):
        rec(d,(x-10,468,x+10,483),'#b87971',INK,2)
        rec(d,(x-12,466,x+12,471),'#e4b194',INK)
    return im

def wheel_angle(t):
    if t<11.7:return 0
    if t<13.6:return q(t,11.7,13.6)*.8
    if t<18.9:return .8+.035*math.sin(t*22)
    return .8+(t-18.9)*2.6

def machines(im,t):
    d=ImageDraw.Draw(im);wx,wy=obj('wheel')['center'];r=obj('wheel')['radius'];a=wheel_angle(t)
    # Elevated rain cistern and open channel, with visible increasing water level.
    bx,by=obj('basin')['center'];fill=e(q(t,8,11.7))
    for x in (bx-23,bx+23):line(d,[(x,by+7),(x,487)],'#645c73',5)
    rec(d,(bx-30,by-29,bx+30,by+18),'#bd958a',INK,2)
    rec(d,(bx-25,by-25,bx+25,by+11),'#586c7d',INK)
    if fill>0:rec(d,(bx-24,by+10-30*fill,bx+24,by+10),'#8dd2d0')
    for i in range(3):line(d,[(bx-22+i*15,by+9-30*fill),(bx-14+i*15,by+9-30*fill)],'#d2ebe0')
    rec(d,(bx-33,by-31,bx+33,by-26),'#e5bba0',INK)
    line(d,[(bx+29,by-6),(wx-11,by-6),(wx-11,wy-34)],'#343d50',9)
    line(d,[(bx+29,by-7),(wx-11,by-7),(wx-11,wy-34)],'#bbbea9',5)
    if t>=11.7:
        for n in range(9):
            yy=wy-33+((t*60+n*8)%48)
            line(d,[(wx-11,yy),(wx-11,yy+5)],'#a8e1da',3)
    # Waterwheel rim, structural spokes and cups.
    ell(d,(wx-r-2,wy-r-2,wx+r+2,wy+r+2),'#a67d70',INK,2)
    ell(d,(wx-r+5,wy-r+5,wx+r-5,wy+r-5),'#55687b',INK,2)
    for k in range(10):
        z=a+k*math.tau/10;c,s=math.cos(z),math.sin(z)
        line(d,[(wx,wy),(wx+(r-3)*c,wy+(r-3)*s)],'#e2b57b',4)
        poly(d,[(wx+(r-8)*c-6*s,wy+(r-8)*s+6*c),(wx+(r+3)*c-6*s,wy+(r+3)*s+6*c),(wx+(r+3)*c+6*s,wy+(r+3)*s-6*c),(wx+(r-8)*c+6*s,wy+(r-8)*s-6*c)],'#ca9b71',INK)
    ell(d,(wx-7,wy-7,wx+7,wy+7),'#f2d099',INK,2)
    # Bearing feet and visible transmission belts.
    poly(d,[(wx-5,wy+3),(wx-15,488),(wx+16,488),(wx+5,wy+3)],'#b4aa9a',INK,2)
    gx,gy=obj('gear')['center'];fx,fy=obj('flower')['center']
    line(d,[(wx+5,wy-7),(gx+4,gy-9)],'#4c465a',4)
    line(d,[(wx-4,wy+7),(gx-5,gy+9)],'#4c465a',4)
    gear(d,gx,gy,17,-a)
    line(d,[(gx+10,gy-7),(fx+9,fy),(fx+10,228)],'#554e64',4)
    line(d,[(gx-9,gy+7),(fx-9,fy),(fx-10,228)],'#554e64',4)
    if t>19:
        for j in range(7):
            yy=fy+((t*34+j*26)%(gy-fy));line(d,[(fx+8,yy),(fx+11,yy+4)],'#b7b4a7')
    # Leaf visibly blocks bearing, then is pulled free by the rabbit.
    leaf_free=e(q(t,16.8,18.9));lx=wx+10+leaf_free*39;ly=wy-8-leaf_free*20
    if t<22:
        poly(d,[(lx-13,ly-5),(lx-6,ly-15),(lx+9,ly-16),(lx+12,ly-5),(lx+2,ly+3)],'#a4b86f',INK)
        line(d,[(lx-8,ly-1),(lx+7,ly-13)],'#647755')
    # Sunflower: hinged folded copper petals reveal the luminous face.
    line(d,[(fx,fy+12),(fx,483)],'#4a5866',9)
    line(d,[(fx-1,fy+12),(fx-1,483)],'#9dba9d',4)
    rec(d,(fx-23,475,fx+23,488),'#ac7c70',INK,2)
    rec(d,(fx-26,470,fx+26,477),'#deb391',INK)
    opened=e(q(t,22.7,28.8));rot=.035*max(0,t-29)+.025*math.sin(t*3)*q(t,28,30)
    for k in range(12):
        z=k*math.tau/12+rot;rr=19+25*opened;hh=10+8*opened
        u=(math.cos(z),math.sin(z));v=(-u[1],u[0])
        pp=[(fx+u[0]*13+v[0]*6,fy+u[1]*13+v[1]*6),(fx+u[0]*(rr-7)+v[0]*hh,fy+u[1]*(rr-7)+v[1]*hh),(fx+u[0]*(rr+13),fy+u[1]*(rr+13)),(fx+u[0]*(rr-7)-v[0]*hh,fy+u[1]*(rr-7)-v[1]*hh),(fx+u[0]*13-v[0]*6,fy+u[1]*13-v[1]*6)]
        poly(d,pp,['#e9ad75','#f5c982','#d79870'][k%3],INK,2)
        line(d,[(fx+u[0]*19,fy+u[1]*19),(fx+u[0]*(rr+5),fy+u[1]*(rr+5))],'#ffdf9c')
    ell(d,(fx-20,fy-20,fx+20,fy+20),'#9d715f',INK,2)
    rr=11+5*opened
    ell(d,(fx-rr,fy-rr,fx+rr,fy+rr),'#ffdd8f' if opened>.8 else '#c59c79',INK)
    if opened>.85:
        for xx in (fx-6,fx+6):line(d,[(xx-2,fy-2),(xx+2,fy-2)],INK,2)
        line(d,[(fx-5,fy+5),(fx,fy+8),(fx+5,fy+5)],INK)
    # Physical leaves unfold on the stem and pots, with persistent growth.
    growth=e(q(t,29.8,33.5))
    for side,yy in [(-1,410),(1,385)]:
        le=10+20*growth
        poly(d,[(fx,yy),(fx+side*le,yy-15*growth-4),(fx+side*(le+5),yy+6),(fx+side*12,yy+8)],'#7eaa8c',INK)
    for px in (83,288,316):
        height=9+25*growth
        line(d,[(px,465),(px,465-height)],'#49756b',3)
        for side in (-1,1):
            poly(d,[(px,457),(px+side*(8+5*growth),448-height*.25),(px+side*11,459),(px,461)],'#97b58d',INK)
        if growth>.5:
            for k in range(5):
                z=k*math.tau/5;ell(d,(px+5*math.cos(z)-3,465-height+5*math.sin(z)-3,px+5*math.cos(z)+3,465-height+5*math.sin(z)+3),'#f1b8aa',INK)
            ell(d,(px-2,463-height,px+2,467-height),'#ffdf97')

def clothes(im,t):
    d=ImageDraw.Draw(im);x1,y1,x2,y2=obj('clothesline')['span']
    for x in (x1,x2):
        line(d,[(x,226),(x,479)],'#4b586d',4);ell(d,(x-3,222,x+3,228),'#d9b293',INK)
    line(d,[(x1,y1),(180,y1+12),(x2,y2)],INK,2)
    gear(d,x2,227,12,wheel_angle(t)*.4,'#9fa998')
    progress=e(q(t,31,36.8));travel=max(0,t-36.8)*8
    for i,col in enumerate(['#b2d3ca','#dfa1a1','#f3d3a1','#9dacc9']):
        x=x1+40+i*64+math.sin(travel/30)*8*progress
        yy=y1+8+6*math.sin((x-x1)/(x2-x1)*math.pi)
        sway=math.sin(t*3.5+i)*progress*5
        line(d,[(x-7,yy-3),(x-7,yy+5)],'#e2b98e',3);line(d,[(x+7,yy-3),(x+7,yy+5)],'#e2b98e',3)
        # The same cloth gains a tail and fins, it never changes identity/position.
        poly(d,[(x-15,yy+5),(x+15,yy+5),(x+17+sway,yy+35),(x-14+sway,yy+36)],col,INK,2)
        for sy in (12,22,31):line(d,[(x-12+sway*.5,yy+sy),(x+14+sway*.5,yy+sy)],'#f7e8cb',2)
        if progress:
            poly(d,[(x+15+sway,yy+16),(x+15+sway+16*progress,yy+7),(x+15+sway+16*progress,yy+34),(x+15+sway,yy+27)],col,INK)
            poly(d,[(x+sway,yy+6),(x+8+sway,yy+6-10*progress),(x+12+sway,yy+6)],col,INK)
            ell(d,(x-10+sway,yy+15,x-6+sway,yy+19),INK)

def rabbit(im,t):
    x,y=path(t,S['rabbit_path']);running=(3.6<t<6.8 or 13.5<t<16.0 or 20.5<t<22.5)
    bounce=abs(math.sin(t*10))*3 if running else (2*math.sin(t*6) if t>34 else 0)
    if .6<t<1.4:bounce+=math.sin(q(t,.6,1.4)*math.pi)*13
    y-=bounce;d=ImageDraw.Draw(im)
    ell(d,(x-19,y-2,x+19,y+3),'#6a657d')
    # Scarf tail and small cotton tail behind the torso.
    poly(d,[(x-10,y-36),(x-28,y-28+math.sin(t*5)*3),(x-25,y-22),(x-8,y-29)],'#d97f7c',INK)
    ell(d,(x-21,y-25,x-10,y-13),'#e5deca',INK,2)
    for side in (-1,1):
        dx=side*8+(side*4*math.sin(t*10) if running else 0)
        ell(d,(x+dx-7,y-10,x+dx+6,y),'#c08c70',INK,2)
        line(d,[(x+dx-4,y-3),(x+dx+4,y-3)],'#edbf8f')
    poly(d,[(x-13,y-35),(x+12,y-35),(x+17,y-10),(x-15,y-10)],'#ede4ce',INK,2)
    poly(d,[(x-9,y-33),(x+9,y-33),(x+12,y-12),(x-11,y-12)],'#73a4a0',INK)
    rec(d,(x-5,y-23,x+6,y-16),'#a8c9b9',INK)
    # Fixed silhouette, ears articulate with the hop.
    for side in (-1,1):
        ex=x+side*9;tip=side*(2+2*math.sin(t*2))
        poly(d,[(ex-6,y-53),(ex-6+tip,y-76),(ex-1+tip,y-81),(ex+5+tip,y-77),(ex+6,y-52)],'#f2e9d4',INK,2)
        line(d,[(ex+tip,y-74),(ex,y-57)],'#dba8a0',3)
    ell(d,(x-21,y-61,x+21,y-30),'#f6edda',INK,2)
    ell(d,(x-17,y-44,x-10,y-39),'#e7b2a4');ell(d,(x+11,y-44,x+18,y-39),'#e7b2a4')
    blink=int(t*24)%103 in (0,1,2)
    for xx in (x-9,x+9):
        if blink or t>36:line(d,[(xx-3,y-47),(xx,y-49),(xx+3,y-47)],INK,2)
        else:rec(d,(xx-2,y-50,xx+1,y-45),INK);rec(d,(xx-1,y-50,xx-1,y-49),'#fff5dc')
    poly(d,[(x-3,y-43),(x+3,y-43),(x,y-40)],'#af7a7c',None)
    line(d,[(x,y-40),(x-3,y-37)],INK)
    rec(d,(x-13,y-33,x+13,y-29),'#d97f7c',INK)
    # Arms have explicit targets for the umbrella/blocked bearing.
    if 3.4<t<13.5:
        lift=e(q(t,6.8,8.5));ux,uy=obj('umbrella')['placed_center']
        hand=(mix(x+15,ux,lift),mix(y-61,uy+26,lift));other=(x-10,y-37)
    elif 15.5<t<20.5:
        lx=obj('wheel')['center'][0]+10+e(q(t,16.8,18.9))*39
        ly=obj('wheel')['center'][1]-8-e(q(t,16.8,18.9))*20
        hand=(lx,ly);other=(x-12,y-25)
    elif t>34:
        hand=(x+23,y-42-math.sin(t*6)*4);other=(x-22,y-45+math.sin(t*6)*4)
    else:hand=(x+17,y-22);other=(x-16,y-22)
    for shoulder,target in [((x+11,y-29),hand),((x-11,y-29),other)]:
        line(d,[shoulder,target],INK,7);line(d,[shoulder,target],'#e9dfc9',5)
        ell(d,(target[0]-3,target[1]-3,target[0]+3,target[1]+3),'#f7ead4',INK)
    # Umbrella rests in its original location after it is placed over the tank.
    if t>3.4:
        f=e(q(t,3.4,4.25));ux,uy=hand[0],hand[1]-26
        if t>=8.5:ux,uy=obj('umbrella')['placed_center']
        width=28*f;depth=13*f
        invert=e(q(t,7.7,8.5));sgn=mix(-1,1,invert)
        line(d,[(ux,uy),(ux,uy+29)],INK,3);line(d,[(ux,uy+28),(ux+6,uy+31),(ux+10,uy+27)],'#d0b48f',3)
        left=(ux-width,uy);right=(ux+width,uy);mid=(ux,uy+sgn*depth)
        for k,col in enumerate(['#76aaa9','#e5a092','#a8c5b5','#f0c795']):
            xa=mix(left[0],right[0],k/4);xb=mix(left[0],right[0],(k+1)/4)
            poly(d,[mid,(xa,uy),(xb,uy)],col,INK)
        line(d,[left,(ux,uy+sgn*depth),right],INK,2)
        if t>8.5:
            fill=e(q(t,8.5,11.7));line(d,[(ux-17,uy+5),(ux+17,uy+5)],'#b2e4dc',2)
            by=obj('basin')['center'][1]
            for k in range(5):
                yy=uy+depth+((t*40+k*9)%(by-uy-depth))
                line(d,[(ux,yy),(ux,yy+3)],'#a9e5e0',2)
    return [x-31,y-82,x+32,y+3]

def frame(t):
    im=BASE.copy();d=ImageDraw.Draw(im);sun=e(q(t,29.8,33.5))
    if sun:
        # A warm sky gradient, no additive blowout on object textures.
        sky=Image.new('RGB',(W,285));sd=ImageDraw.Draw(sky)
        for yy in range(285):line(sd,[(0,yy),(W,yy)],tuple(round(mix(a,b,yy/285)) for a,b in zip((237,181,151),(247,213,173))))
        im.paste(Image.blend(im.crop((0,0,W,285)),sky,sun),(0,0));d=ImageDraw.Draw(im)
        for k,col in enumerate(['#d6929c','#e3b58e','#f0d397','#a8c5a3','#a5bac1']):
            d.arc((62+k*4,104+k*4,294-k*4,334-k*4),185,353,fill=col,width=3)
    cx,cy=obj('cloud')['center'];cx+=sun*80
    for dx,dy,rr in [(-29,9,21),(-10,-4,26),(17,3,24),(38,12,15)]:
        ell(d,(cx+dx-rr,cy+dy-rr/2,cx+dx+rr,cy+dy+rr/2),'#adb6c9',INK)
    rec(d,(cx-40,cy+9,cx+40,cy+20),'#adb6c9')
    line(d,[(cx-39,cy+20),(cx+36,cy+20)],'#747e9e')
    if t<29.8:
        rng=random.Random(91)
        for k in range(22):
            xx=cx+rng.randrange(-37,38);yy=cy+25+((t*85+k*27)%171)
            line(d,[(xx,yy),(xx-2,yy+7)],'#afdbdb',2)
    machines(im,t);clothes(im,t);bbox=rabbit(im,t)
    d=ImageDraw.Draw(im)
    # Foreground trim and little persistent puddle rings.
    for xx in (45,126,225,306):
        yy=490+2*math.sin(xx);rr=3+((t*2+xx)%6)
        d.arc((xx-rr,yy-2,xx+rr,yy+2),0,320,fill='#acc5c4')
    if t>29.8:
        for k in range(11):
            xx=46+(k*47)%275;yy=305+(k*31)%146+math.sin(t*2+k)*4
            if math.sin(t*3+k)>0.7:
                line(d,[(xx-2,yy),(xx+2,yy)],'#ffe6ad');line(d,[(xx,yy-2),(xx,yy+2)],'#ffe6ad')
    cxx,cyy,cw=path(t,S['camera_keys']);ch=cw*H/W
    left=max(0,min(W-cw,cxx-cw/2));top=max(0,min(H-ch,cyy-ch/2))
    box=(round(left),round(top),round(left+cw),round(top+ch))
    out=im.crop(box).resize(tuple(S['output_size']),Image.Resampling.NEAREST)
    sb=[(bbox[0]-left)/cw,(bbox[1]-top)/ch,(bbox[2]-left)/cw,(bbox[3]-top)/ch]
    return out,{'t':t,'world':S['world_id'],'camera':[left,top,cw,ch],'rabbit_world_bbox':bbox,'rabbit_normalized_bbox':sb}

def initialize(scene):
    global S, W, H, FPS, BASE
    S = scene
    W, H = S['logical_size']
    FPS = S['fps']
    BASE = background()
