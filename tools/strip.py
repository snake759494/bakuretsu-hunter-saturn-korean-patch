import sys,numpy as np
from PIL import Image
def strip(path,bpp,w,colh=1000,cols=8,start=0,out='shots/x.png'):
    d=np.frombuffer(open(path,'rb').read(),np.uint8)
    if bpp==4: p=np.zeros(len(d)*2,np.uint8);p[0::2]=d>>4;p[1::2]=d&15;p=(p*17).astype(np.uint8)
    else: p=d
    rows=len(p)//w;img=p[:rows*w].reshape(rows,w)
    r0=start*colh*cols;m=np.zeros((colh,(w+4)*cols),np.uint8)
    for k in range(cols):
        a=img[r0+k*colh:r0+(k+1)*colh]
        m[:a.shape[0],k*(w+4):k*(w+4)+w]=a
    Image.fromarray(m).save(out);return rows
if __name__=='__main__':
    print(strip(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),start=int(sys.argv[4]),out=sys.argv[5]))
