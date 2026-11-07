"""Slot battle UI sprites in SLOT_DT (uncompressed): バトル/カード buttons, 敵ソーサラー panel, Doter clouds."""
import os,numpy as np
from PIL import Image,ImageDraw,ImageFont
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def mask(text,w,h,size,font='NanumSquareNeo-eHv.ttf',dx=0,dy=0,sp=0):
    f=ImageFont.truetype(os.path.join(R,font),size)
    im=Image.new('L',(w*4,h*4));d=ImageDraw.Draw(im)
    # draw char by char with spacing
    xs=[];x=0
    for ch in text:
        bb=d.textbbox((0,0),ch,font=f);xs.append((x,ch,bb));x+=(bb[2]-bb[0] if ch!=' ' else size//3)+sp
    tw=x-sp;bb=d.textbbox((0,0),text,font=f);th=bb[3]-bb[1]
    ox=(w*4-tw)//2;oy=(h*4-th)//2-bb[1]
    for x0,ch,b in xs: d.text((ox+x0-b[0]+0,oy),ch,font=f,fill=255)
    m=np.array(im)>110
    return m[h*2-h//2-dy:h*2+h-h//2-dy, w*2-w//2-dx:w*2+w-w//2-dx]
def dil(m):
    o=m.copy()
    for dy in(-1,0,1):
        for dx in(-1,0,1): o|=np.roll(np.roll(m,dy,0),dx,1)
    return o
def g8(t,p,w,h): return np.frombuffer(bytes(t[p:p+w*h]),np.uint8).reshape(h,w).copy()
def p8(t,p,a): t[p:p+a.size]=a.astype(np.uint8).tobytes()
def g4(t,p,w,h):
    a=np.frombuffer(bytes(t[p:p+w*h//2]),np.uint8);q=np.zeros(w*h,np.uint8);q[0::2]=a>>4;q[1::2]=a&15;return q.reshape(h,w)
def p4(t,p,a):
    q=a.ravel();t[p:p+q.size//2]=((q[0::2]<<4)|q[1::2]).astype(np.uint8).tobytes()
def button(t,p,text):
    a=g8(t,p,48,16)
    TXT={0x21,0x22,0x12,0x24,0x01}
    for y in range(2,14):
        row=a[y,2:45];bg=[v for v in row if v not in TXT]
        vals,cnt=np.unique(bg,return_counts=True);fill=vals[cnt.argmax()]
        for x in range(2,45):
            if a[y,x] in TXT: a[y,x]=fill
    m=mask(text,48,16,11,sp=1)
    o=dil(m)&~m; sh=np.roll(m,1,0)&~m&~o
    inner=np.zeros((16,48),bool);inner[2:14,2:45]=True
    a[sh&inner]=0x24;a[o&inner]=0x12;a[m&inner]=0x21
    p8(t,p,a)
def panel(t,p):
    a=g8(t,p,120,72)
    for y in range(3,21):
        for x in range(3,56):
            if not (0x1a<=a[y,x]<=0x1f): a[y,x]=a[y,(x%3)] if 0x1a<=a[y,x%3]<=0x1f else 0x1c
    m=mask('적 소서러',53,18,12,sp=0)
    o=dil(m)&~m
    sub=a[3:21,3:56];sub[o]=0x15;sub[m]=0x31
    p8(t,p,a)
def cloud(t,p,text):
    a=g4(t,p,48,32)
    inside=np.zeros((32,48),bool);inside[10:23,6:42]=True
    a[inside&(a<15)&(a>1)]=15
    m=mask(text,36,13,11,font='NanumSquareNeo-dEb.ttf')
    sub=a[10:23,6:42];sub[m]=5
    p4(t,p,a)
def cards(t,p,fill,outl,shad,KJ,chars):
    a=g8(t,p,120,24)
    for k,ch in enumerate(chars):
        x0=30*k+6;x1=30*k+23
        for y in range(4,21):
            row=a[y,x0:x1];bg=[v for v in row if v not in KJ]
            f=np.unique(bg,return_counts=True);f=f[0][f[1].argmax()] if len(bg) else a[y,x0-1]
            for x in range(x0,x1):
                if a[y,x] in KJ: a[y,x]=f
        m=mask(ch,16,16,14,font='NanumSquareNeo-cBd.ttf')
        o=dil(m)&~m; sh=np.roll(np.roll(m,1,0),1,1)&~m&~o
        sub=a[4:20,x0:x0+16];sub[sh]=shad;sub[o]=outl;sub[m]=fill
    p8(t,p,a)
def apply(t):
    cards(t,0x25f20,0x31,0x11,0x14,{0x31,0x30,0x11,0x14},'필전회속')
    cards(t,0x26c60,0x21,0x22,0x24,{0x21,0x22,0x24},'필전회지')
    button(t,0x2ae60,'배틀'); button(t,0x2b360,'카드')
    panel(t,0x28aa0); player(t)
    hp_labels(t)
    cloud(t,0x46080,'하아'); cloud(t,0x463a0,'하암~')
if __name__=='__main__':
    W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    t=bytearray(open(os.path.join(W,'disc/DAT/SLOT_DT.BIN'),'rb').read());apply(t)
    def show(a): v=np.unique(a);m={x:i*255//max(1,len(v)-1) for i,x in enumerate(v)};return np.vectorize(m.get)(a).astype(np.uint8)
    Image.fromarray(np.vstack([show(g8(t,0x25f20,120,24)),show(g8(t,0x26c60,120,24))])).resize((720,288),0).save(os.path.join(W,'shots/cards.png'))
    ims=[show(g8(t,0x2ae60,48,16)),show(g8(t,0x2b360,48,16)),show(g4(t,0x46080,48,32)),show(g4(t,0x463a0,48,32))]
    Image.fromarray(show(g8(t,0x28aa0,120,72))).resize((480,288),0).save(os.path.join(W,'shots/ui_panel.png'))
    c=np.zeros((32,48*4+12),np.uint8);x=0
    for a in ims: c[:a.shape[0],x:x+48]=a;x+=52
    Image.fromarray(c).resize((c.shape[1]*5,160),0).save(os.path.join(W,'shots/ui_btn.png'))

# ---- HP panels (40x40 8bpp, left/right halves): 力技 / 防必 labels -> 힘기 / 방필
HP_PANELS=[(0x359a0,'힘기'),(0x361e0,'방필'),(0x36a20,'힘기'),(0x37260,'방필'),
           (0x37aa0,'힘기'),(0x382e0,'방필'),(0x38b20,'힘기'),(0x39360,'방필')]
TXT8={0x10,0x30,0x31,0x23,0x13,0x15}
def hp_labels(t):
    import sys;sys.path.insert(0,os.path.dirname(__file__))
    from kname import F9
    def glyph(ch):
        dw,(w,h,ox,oy),rows,bits=F9[ord(ch)]
        m=np.zeros((12,12),bool)
        for r,v in enumerate(rows):
            for b in range(w):
                if v>>(bits-1-b)&1: m[r+1+(9-h)//2+0, 1+b+ox]=True
        return m
    for p,lab in HP_PANELS:
        a=g8(t,p,40,40)
        for (y0,y1),ch in zip(((17,27),(29,39)),lab):
            for y in range(y0,y1):
                bg=[v for v in a[y,13:40] if v not in TXT8]
                f=np.unique(bg,return_counts=True);f=f[0][f[1].argmax()]
                for x in range(0,13):
                    if a[y,x] in TXT8: a[y,x]=f
            m=glyph(ch)[0:10,0:12]
            o=dil(m)&~m; sh=np.roll(np.roll(m,1,0),1,1)&~m&~o
            sub=a[y0:y1,0:12];sub[o]=0x30;sub[sh]=0x10;sub[m]=0x31
        p8(t,p,a)

def player(t,p=0x28aa0):
    a=g8(t,p,120,72)
    TX={0x15,0x30,0x31,0x2d,0x19,0x23}
    for y in range(4,22):
        bg=[v for v in list(a[y,58:66])+list(a[y,116:120]) if v not in TX]
        f=np.unique(bg,return_counts=True);f=f[0][f[1].argmax()] if len(bg) else 0x1c
        for x in range(64,117):
            if a[y,x] in TX: a[y,x]=f
    m=mask('플레이어',53,18,12,sp=0)
    o=dil(m)&~m
    sub=a[3:21,63:116];sub[o]=0x15;sub[m]=0x31
    p8(t,p,a)
