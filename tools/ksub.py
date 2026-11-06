import numpy as np,sys
sys.path.insert(0,'tools')
from kname import bdf,F7,F9
def textmask(s,F=F7,asc=None):
    W=sum(F[ord(c)][0] if ord(c) in F else 4 for c in s);H=12;img=np.zeros((H,W+2),bool);x=1
    for ch in s:
        if ord(ch) not in F: x+=4;continue
        dw,(w,h,ox,oy),rows,bits=F[ord(ch)]
        for r,v in enumerate(rows):
            y=10-oy-h+r
            for b in range(w):
                if v>>(bits-1-b)&1 and 0<=y<H: img[y,x+ox+b]=True
        x+=dw
    ys,xs=np.nonzero(img);return img[ys.min():ys.max()+1,xs.min():xs.max()+1]
def dil(m):
    o=np.pad(m,1);r=o.copy()
    for dy in (-1,0,1):
        for dx in (-1,0,1): r|=np.roll(np.roll(o,dy,0),dx,1)
    return r
def overlay(P,s,x,y,fg,ol,F=F7,anchor='tl'):
    m=textmask(s,F);O=dil(m);h,w=O.shape
    if anchor=='br': x-=w;y-=h
    sub=P[y:y+h,x:x+w];sub[O[:sub.shape[0],:sub.shape[1]]]=ol
    mm=np.pad(m,1)[:sub.shape[0],:sub.shape[1]];sub[mm]=fg;return (x,y,w,h)
