"""A new clockwork garden story; shares drawing primitives with the rooftop assets.

The rooftop drawing stays untouched. This is a bounded starter scene, not a
text-to-video model. Palette and seed change its visual arrangement, not its plot.
"""
import copy
import math
import random
from PIL import Image, ImageDraw
from pixel_drawing import rec, ell, line, poly, gear, q, e, mix, path, INK
from pixel_engine import number

PALETTES = {
    'moon': {'sky': [(31,40,76),(110,117,151)], 'hills': ['#4f637b','#3c566b'],
             'leaf': ['#497f7b','#70a398','#a2c7aa'], 'petal': ['#f0bc8b','#e7a7a5','#a8cecf'], 'light': '#ffe4a4'},
    'dawn': {'sky': [(110,83,126),(237,182,151)], 'hills': ['#8b879e','#677c8c'],
             'leaf': ['#4f837f','#90b29a','#bad0a2'], 'petal': ['#f1c7a0','#dab1cd','#acc9dc'], 'light': '#fff0c2'},
    'forest': {'sky': [(29,61,76),(112,152,149)], 'hills': ['#4b7c80','#3b656b'],
               'leaf': ['#427c69','#76a47c','#b1ca96'], 'petal': ['#eeb69c','#e3c483','#b8c4d9'], 'light': '#fff0ae'},
}


def validate_garden(scene):
    if scene.get('schema_version') != 1 or scene.get('id') != 'moonlight-chimes':
        raise ValueError('Expected the moonlight-chimes starter schema.')
    if scene.get('logical_size') != [360,640] or scene.get('duration') != 32:
        raise ValueError('The garden story uses a 360x640 world and a 32-second timeline.')
    size=scene.get('output_size')
    if (not isinstance(size,list) or len(size)!=2 or any(type(v) is not int or not 64<=v<=4096 or v%2 for v in size)
            or size[0]*640!=size[1]*360):
        raise ValueError('Output needs even dimensions with a 9:16 aspect.')
    if type(scene.get('fps')) is not int or not 1<=scene['fps']<=60:
        raise ValueError('fps must be an integer in [1,60].')
    if scene.get('palette') not in PALETTES:
        raise ValueError('Unknown garden palette.')
    if type(scene.get('seed')) is not int or not 0<=scene['seed']<2**32:
        raise ValueError('seed must be an integer in [0, 2**32).')
    keys=scene.get('camera_keys')
    if not isinstance(keys,list) or len(keys)<2:raise ValueError('Camera path is required.')
    previous=-1
    for k in keys:
        if (not isinstance(k,list) or len(k)!=4 or not all(number(v) for v in k)
                or not previous<k[0]<=32 or not 0<=k[1]<=360 or not 0<=k[2]<=640 or not 0<k[3]<=360):
            raise ValueError('Invalid garden camera path.')
        previous=k[0]
    if keys[0][0]!=0 or keys[-1][0]!=32:raise ValueError('Camera must cover the whole story.')
    return scene


