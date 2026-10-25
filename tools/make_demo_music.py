"""Synthesize the project's original 44-second demo score using only the standard library."""
from array import array
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import wave

SR=22050
DURATION=44
BPM=120
BEAT=60/BPM


def compose():
    count=SR*DURATION
    left=array('f',[0])*count;right=array('f',[0])*count
    def note(midi,start,length,gain,pan=0,tone='bell'):
        freq=440*2**((midi-69)/12)
        a=max(0,round(start*SR));n=min(round(length*SR),count-a)
        for i in range(n):
            t=i/SR;u=t/length
            attack=min(1,t/.012);release=min(1,max(0,(length-t)/.07))
            phase=math.tau*freq*t
            if tone=='pad':
                signal=(math.sin(phase)+.17*math.sin(phase*2))*.7
                env=math.sin(math.pi*u)**.65
            elif tone=='bass':
                signal=(math.sin(phase)+.16*math.sin(phase*3))*.8
                env=attack*math.exp(-t*2)*release
            else:
                signal=(math.sin(phase)+.23*math.sin(phase*2)+.10*math.sin(phase*3))*.72
                env=attack*math.exp(-t*4.5)*release
            value=signal*gain*env
            left[a+i]+=value*(1-pan*.35);right[a+i]+=value*(1+pan*.35)
    # A new score authored for this project, independent of the previous recording.
    chords=[(55,59,62),(50,57,62),(52,55,59),(48,55,60)]
    motifs=[[0,2,4,2,1,3,2,0],[2,4,5,4,2,1,0,2],
            [4,3,2,0,1,2,4,5],[5,4,2,3,1,0,2,0]]
    scale=[67,69,71,72,74,76,78,79]
    rng=random.Random(20261025)
    for bar in range(22):
        start=bar*2;chord=chords[bar%4]
        section=0 if start<4 else (1 if start<20 else 2)
        for k,midi in enumerate(chord):note(midi+12,start,1.95,.035,-.5+k*.5,'pad')
        for k in range(4):
            note(chord[0]-12+(12 if k==2 else 0),start+k*.5,.39,.11,0,'bass')
        motif=motifs[(bar//2+bar%2)%4]
        for k,degree in enumerate(motif):
            if section==0 and k%2:continue
            note(scale[degree],start+k*.25,.30,.10 if section else .065,math.sin(bar+k)*.6)
        if section==2:
            for k in range(4):note(chord[k%3]+24,start+k*.5+.125,.28,.035,.6*(-1 if k%2 else 1))
        if start>=4:
            for k in range(8):
                a=round((start+k*.25)*SR)
                for i in range(min(round(.035*SR),count-a)):
                    value=(rng.random()*2-1)*math.exp(-i/(SR*.009))*.018
                    left[a+i]+=value;right[a+i]+=value
            for k in (0,2):
                a=round((start+k*.5)*SR)
                for i in range(min(round(.16*SR),count-a)):
                    t=i/SR
                    value=math.sin(math.tau*(54*t+30*.018*(1-math.exp(-t/.018))))*math.exp(-t*24)*.09
                    left[a+i]+=value;right[a+i]+=value
    peak=max(max(abs(v) for v in left),max(abs(v) for v in right))
    gain=.68/peak
    pcm=array('h')
    for i,(a,b) in enumerate(zip(left,right)):
        t=i/SR;fade=min(1,t/.12,max(0,(DURATION-t)/1.6))
        pcm.extend((round(a*gain*fade*32767),round(b*gain*fade*32767)))
    if sys.byteorder!='little':pcm.byteswap()
    return pcm


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists():raise FileExistsError('Choose a new output file.')
    pcm=compose();args.out.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(args.out),'wb') as stream:
        stream.setnchannels(2);stream.setsampwidth(2);stream.setframerate(SR);stream.writeframes(pcm.tobytes())
    print(json.dumps(dict(duration=DURATION,sample_rate=SR,channels=2,bpm=BPM,
        sha256=hashlib.sha256(args.out.read_bytes()).hexdigest(),origin='Original procedural score for ai-video-marker',license='MIT'),indent=2))


if __name__=='__main__':main()
