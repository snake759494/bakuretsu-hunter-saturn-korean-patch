import sys,numpy as np
from PIL import Image
def tiles(path,off,bpp,cols=32,out='shots/x.png',n=None,tw=8):
    d=np.frombuffer(open(path,'rb').read(),np.uint8)[off:]
    if bpp==4:
        p=np.zeros(len(d)*2,np.uint8);p[0::2]=d>>4;p[1::2]=d&15;p=(p*17).astype(np.uint8)
    else: p=d
    ts=tw*tw;N=n or len(p)//ts;rows=(N+cols-1)//cols
    img=np.zeros((rows*tw,cols*tw),np.uint8)
    for i in range(N):
        t=p[i*ts:(i+1)*ts].reshape(tw,tw);img[(i//cols)*tw:(i//cols+1)*tw,(i%cols)*tw:(i%cols+1)*tw]=t
    Image.fromarray(img).resize((cols*tw*2,rows*tw*2),0).save(out)
if __name__=='__main__':
    tiles(sys.argv[1],int(sys.argv[2],0),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5])