class GardenRenderer:
    def __init__(self,scene):
        self.scene=copy.deepcopy(validate_garden(scene));self.palette=PALETTES[scene['palette']]
        self.rng=random.Random(scene['seed']);self.base=self.background()
        self.flowers=[(79+self.rng.randrange(-6,7),338),(191,291+self.rng.randrange(-5,6)),(283+self.rng.randrange(-5,6),352)]

    def background(self):
        im=Image.new('RGB',(360,640));d=ImageDraw.Draw(im);p=self.palette
        for y in range(640):line(d,[(0,y),(360,y)],tuple(round(mix(a,b,y/640)) for a,b in zip(*p['sky'])))
        for _ in range(64):
            x=self.rng.randrange(14,347);y=self.rng.randrange(20,286)
            rec(d,(x,y,x+1,y+1),'#b9cbd1')
        ell(d,(248,57,300,109),'#e5d8b2');ell(d,(237,51,286,99),tuple(p['sky'][0]))
        for index,col in enumerate(p['hills']):
            yy=335+index*49
            poly(d,[(0,yy),(42,yy-48),(92,yy-12),(143,yy-57),(220,yy-25),(277,yy-66),(360,yy-22),(360,520),(0,520)],col,None)
        # A terraced garden, wooden deck and quiet stream live in one map.
        rec(d,(0,483,360,640),'#3c5c64');poly(d,[(0,541),(95,526),(173,558),(360,524),(360,640),(0,640)],'#507a80',None)
        for k in range(26):
            x=self.rng.randrange(360);y=self.rng.randrange(546,638)
            line(d,[(x,y),(x+self.rng.randrange(6,18),y)],'#8faeb0')
        poly(d,[(24,478),(322,478),(346,517),(8,517)],'#a88b85',INK,2)
        rec(d,(8,517,346,527),'#685f70',INK,2)
        for yy in (487,497,507):line(d,[(17,yy),(337,yy)],'#6d697b')
        for x in range(27,340,27):line(d,[(x,480),(x-9,516)],'#cab09b')
        for x in (28,312):
            rec(d,(x,527,x+9,605),'#6b6677',INK,2);rec(d,(x+2,528,x+4,604),'#b29b91')
            line(d,[(x-15,601),(x+21,601)],'#98b1ad',2)
        # A left cottage: shingles, windows, flower ledge and warm interior.
        rec(d,(9,343,65,477),'#8a8995',INK,2)
        poly(d,[(0,347),(34,315),(74,347)],'#9b787f',INK,2)
        for yy in (333,340):line(d,[(17-(yy-333),yy),(51+(yy-333),yy)],'#c6a19b')
        rec(d,(20,371,54,422),'#e2bb94',INK,2)
        rec(d,(24,376,50,415),'#a9b8b0',INK)
        line(d,[(37,373),(37,420)],'#6a6d7f',3);line(d,[(22,397),(52,397)],'#6a6d7f',3)
        rec(d,(15,422,59,430),'#ba9a90',INK);rec(d,(27,446,51,477),'#596776',INK,2)
        ell(d,(45,459,47,461),'#f4d4a0')
        # Right tree and overhead wood arch carry the bell flowers physically.
        poly(d,[(321,482),(326,275),(313,218),(322,182),(337,263),(349,478)],'#6e6d7b',INK,2)
        for yy in range(280,471,18):line(d,[(333,yy),(337,yy+8)],'#a49691')
        for x,y,r in [(304,197,32),(335,174,28),(350,218,29),(310,242,28),(337,255,23)]:
            ell(d,(x-r,y-r,x+r,y+r),p['leaf'][0],INK,2)
            for k in range(5):
                xx=x+math.cos(k*2.3)*r*.6;yy=y+math.sin(k*2.3)*r*.5
                line(d,[(xx-4,yy),(xx+4,yy)],p['leaf'][1],2)
        line(d,[(45,478),(45,238),(78,206),(286,206),(315,238),(315,478)],INK,9)
        line(d,[(45,478),(45,238),(78,206),(286,206),(315,238),(315,478)],'#b8a18e',5)
        for x in range(78,287,20):line(d,[(x,203),(x+5,209)],'#e0c5a5',2)
        for side in (25,333):
            for yy in range(510,588,11):
                line(d,[(side,yy),(side+4,yy+14)],p['leaf'][0],2)
                ell(d,(side-7,yy-3,side,yy+5),p['leaf'][1],INK)
                ell(d,(side+1,yy+3,side+8,yy+10),p['leaf'][2],INK)
        for x in (60,295):
            rec(d,(x-18,464,x+18,481),'#b48279',INK,2);rec(d,(x-20,460,x+20,466),'#d1a993',INK)
        return im

    def rabbit(self,im,t,crank):
        x=mix(87,117,e(q(t,1,4))) if t<13 else mix(117,108,e(q(t,13,15)))
        y=500-(abs(math.sin(t*9))*2 if 1<t<4 else 0)
        d=ImageDraw.Draw(im)
        # Same cream rabbit, teal overalls and coral scarf as the bundled cast.
        ell(d,(x-19,y-2,x+19,y+3),'#6a657d')
        poly(d,[(x-10,y-36),(x-28,y-28+math.sin(t*5)*3),(x-25,y-22),(x-8,y-29)],'#d97f7c',INK)
        ell(d,(x-21,y-25,x-10,y-13),'#e5deca',INK,2)
        for side in (-1,1):
            dx=side*8+(side*3*math.sin(t*9) if 1<t<4 else 0)
            ell(d,(x+dx-7,y-10,x+dx+6,y),'#c08c70',INK,2)
            line(d,[(x+dx-4,y-3),(x+dx+4,y-3)],'#edbf8f')
        poly(d,[(x-13,y-35),(x+12,y-35),(x+17,y-10),(x-15,y-10)],'#ede4ce',INK,2)
        poly(d,[(x-9,y-33),(x+9,y-33),(x+12,y-12),(x-11,y-12)],'#73a4a0',INK)
        rec(d,(x-5,y-23,x+6,y-16),'#a8c9b9',INK)
        for side in (-1,1):
            ex=x+side*9;tip=side*(2+2*math.sin(t*2))
            poly(d,[(ex-6,y-53),(ex-6+tip,y-76),(ex-1+tip,y-81),(ex+5+tip,y-77),(ex+6,y-52)],'#f2e9d4',INK,2)
            line(d,[(ex+tip,y-74),(ex,y-57)],'#dba8a0',3)
        ell(d,(x-21,y-61,x+21,y-30),'#f6edda',INK,2)
        for dx in (-14,14):ell(d,(x+dx-3,y-44,x+dx+3,y-39),'#e7b2a4')
        blink=int(t*24)%103 in (0,1,2)
        for xx in (x-9,x+9):
            if blink or t>25:line(d,[(xx-3,y-47),(xx,y-49),(xx+3,y-47)],INK,2)
            else:rec(d,(xx-2,y-50,xx+1,y-45),INK);rec(d,(xx-1,y-50,xx-1,y-49),'#fff5dc')
        poly(d,[(x-3,y-43),(x+3,y-43),(x,y-40)],'#af7a7c',None)
        line(d,[(x,y-40),(x-3,y-37)],INK);rec(d,(x-13,y-33,x+13,y-29),'#d97f7c',INK)
        reach=e(q(t,3.5,4));release=e(q(t,12,13))
        hand=(mix(x+17,crank[0],reach*(1-release)),mix(y-22,crank[1],reach*(1-release)))
        other=(x-16,y-22)
        if t>25:hand=(x+24,y-43-math.sin(t*5)*4);other=(x-22,y-43+math.sin(t*5)*4)
        for shoulder,target in [((x+11,y-29),hand),((x-11,y-29),other)]:
            line(d,[shoulder,target],INK,7);line(d,[shoulder,target],'#e9dfc9',5)
            ell(d,(target[0]-3,target[1]-3,target[0]+3,target[1]+3),'#f7ead4',INK)
        return [x-31,y-82,x+32,y+3],hand

    def frame(self,t):
        if not number(t) or not 0<=t<32:raise ValueError('Frame time must be within the story.')
        im=self.base.copy();d=ImageDraw.Draw(im);p=self.palette
        charge=q(t,4,12);running=q(t,12,14);a=(t-4)*math.pi if t<12 else 8*math.pi+(t-12)*2.4
        # A wind-up box, visible spring, 4 persistent charge lights and drive shaft.
        rec(d,(146,425,219,481),'#9f7f79',INK,2);rec(d,(149,430,216,475),'#d5b391',INK)
        rec(d,(158,435,208,466),'#4a596a',INK,2)
        coil=[]
        for k in range(150):
            u=k/149;z=u*math.tau*(2+4*charge)
            coil.append((183+u*19*math.cos(z),451+u*11*math.sin(z)))
        line(d,coil,'#f0ce8f',1)
        for k in range(4):
            ell(d,(153+k*17,469,161+k*17,477),p['light'] if charge>=(k+1)/4 else '#817a81',INK)
        gear(d,181,421,17,a*running,'#c6b089');gear(d,205,410,11,-a*running,'#8eaca3')
        line(d,[(181,403),(181,218)],INK,6);line(d,[(181,403),(181,218)],'#b5aa91',3)
        for y in range(239,401,16):
            line(d,[(178,y),(184,y+6)],'#e5cfa5' if running else '#8d9295',2)
        crank=(141+10*math.cos(a),450+10*math.sin(a)) if 4<=t<=12 else (151,450)
        line(d,[(154,448),(141,450),crank],INK,5);line(d,[(154,448),(141,450),crank],'#dab68e',3)
        # Bell shells unfold at distinct beats, leaving their new state in place.
        blooms=[]
        for j,(x,y) in enumerate(self.flowers):
            opening=e(q(t,14+j*3,17+j*3));blooms.append(opening)
            swing=math.sin((t-16-j*3)*4)*4*opening
            line(d,[(181,218),(x,218),(x,y-29)],INK,4)
            line(d,[(181,218),(x,218),(x,y-29)],'#d8b78f',2)
            gear(d,x,218,9,a*running*(-1 if j%2 else 1),'#a9b6a0')
            line(d,[(x,y+23),(x,470)],INK,5);line(d,[(x,y+23),(x,470)],p['leaf'][1],3)
            for side in (-1,1):
                poly(d,[(x,y+71),(x+side*(13+8*opening),y+57),(x+side*22,y+73),(x,y+80)],p['leaf'][1],INK)
            for k in range(8):
                z=k*math.tau/8;rr=13+25*opening
                u,v=math.cos(z),math.sin(z)
                poly(d,[(x+u*8-v*5,y+v*8+u*5),(x+u*(rr-6)-v*9,y+v*(rr-6)+u*9),
                        (x+u*(rr+9),y+v*(rr+9)),(x+u*(rr-6)+v*9,y+v*(rr-6)-u*9),
                        (x+u*8+v*5,y+v*8-u*5)],p['petal'][j],INK,2)
                line(d,[(x+u*16,y+v*16),(x+u*(rr+3),y+v*(rr+3))],'#f8dec0')
            ell(d,(x-13,y-13,x+13,y+13),'#ae927a',INK,2)
            ell(d,(x-8,y-8,x+8,y+8),p['light'] if opening>.8 else '#6f7985',INK)
            line(d,[(x,y+9),(x+swing,y+29)],INK,2)
            ell(d,(x+swing-4,y+26,x+swing+4,y+34),'#d3b78f',INK)
            if opening>.9:
                # Short ripples originate at the moving bell clapper.
                phase=(t*1.5+j)%1;r=13+phase*16
                d.arc((x-r,y-r,x+r,y+r),20,70,fill='#e4d8b5',width=1)
                d.arc((x-r,y-r,x+r,y+r),110,160,fill='#e4d8b5',width=1)
        # A folding copper bird on the top spindle opens into a mobile.
        opened=e(q(t,23,27));bx=181;by=180
        line(d,[(181,218),(181,by+12)],INK,4)
        line(d,[(181,218),(181,by+12)],'#d3b78f',2)
        ell(d,(bx-9,by-9,bx+9,by+9),'#d7b18e',INK)
        for side in (-1,1):
            poly(d,[(bx+side*5,by),(bx+side*(12+30*opened),by-5-12*opened),
                    (bx+side*(17+21*opened),by+7),(bx+side*5,by+9)],'#a3c7bb',INK,2)
        ell(d,(bx+2,by-4,bx+4,by-2),INK)
        poly(d,[(bx+8,by-1),(bx+14,by+2),(bx+8,by+4)],'#f0ce8f',INK)
        for k in range(3):
            z=t*.5+k*math.tau/3;xx=181+math.cos(z)*(16+26*opened);yy=198+math.sin(z)*7
            if opened:
                line(d,[(181,by+12),(xx,yy)],'#c4b28f')
                poly(d,[(xx-7,yy),(xx,yy-4-4*math.sin(t*5+k)),(xx+7,yy),(xx,yy+4)],p['petal'][k],INK)
        bbox,hand=self.rabbit(im,t,crank)
        # Persistent small flowers and fireflies join only after the mechanism works.
        d=ImageDraw.Draw(im);joy=e(q(t,24,28))
        for x in (60,295):
            for j in range(3):
                xx=x-11+j*11;yy=457-(8+18*joy)
                line(d,[(xx,462),(xx,yy)],p['leaf'][1],2)
                for k in range(5):
                    z=k*math.tau/5;ell(d,(xx+4*math.cos(z)-2,yy+4*math.sin(z)-2,xx+4*math.cos(z)+2,yy+4*math.sin(z)+2),p['petal'][j],INK)
                ell(d,(xx-2,yy-2,xx+2,yy+2),p['light'])
        for k in range(13):
            x=38+(k*47)%286+math.sin(t*.8+k)*7;y=315+(k*31)%165+math.cos(t+k)*6
            if joy and math.sin(t*3+k)>.2:
                rec(d,(x-1,y-1,x+1,y+1),p['light']);line(d,[(x-3,y),(x+3,y)],p['light'])
        cx,cy,cw=path(t,self.scene['camera_keys']);ch=cw*640/360
        left=max(0,min(360-cw,cx-cw/2));top=max(0,min(640-ch,cy-ch/2))
        box=tuple(round(v) for v in (left,top,left+cw,top+ch))
        out=im.crop(box).resize(tuple(self.scene['output_size']),Image.Resampling.NEAREST)
        return out,{'t':t,'world':'GARDEN-STARTER','camera':[left,top,cw,ch],
                    'rabbit_world_bbox':bbox,'rabbit_normalized_bbox':[(bbox[0]-left)/cw,(bbox[1]-top)/ch,(bbox[2]-left)/cw,(bbox[3]-top)/ch],
                    'spring_charge':charge,'flower_openings':blooms,'bird_opening':opened,
                    'crank_world':list(crank),'right_hand_world':list(hand),'seed':self.scene['seed']}
