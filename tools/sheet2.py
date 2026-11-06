import sys,numpy as np
from PIL import Image
def best_w(a,cands):
    r=[]
    for w in cands:
        n=len(a)//w; 
        if n<4: continue
        m=a[:n*w].reshape(n,w).astype(int); r.append((np.mean(np.abs(m[1:]-m[:-1])),w))
    return sorted(r)[:5]
def render(path,off,bpp,w,h=None,out='x.png',scale=1):
    d=np.frombuffer(open(path,'rb').read(),np.uint8)[off:]
    if bpp==4:
        p=np.zeros(len(d)*2,np.uint8);p[0::2]=d>>4;p[1::2]=d&15;p=p*17
    else: p=d
    h=h or len(p)//w; img=p[:w*h].reshape(h,w)
    Image.fromarray(img).resize((w*scale,h*scale),0).save(out)
if __name__=='__main__':
    f,off,bpp,w=sys.argv[1],int(sys.argv[2],0),int(sys.argv[3]),int(sys.argv[4])
    h=int(sys.argv[5]) if len(sys.argv)>5 else None
    render(f,off,bpp,w,h,sys.argv[6] if len(sys.argv)>6 else 'shots/x.png')
