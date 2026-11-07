"""Slot-battle tutorial (Doter) messages: Korean text + 16x16 font in SLOT_DT."""
import struct,os,numpy as np
from PIL import Image,ImageDraw,ImageFont
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FB=0x46f3c; MSG0=0x466a0; MSGEND=0x46e92; NG=186
PTRS=list(range(0x46ea4,0x46f3c,4))      # 38 message pointers (LWRAM 0x200000-based)
FONT=os.path.join(os.path.dirname(W),'NanumSquareNeo-cBd.ttf')
def cell(ch):
    if ch==' ': return np.zeros((16,16),np.uint8)
    sym=ch in '!.?~”♥「」『』・0135ABCHP'
    f=ImageFont.truetype(FONT,15 if not sym else 14)
    im=Image.new('L',(16,16));d=ImageDraw.Draw(im)
    if ch=='♥':
        d.polygon([(8,14),(1,7),(1,4),(3,2),(6,2),(8,4),(10,2),(13,2),(15,4),(15,7)],fill=255)
    elif ch=='・': d.rectangle([7,7,8,8],fill=255)
    elif ch=='「': d.line([(9,2),(9,12)],fill=255);d.line([(9,2),(14,2)],fill=255)
    elif ch=='」': d.line([(6,3),(6,13)],fill=255);d.line([(1,13),(6,13)],fill=255)
    elif ch=='『': d.line([(8,1),(8,13),(10,13),(10,3),(14,3),(14,1),(8,1)],fill=255)
    elif ch=='』': d.line([(7,14),(7,2),(5,2),(5,12),(1,12),(1,14),(7,14)],fill=255)
    elif ch=='”': d.line([(5,2),(4,5)],fill=255);d.line([(6,2),(5,5)],fill=255);d.line([(10,2),(9,5)],fill=255);d.line([(11,2),(10,5)],fill=255)
    else:
        bb=d.textbbox((0,0),ch,font=f);w,h=bb[2]-bb[0],bb[3]-bb[1]
        x=(16-w)//2-bb[0]; y=(16-h)//2-bb[1]
        if ch in '.': x,y=2-bb[0],13-bb[3]
        if ch in '「『': x=8-bb[0]
        if ch in '」』': x=8-bb[2]
        d.text((x,y),ch,font=f,fill=255)
    return (np.array(im)>100).astype(np.uint8)*15
def enc(P):
    out=b''
    for cy,cx in ((0,0),(0,1),(1,0),(1,1)):
        c=P[cy*8:cy*8+8,cx*8:cx*8+8].ravel();out+=bytes(((c[0::2]<<4)|c[1::2]).astype(np.uint8))
    return out
def apply(t):
    L=[l.rstrip('\n') for l in open(os.path.join(W,'slotmsg_ko.txt'),encoding='utf-8') if l.strip()]
    assert len(L)==len(PTRS)
    chars=[' ']+sorted(set(''.join(L))-set('/ '))
    assert len(chars)<=NG,len(chars)
    idx={c:i for i,c in enumerate(chars)}
    for i in range(NG):
        P=cell(chars[i]) if i<len(chars) else np.zeros((16,16),np.uint8)
        t[FB+i*128:FB+(i+1)*128]=enc(P)
    o=MSG0
    for pa,l in zip(PTRS,L):
        t[pa:pa+4]=struct.pack('>I',0x200000+o)
        for ch in l:
            v=0xfffe if ch=='/' else idx[ch]
            t[o:o+2]=struct.pack('>H',v);o+=2
        t[o:o+2]=b'\xff\xff';o+=2
    assert o<=MSGEND,hex(o)
    t[o:MSGEND]=bytes(MSGEND-o)
    return chars
if __name__=='__main__':
    import sys;sys.path.insert(0,os.path.dirname(__file__))
    t=bytearray(open(os.path.join(W,'disc/DAT/SLOT_DT.BIN'),'rb').read());apply(t)
    import smsg;smsg.d=bytes(t)
    rows=[]
    for pa,o in smsg.ptrs()[3:15]:
        im=smsg.render(smsg.msg(o));rows.append(np.pad(im,((0,6),(0,176-im.shape[1]))))
    Image.fromarray(np.vstack(rows).astype(np.uint8)*255).resize((352,sum(r.shape[0] for r in rows)*2),0).save(os.path.join(W,'shots/kslot_prev.png'))
