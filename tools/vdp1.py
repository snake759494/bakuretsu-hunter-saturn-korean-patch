import struct,sys
from PIL import Image
def cmds(v):
    i=0;out=[];n=0
    while i<0x80000 and n<2000:
        c=struct.unpack('>16H',v[i:i+32]);ctrl=c[0]
        if ctrl&0x8000: break
        cmd=ctrl&0xf; jp=(ctrl>>12)&7
        if not (ctrl&0x4000) and cmd in (0,1,2):
            x=struct.unpack('>h',v[i+12:i+14])[0];y=struct.unpack('>h',v[i+14:i+16])[0]
            out.append(dict(at=i,cmd=cmd,pmod=c[2],col=c[3],src=c[4]*8,w=(c[5]>>8)*8,h=c[5]&0xff,x=x,y=y))
        if jp==1: i=c[1]*8
        elif jp==2: i=c[1]*8  # call (approx)
        else: i+=32
        n+=1
    return out
def sprite(v,cr,s):
    mode=(s['pmod']>>3)&7; w,h=s['w'],s['h']; im=Image.new('RGBA',(w,h))
    def col(i):
        c=struct.unpack('>H',cr[(i%2048)*2:(i%2048)*2+2])[0]; return ((c&31)<<3,((c>>5)&31)<<3,((c>>10)&31)<<3,255)
    for y in range(h):
        for x in range(w):
            if mode in (0,1):
                b=v[(s['src']+(y*w+x)//2)&0x7ffff]; p=(b>>4) if x%2==0 else b&15
                if p==0: continue
                im.putpixel((x,y),col(s['col']+p) if mode==0 else (p*17,p*17,p*17,255))
            elif mode==5:
                p=struct.unpack('>H',v[(s['src']+(y*w+x)*2)&0x7ffff:][:2])[0]
                if p&0x8000: im.putpixel((x,y),((p&31)<<3,((p>>5)&31)<<3,((p>>10)&31)<<3,255))
            else:
                p=v[(s['src']+y*w+x)&0x7ffff]
                if p: im.putpixel((x,y),col(s['col']+p))
    return im
if __name__=='__main__':
    n=sys.argv[1]; v=open(f'shots/{n}.v1','rb').read(); cr=open(f'shots/{n}.cram','rb').read()
    for s in cmds(v): print(hex(s['at']),s['cmd'],'mode',(s['pmod']>>3)&7,hex(s['col']),'src',hex(s['src']),s['w'],s['h'],'xy',s['x'],s['y'])
