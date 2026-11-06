import json
from PIL import Image
import numpy as np
sc=json.load(open('scenes.json')); G=open('glyphs.bin','rb').read()
def gimg(gid):
    blk=G[gid*0x80:gid*0x80+0x80];P=np.zeros((16,16),np.uint8)
    for y in range(16):
        for x in range(16):
            c=(y//8)*2+(x//8); b=blk[c*32+(y%8)*4+(x%8)//2]; P[y,x]=1 if ((b>>4) if x%2==0 else b&15) else 0
    return P
cache={}
lines=[];k=0
for nm,e in sc.items():
    if nm.endswith('M'): continue
    for mi,mm in enumerate(e['msgs']):
        cur=[]
        for w in mm['w']+[0xfffe]:
            if w>=0xff00:
                gl=[e['gmap'][x] for x in cur if x!=0]
                if len(gl)>=1:
                    lines.append(dict(sc=nm,m=mi,g=gl));
                cur=[]
            else: cur.append(w)
print(len(lines))
for i,l in enumerate(lines):
    n=len(l['g']);S=3;pad=24
    im=np.full((16*S+pad*2,(16*n)*S+pad*2),255,np.uint8)
    for j,gid in enumerate(l['g']):
        if gid not in cache: cache[gid]=gimg(gid)
        P=np.kron(cache[gid],np.ones((S,S),np.uint8))
        im[pad:pad+16*S,pad+j*16*S:pad+(j+1)*16*S]=255-P*255
    Image.fromarray(im).save(f'ocr/{i:05d}.png')
json.dump(lines,open('lines.json','w'))
