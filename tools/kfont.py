import numpy as np
from PIL import Image,ImageDraw,ImageFont
import os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT=os.path.join(ROOT,'NanumSquareNeo-bRg.ttf')
_f=ImageFont.truetype(FONT,15)
G=open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'glyphs.bin'),'rb').read()
_cache={}
# punctuation that should sit low/left like the original
def render(ch):
    if ch in _cache: return _cache[ch]
    im=Image.new('L',(16,16));d=ImageDraw.Draw(im)
    if ch=='　' or ch==' ':
        P=np.zeros((16,16),np.uint8)
    else:
        bb=d.textbbox((0,0),ch,font=_f);w=bb[2]-bb[0];h=bb[3]-bb[1]
        x=(16-w)//2-bb[0]
        if ch in '、。，．,.': x=1-bb[0]; y=13-bb[3]
        elif ch in '「『': x=3-bb[0]; y=1-bb[1]
        elif ch in '」』': x=12-bb[2]; y=15-bb[3]
        else:
            # vertical: align to font baseline box (asc 15px font) centred
            y=(16-15)//2  # draw at fixed baseline so all syllables align
            d.text((x,y),ch,font=_f,fill=255)
            P=(np.array(im)>100).astype(np.uint8)
            _cache[ch]=P;return P
        d.text((x,y),ch,font=_f,fill=255)
        P=(np.array(im)>100).astype(np.uint8)
    _cache[ch]=P;return P
def orig(gid):
    blk=G[gid*0x80:gid*0x80+0x80]; return blk
def encode4(P):
    out=bytearray(0x80)
    for c in range(4):
        for y in range(8):
            for x in range(0,8,2):
                a=P[(c//2)*8+y,(c%2)*8+x]; b=P[(c//2)*8+y,(c%2)*8+x+1]
                out[c*32+y*4+x//2]=(0xf0 if a else 0)|(0x0f if b else 0)
    return bytes(out)
def glyph_bytes(tok):
    if tok.startswith('⟨'): return orig(int(tok[1:-1]))
    return encode4(render(tok))

def pixels(tok):
    if tok.startswith('⟨'):
        blk=orig(int(tok[1:-1]));P=np.zeros((16,16),np.uint8)
        for y in range(16):
            for x in range(16):
                c=(y//8)*2+(x//8); b=blk[c*32+(y%8)*4+(x%8)//2]; P[y,x]=1 if ((b>>4) if x%2==0 else b&15) else 0
        return P
    return render(tok)
