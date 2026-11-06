import numpy as np
from PIL import Image,ImageFont,ImageDraw
def glyph64(ch,fill):
    f=ImageFont.truetype('../NanumSquareNeo-eHv.ttf',58);im=Image.new('L',(64,64));d=ImageDraw.Draw(im)
    bb=d.textbbox((0,0),ch,font=f);w,h=bb[2]-bb[0],bb[3]-bb[1]
    d.text(((64-w)//2-bb[0],(64-h)//2-bb[1]),ch,font=f,fill=255);m=np.array(im)>110
    o=np.pad(m,1);O=o.copy()
    for dy in(-1,0,1):
        for dx in(-1,0,1): O|=np.roll(np.roll(o,dy,0),dx,1)
    O=O[1:-1,1:-1];P=np.zeros((64,64),np.uint8);P[O]=15;P[m]=fill;return P
def apply(t):
    for off,ch,fill in [(0x212e0,'승',13),(0x21b00,'리',13),(0x22320,'패',14),(0x22b40,'배',14)]:
        P=glyph64(ch,fill);t[off:off+0x800]=((P[:,0::2]<<4)|P[:,1::2]).astype(np.uint8).tobytes()
if __name__=='__main__':
    t=bytearray(open('disc/DAT/SLOT_DT.BIN','rb').read());apply(t)
    ims=[]
    for o in (0x212e0,0x21b00,0x22320,0x22b40):
        a=np.frombuffer(t[o:o+0x800],np.uint8);p=np.zeros(4096,np.uint8);p[0::2]=a>>4;p[1::2]=a&15;ims.append(p.reshape(64,64)*17)
    Image.fromarray(np.hstack(ims)).resize((512,128),0).save('shots/slotk.png')
