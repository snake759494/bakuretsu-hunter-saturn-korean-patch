import struct,glob,os,json
BASE=0x0602C000
def u32(m,i): return struct.unpack('>I',m[i:i+4])[0]
def u16(m,i): return struct.unpack('>H',m[i:i+2])[0]
_c={}
def msg_end(m,off):
    k=(id(m),off)
    if k in _c: return _c[k]
    r=_msg_end(m,off); _c[k]=r; return r
def _msg_end(m,off):
    i=off
    while i<len(m)-1:
        x=u16(m,i)
        if x==0xffff: return i+2
        if x>0x400 and x not in (0xfffe,0xfffc,0xfffd,0xfffb,0xfffa): return None
        i+=2
    return None
def analyze(path):
    m=open(path,'rb').read();n=len(m)
    # glyph entry
    g=None
    for i in range(0,n-12,4):
        if u32(m,i)==0x00070000 and 0x00200000<=u32(m,i+4)<0x00300000 and u32(m,i+8)%0x80==0 and 0<u32(m,i+8)<0x40000:
            g=(i,u32(m,i+4)-0x200000,u32(m,i+8)//0x80);break
    # pointer runs
    best=None
    i=0
    while i<n-4:
        j=i;tg=[]
        while j<n-4:
            p=u32(m,j)-BASE
            if 0<=p<n and p%2==0 and (not tg or p>tg[-1]) and msg_end(m,p) is not None: tg.append(p);j+=4
            else: break
        if len(tg)>=5 and (best is None or len(tg)>len(best[1])): best=(i,tg)
        i=j+4 if j>i else i+4
    return m,g,best
if __name__=='__main__':
    res={}
    for f in sorted(glob.glob('disc/PRG/*.BIN')):
        m,g,best=analyze(f)
        if best:
            t0=best[1][0];tl=msg_end(m,best[1][-1])
            print(os.path.basename(f),'glyph',(hex(g[0]),hex(g[1]),hex(g[2])) if g else None,'ptrtab',hex(best[0]),len(best[1]),'text',hex(t0),hex(tl))
        else: print(os.path.basename(f),'glyph',g,'NO TABLE')
