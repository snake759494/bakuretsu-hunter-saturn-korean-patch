import struct,glob,os,json,sys,collections
BASE=0x0602C000
def u32(m,i): return struct.unpack('>I',m[i:i+4])[0]
def u16(m,i): return struct.unpack('>H',m[i:i+2])[0]
def msg(m,p):
    i=p;ws=[]
    while i<len(m)-1 and len(ws)<400:
        x=u16(m,i);ws.append(x);i+=2
        if x==0xffff: return ws,i
        if 0x400<=x<0xfff0: return None
    return None
res={};ctl=collections.Counter()
old=json.load(open('scan.json'))
for f in sorted(glob.glob('disc/PRG/MEN*.BIN')):
    nm=os.path.basename(f)[3:-4]; m=open(f,'rb').read()
    tg={}
    for i in range(0,len(m)-3,2):
        p=u32(m,i)-BASE
        if 0<=p<len(m) and p%2==0:
            r=msg(m,p)
            if r and sum(1 for w in r[0] if 0<w<0x400)>=2: tg.setdefault(p,[]).append(i)
    ps=sorted(tg); cl=[];cur=None
    for p in ps:
        e=msg(m,p)[1]
        if cur and p<=cur[1]+0x40: cur[1]=max(cur[1],e);cur[2].append(p)
        else: cur=[p,e,[p]];cl.append(cur)
    cl=[c for c in cl if max(u16(m,i) for i in range(c[0],c[1],2) if u16(m,i)<0xff00)<0x300]
    cl.sort(key=lambda c:len(c[2]),reverse=True)
    if not cl: print(nm,'none');continue
    r0,r1,tps=cl[0]
    ptrs=sorted(i for p in tps for i in tg[p])
    for i in range(r0,r1,2):
        x=u16(m,i)
        if x>=0xff00: ctl[hex(x)]+=1
    mx=max(u16(m,i) for i in range(r0,r1,2) if u16(m,i)<0xff00)
    print(nm,hex(r0),hex(r1),'msgs',len(tps),'ptrs',len(ptrs),'other clusters',[(hex(c[0]),len(c[2])) for c in cl[1:4]],'maxg',hex(mx))
    res[nm]=dict(r0=r0,r1=r1,targets=tps,ptrs=ptrs,maxg=mx,dat=old.get(nm,{}).get('dat'),glyph=old.get(nm,{}).get('glyph'))
print(ctl)
json.dump(res,open('scan2.json','w'))
