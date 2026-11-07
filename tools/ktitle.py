"""Chapter title cards (8bpp 16x16-char NBG images inside DAT/Sx_01.BIN).
Layout: [chars][map 32x32 1-word @p][palette 256 @p+0x800]; char pn at p-(max+2)*0x80+pn*0x80."""
import os,struct,numpy as np
from PIL import Image,ImageDraw,ImageFont
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT=os.path.join(os.path.dirname(W),'NanumSquareNeo-cBd.ttf')
T={'S1_01':(0x37a04,'목숨 거두소서, 붉은 꽃'),'S2_01':(0x3b504,'그림자와 빛의 불문율'),
   'S3_01':(0x13f04,'사랑, 흐르는 대로'),'S4_01':(0x37904,'미궁의 오페라하우스'),'S5_01':(0x49504,'이단의 사랑은 크리스탈')}
def _map(d,p): return np.frombuffer(bytes(d[p:p+0x800]),'>u2').reshape(32,32).astype(int)[:14,:20]
def decode(d,p):
    m=_map(d,p);c0=p-(m.max()+2)*0x80;img=np.zeros((224,320),np.uint8)
    for ty in range(14):
        for tx in range(20):
            a=c0+m[ty,tx]*0x80
            for k in range(4):
                c=a+k*64;img[ty*16+(k//2)*8:ty*16+(k//2)*8+8,tx*16+(k%2)*8:tx*16+(k%2)*8+8]=np.frombuffer(bytes(d[c:c+64]),np.uint8).reshape(8,8)
    raw=struct.unpack('>256H',bytes(d[p+0x800:p+0xa00]))
    pal=np.array([[(((c>>s)&31)<<3) for s in (0,5,10)] for c in raw],np.int32)
    return m,c0,img,pal
def encode(d,p,m,c0,img):
    done={}
    for ty in range(14):
        for tx in range(20):
            t=img[ty*16:ty*16+16,tx*16:tx*16+16];pn=m[ty,tx]
            if pn in done:
                if not np.array_equal(done[pn],t): print('shared char conflict',ty,tx)
                continue
            done[pn]=t;a=c0+pn*0x80
            for k in range(4):
                c=a+k*64;d[c:c+64]=t[(k//2)*8:(k//2)*8+8,(k%2)*8:(k%2)*8+8].tobytes()
def textmask(rgb): return (rgb[...,2]>=40)&(rgb[...,1]>=40)
def apply(get,put=None):
    data={n:get('DAT/%s.BIN'%n) for n in T}
    dec={n:decode(data[n],T[n][0]) for n in T}
    rgbs={n:dec[n][3][dec[n][2]] for n in T}
    masks={}
    for n in T:
        mk=textmask(rgbs[n]);mk[:,:]=np.maximum.reduce([np.roll(np.roll(mk,dy,0),dx,1) for dy in (-2,-1,0,1,2) for dx in (-2,-1,0,1,2)]);masks[n]=mk
    for n in T:
        p,s=T[n];m,c0,img,pal=dec[n];rgb=rgbs[n].astype(float);mk=masks[n]
        bg=rgb.copy();need=mk.copy()
        for o in T:
            if o==n: continue
            ok=need&~masks[o];bg[ok]=rgbs[o][ok];need&=~ok
        known=~need
        for it in range(400):          # diffusion inpaint of what no other card shows
            acc=np.zeros_like(bg);cnt=np.zeros(bg.shape[:2])
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                k=np.roll(np.roll(known,dy,0),dx,1);acc+=np.roll(np.roll(bg,dy,0),dx,1)*k[...,None];cnt+=k
            upd=need&(cnt>0);bg[upd]=acc[upd]/cnt[upd][:,None]
            if it<200: known=known|upd
        ys,xs=np.where(mk);cy=(ys.min()+ys.max())/2+4
        f=ImageFont.truetype(FONT,26);size=26
        while f.getlength(s)>296: size-=1;f=ImageFont.truetype(FONT,size)
        al=Image.new('L',(320,224));ImageDraw.Draw(al).text((160,cy),s,font=f,fill=255,anchor='mm')
        a=np.array(al,float)[...,None]/255
        out=bg*(1-a)+255*a
        # nearest palette index (skip colour 0 = transparent)
        P=pal[1:].astype(float);flat=out.reshape(-1,3)
        idx=np.argmin(((flat[:,None,:]-P[None])**2).sum(2),1)+1
        new=idx.reshape(224,320).astype(np.uint8)
        new[~(mk|(a[...,0]>0))]=img[~(mk|(a[...,0]>0))]
        encode(data[n],p,m,c0,new)
        Image.fromarray(pal[new].astype(np.uint8)).save(os.path.join(W,'shots','kt_%s.png'%n)) if os.path.isdir(os.path.join(W,'shots')) else None
        if put: put('DAT/%s.BIN'%n,bytes(data[n]))
