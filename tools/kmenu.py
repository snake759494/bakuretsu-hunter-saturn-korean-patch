import sys,numpy as np
sys.path.insert(0,'tools')
from tit import *
from PIL import ImageFont,ImageDraw
FT='../NanumSquareNeo-eHv.ttf'
def mask(s,size,W,H,thr=110):
    f=ImageFont.truetype(FT,size);im=Image.new('L',(W*2,H*2));d=ImageDraw.Draw(im)
    d.text((2,2),s,font=f,fill=255);a=np.array(im)>thr
    ys,xs=np.nonzero(a);a=a[ys.min():ys.max()+1,xs.min():xs.max()+1];return a
def dil(m):
    o=m.copy();o[1:]|=m[:-1];o[:-1]|=m[1:];o[:,1:]|=m[:,:-1];o[:,:-1]|=m[:,1:];return o
def place(m,W,H,x0,x1,y0,y1):
    out=np.zeros((H,W),bool);h,w=m.shape;x=x0+(x1-x0-w)//2;y=y0+(y1-y0-h)//2;out[y:y+h,x:x+w]=m;return out
def button(t,off,s,size,bar,sp=0,fn='../NanumSquareNeo-dEb.ttf'):
    P=get(t,off,80,16);B=np.zeros_like(P)
    if bar:
        for y in range(16):
            r=[v for v in P[y] if 3<=v<=6]
            if r:
                v=max(set(r),key=r.count);xs=[x for x in range(80) if 3<=P[y,x]<=6]
                B[y,min(xs):max(xs)+1]=v
                # rounded ends keep original
                for x in range(80):
                    if 3<=P[y,x]<=6: B[y,x]=P[y,x]
    global FT;FT=fn;m=mask(s,size,80,16,90);FT='../NanumSquareNeo-eHv.ttf'
    if sp: # letterspacing via per-char
        pass
    F=place(m,80,16,0,80,1,15);O1=dil(F);O2=dil(O1)
    N=B.copy();N[O2]=2;N[O1]=1;N[F]=15;put(t,off,N)
def wood(t,off,w,h,s,size,x0,x1,y0,y1,TX=(15,14,11)):
    P=get(t,off,w,h);T=np.isin(P,TX);T[:, :x0]=False;T[:,x1:]=False
    N=P.copy()
    for y in range(h):
        for x in range(w):
            if T[y,x]:
                for k in [d*j for j in (23,37,51,11,7,61,3,90,120,150) for d in (1,-1)]:
                    xx=x+k
                    if 1<=xx<w-1 and not T[y,xx]: N[y,x]=P[y,xx];break
    m=mask(s,size,w,h);F=place(m,w,h,x0,x1,y0,y1);N[F]=15;put(t,off,N)
def build(t):
    import ksub
    L=np.frombuffer(bytes(t[0x200:0x200+232*72]),np.uint8).reshape(72,232).copy()
    ksub.overlay(L,'폭렬헌터',232,66,255,52,anchor='br');t[0x200:0x200+232*72]=L.tobytes()
    for off,s,bar in [(0x4ca0,'시작',1),(0x4f40,'옵션',1),(0xe700,'스테레오',1),(0xe9a0,'모노',1),(0xdf20,'음성',1),(0xe1c0,'텍스트',1),(0xe460,'사운드',0),(0xdc80,'메시지',0)]:
        button(t,off,s,12,bar)
    for off,s in [(0x88a0,'로드'),(0x8bc0,'복사'),(0x8ee0,'삭제')]:
        wood(t,off,64,24,s,16,2,63,2,21)
    wood(t,0x6860,256,32,'처음부터',19,62,200,8,28)
    wood(t,0x5840,256,32,'스테이지',16,60,137,8,28)
    wood(t,0x5840,256,32,'장',15,140,170,8,28)
if __name__=='__main__':
    t=bytearray(open(T,'rb').read());build(t)
    L=[('ti',0x4ca0,80,16,0x350),('ti',0x4f40,80,16,0x360),('op',0xe460,80,16,0x3b0),('op',0xe700,80,16,0x3d0),('op',0xe9a0,80,16,0x3d0),('op',0xdc80,80,16,0x3b0),('op',0xdf20,80,16,0x3c0),('op',0xe1c0,80,16,0x3d0),('fm',0x88a0,64,24,0x420),('fm',0x8bc0,64,24,0x430),('fm',0x8ee0,64,24,0x430),('fm',0x6860,256,32,0x410),('fm',0x5840,256,32,0x410)]
    ims=[show(get(t,o,w,h),pal(open(f'shots/{n}.cram','rb').read(),c),3) for n,o,w,h,c in L]
    m=Image.new('RGB',(768,sum(i.height for i in ims)));y=0
    for i in ims: m.paste(i,(0,y));y+=i.height
    m.save('shots/t3.png')
