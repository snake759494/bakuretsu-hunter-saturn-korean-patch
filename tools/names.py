import json,struct,glob,os
from PIL import Image
import numpy as np
s=json.load(open('scan2.json'))
def u16(m,i): return struct.unpack('>H',m[i:i+2])[0]
def tile(d,t):
    off=0x1104+(t-0x380)*0x80; blk=d[off:off+0x80];P=np.zeros((16,16),np.uint8)
    for y in range(16):
        for x in range(16):
            c=(y//8)*2+(x//8); b=blk[c*32+(y%8)*4+(x%8)//2]; P[y,x]=(b>>4) if x%2==0 else b&15
    return P
out={}
for nm,e in s.items():
    m=open('disc/PRG/MEN'+nm+'.BIN','rb').read()
    # find run of groups (a,b,c,ffff) with a in 0x380..0x3ff or 0
    best=None
    for st in range(0,len(m)-16,2):
        k=0
        while True:
            g=[u16(m,st+k*8+j*2) for j in range(4)]
            if g[3]==0xffff and all(x==0 or 0x380<=x<0x400 for x in g[:3]): k+=1
            else: break
        if k>=5 and (best is None or k>best[1]): best=(st,k)
    st,k=best
    groups=[[u16(m,st+i*8+j*2) for j in range(3)] for i in range(k)]
    out[nm]=dict(off=st,groups=groups)
json.dump(out,open('names.json','w'))
