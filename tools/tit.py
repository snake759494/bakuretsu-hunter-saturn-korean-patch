import struct,sys,numpy as np
from PIL import Image
T='disc/DAT/TIT_DT.BIN'
def pal(cr,col): return [struct.unpack('>H',cr[(col+i)*2:(col+i)*2+2])[0] for i in range(16)]
def rgb(c): return ((c&31)<<3,((c>>5)&31)<<3,((c>>10)&31)<<3)
def get(t,off,w,h):
    a=np.frombuffer(t[off:off+w*h//2],np.uint8);P=np.zeros((h,w),np.uint8);P[:,0::2]=(a>>4).reshape(h,w//2);P[:,1::2]=(a&15).reshape(h,w//2);return P
def put(t,off,P):
    h,w=P.shape;b=(P[:,0::2]<<4)|P[:,1::2];t[off:off+w*h//2]=b.astype(np.uint8).tobytes()
def show(P,pl,s=4):
    im=Image.new('RGB',(P.shape[1],P.shape[0]))
    im.putdata([rgb(pl[p]) if p else (255,0,255) for p in P.flatten()]);return im.resize((P.shape[1]*s,P.shape[0]*s),0)
