import struct,numpy as np
from PIL import Image
def decode(d):
    v=bytes(d[4:0xc704]);pal=[struct.unpack('>H',d[0xc704+i*2:0xc706+i*2])[0] for i in range(256)]
    # map: 20x14 chars of 16px, sequential by row? use VRAM map from dump
    return v,pal
def cellimg(v,mp):
    H,W=len(mp),len(mp[0]);idx=np.zeros((H*16,W*16),np.uint8)
    for ty in range(H):
        for tx in range(W):
            base=(mp[ty][tx]&0x3ff)*0x80
            for cy in range(2):
                for cx in range(2):
                    cell=base+(cy*2+cx)*64;idx[ty*16+cy*8:ty*16+cy*8+8,tx*16+cx*8:tx*16+cx*8+8]=np.frombuffer(v[cell:cell+64],np.uint8).reshape(8,8)
    return idx
def rgb(idx,pal):
    im=Image.new('RGB',(idx.shape[1],idx.shape[0]));im.putdata([((c&31)<<3,(c>>5&31)<<3,(c>>10&31)<<3) for p in idx.flatten() for c in [pal[p]]]);return im
def setpix(d,mp,x,y,val):
    ty,tx=y//16,x//16;base=(mp[ty][tx]&0x3ff)*0x80;cy,cx=(y%16)//8,(x%16)//8
    d[4+base+(cy*2+cx)*64+(y%8)*8+(x%8)]=val
def patch(d,mp,sub=True,box=True):
    import sys;sys.path.insert(0,'tools')
    import kmenu,ksub
    v,_=decode(d);I=cellimg(v,mp)
    if box:
        m=kmenu.mask('세이브 중',13,64,32,100);F=kmenu.place(m,62,30,0,62,0,30)
        for y in range(30):
            for x in range(62): setpix(d,mp,129+x,129+y,88 if F[y,x] else 193)
    if sub:
        P=I.copy();r=ksub.overlay(P,'폭렬헌터',303,223,193,1,anchor='br')
        x0,y0,w,h=r
        for y in range(y0,y0+h):
            for x in range(x0,x0+w):
                if P[y,x]!=I[y,x]: setpix(d,mp,x,y,int(P[y,x]))
