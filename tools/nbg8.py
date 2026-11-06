import sys,struct,numpy as np
from PIL import Image
def render(v,cr,mapaddr,W=32,H=16,pbase=0):
    img=np.zeros((H*16,W*16),np.uint16);idx=np.zeros((H*16,W*16),np.uint8)
    for ty in range(H):
        for tx in range(W):
            pn=struct.unpack('>H',v[mapaddr+(ty*32+tx)*2:][:2])[0];cn=(pn&0x3ff)|((pn>>10&3)<<10 if 0 else 0)
            base=(pn&0x3ff)*0x80
            for cy in range(2):
                for cx in range(2):
                    cell=base+(cy*2+cx)*64;a=np.frombuffer(v[cell:cell+64],np.uint8).reshape(8,8)
                    idx[ty*16+cy*8:ty*16+cy*8+8,tx*16+cx*8:tx*16+cx*8+8]=a
    return idx
if __name__=='__main__':
    n=sys.argv[1];v=open(f'shots/{n}.v2','rb').read();cr=open(f'shots/{n}.cram','rb').read()
    idx=render(v,cr,int(sys.argv[2],16))
    pal=[struct.unpack('>H',cr[i*2:i*2+2])[0] for i in range(1024)];off=int(sys.argv[3],16) if len(sys.argv)>3 else 0
    im=Image.new('RGB',(idx.shape[1],idx.shape[0]));im.putdata([((c&31)<<3,(c>>5&31)<<3,(c>>10&31)<<3) for p in idx.flatten() for c in [pal[off+p]]])
    im.save(f'shots/{n}_nbg.png')
