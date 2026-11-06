import sys,struct
from PIL import Image
v=open(sys.argv[1]+'.v2','rb').read(); cr=open(sys.argv[1]+'.cram','rb').read()
def col(i):
    c=struct.unpack('>H',cr[i*2:i*2+2])[0]; return ((c&31)<<3,((c>>5)&31)<<3,((c>>10)&31)<<3)
def render(mapaddr,bpp,suppl,cnum_shift,out,palbase=0,W=32,H=32):
    im=Image.new('RGB',(W*16,H*16))
    for ty in range(H):
        for tx in range(W):
            pn=struct.unpack('>H',v[mapaddr+(ty*W+tx)*2:mapaddr+(ty*W+tx)*2+2])[0]
            cn=((suppl&0x1f)<<10|(pn&0xfff)) if bpp==4 else (((suppl&0x1c)<<10)|(pn&0xfff))
            pal=(pn>>12)&0xf
            cn<<=cnum_shift  # unit in cells? 
            base=cn*32
            for cy in range(2):
                for cx in range(2):
                    cell=base+(cy*2+cx)*(32 if bpp==4 else 64)
                    for y in range(8):
                        for x in range(8):
                            if bpp==4:
                                b=v[(cell+y*4+x//2)&0x7ffff]; p=(b>>4) if x%2==0 else b&15
                                c=col(pal*16+p+palbase) if p else (0,0,0)
                            else:
                                p=v[(cell+y*8+x)&0x7ffff]; c=col(((pal&0x7)<<8)+p+palbase) if p else (0,0,0)
                            im.putpixel((tx*16+cx*8+x,ty*16+cy*8+y),c)
    im.save(out)
mapaddr=int(sys.argv[2],16);bpp=int(sys.argv[3]);suppl=int(sys.argv[4],16);sh=int(sys.argv[5])
render(mapaddr,bpp,suppl,sh,sys.argv[6])
