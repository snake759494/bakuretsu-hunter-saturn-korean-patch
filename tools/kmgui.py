"""MGAME_DT (flag game) sprite labels -> Korean."""
import os,sys,numpy as np
sys.path.insert(0,os.path.dirname(__file__))
from kslotui import g4,p4,mask,dil
from kname import render,F9
def gal(s):
    img,W=render(s,F9,12);m=img[:, :W]>0
    ys=np.nonzero(m.any(1))[0];return m[ys.min():ys.max()+1]
def put(a,m,x,y,v):
    h,w=m.shape;sub=a[y:y+h,x:x+w];sub[m[:sub.shape[0],:sub.shape[1]]]=v
def heal(a,clr,txt):
    H,W=a.shape
    for y,x in zip(*np.nonzero(clr)):
        v=0
        for k in range(1,12):
            for xx in (x-k,x+k):
                if 0<=xx<W and not clr[y,xx] and a[y,xx] not in txt: v=a[y,xx];break
            else: continue
            break
        a[y,x]=v
def controller(t,p=0x8380):
    a=g4(t,p,176,96);o=a.copy();clr=np.zeros_like(a,bool)
    for col,(kx0,kx1),(sx0,sx1) in ((15,(5,19),(32,69)),(14,(112,123),(135,173))):
        top=(o==col)
        clr[5:18,kx0:kx1]|=top[5:18,kx0:kx1]; clr[5:18,sx0:sx1]|=top[5:18,sx0:sx1]
        sh=np.zeros_like(clr);sh[77:90]=top[5:18]
        clr[77:90,kx0:kx1]|=sh[77:90,kx0:kx1]
        g0=sx0+12
        clr[77:91,sx0:g0]|=(o[77:91,sx0:g0]==col)
        clr[77:90,g0:sx1]|=sh[77:90,g0:sx1]
    heal(a,clr,(14,15))
    for col,kx,sx,(k,u,d) in ((15,5,33,('홍','올려','내려')),(14,112,137,('백','올려','내려'))):
        for y0,s in ((6,u),(78,d)):
            g=gal(k);put(a,g,kx+(13-g.shape[1])//2,y0,col)
            g=gal(s);put(a,g,sx,y0,col)
    p4(t,p,a)
def big(t,p,w,h,ch,fill,outl,x0,x1,y0,y1,size,font='NanumSquareNeo-eHv.ttf',keep=()):
    a=g4(t,p,w,h)
    for y in range(y0,y1):
        for x in range(x0,x1):
            if a[y,x] not in keep: a[y,x]=a[y,x] if False else 0
    m=mask(ch,x1-x0,y1-y0,size,font=font);o=dil(m)&~m
    sub=a[y0:y1,x0:x1];sub[o]=outl;sub[m]=fill
    p4(t,p,a)
def bar(t,p,w,h,s,fill,bg,x0,x1,size=12,font='NanumSquareNeo-eHv.ttf',y0=1,y1=None):
    a=g4(t,p,w,h);y1=y1 or h-1
    a[y0:y1,x0:x1]=bg
    m=mask(s,x1-x0,y1-y0,size,font=font)
    sub=a[y0:y1,x0:x1];sub[m]=fill
    p4(t,p,a)
def apply(t):
    controller(t)
    big(t,0x5160,24,32,'홍',9,0xa,0,24,2,30,22)
    big(t,0x4fc0,24,32,'백',1,0xa,0,24,2,30,22)
    big(t,0x5880,32,24,'미스',8,2,0,32,2,22,14)
    big(t,0x5f00,16,16,'점',8,3,0,16,0,16,14)
    big(t,0x5fa0,16,16,'회',8,3,0,16,0,16,14)
    big(t,0x6120,32,24,'남은',8,2,0,32,0,15,12)
    bar(t,0x5bc0,48,16,'첫째',15,0xb,1,47)
    bar(t,0x5d60,48,16,'둘째',15,0xb,1,47)
    bar(t,0x5300,56,24,'청팀',15,0xc,15,53,14,y0=3,y1=21)
    bar(t,0x55c0,56,24,'홍팀',15,9,4,44,14,y0=3,y1=21)
