import json,sys
from PIL import Image,ImageDraw,ImageFont
import numpy as np
G=open('glyphs.bin','rb').read();n=len(G)//128
v=json.load(open('votes.json'))
lab={int(k):x[0][0] for k,x in v.items()}
try: fix=json.load(open('glyph_fix.json'))
except: fix={}
for k,c in fix.items(): lab[int(k)]=c
def gimg(gid):
    blk=G[gid*0x80:gid*0x80+0x80];P=np.zeros((16,16),np.uint8)
    for y in range(16):
        for x in range(16):
            c=(y//8)*2+(x//8); b=blk[c*32+(y%8)*4+(x%8)//2]; P[y,x]=255 if ((b>>4) if x%2==0 else b&15) else 0
    return P
f=ImageFont.truetype('C:/Windows/Fonts/msgothic.ttc',26);fs=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',11)
per=120;cols=12
for s0 in range(0,n,per):
    im=Image.new('RGB',(cols*80,10*44),(255,255,255));d=ImageDraw.Draw(im)
    for k in range(s0,min(n,s0+per)):
        r,c=divmod(k-s0,cols);x=c*80;y=r*44
        g=Image.fromarray(255-gimg(k)).resize((32,32),Image.NEAREST).convert('RGB'); im.paste(g,(x+2,y+6))
        d.text((x+38,y+6),lab.get(k,'?'),font=f,fill=(200,0,0) if k not in lab else (0,0,180))
        d.text((x+2,y+32),str(k),font=fs,fill=(120,120,120))
    im.save(f'shots/sheet{s0//per}.png')
print(n)
