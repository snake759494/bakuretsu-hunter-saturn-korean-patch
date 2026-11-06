import struct,glob,os,json,sys
sys.path.insert(0,'tools')
from men import analyze,msg_end,u16,u32,BASE
def fontish(blk): return all((x>>4) in (0,15) and (x&15) in (0,15) for x in blk)
def glyph_region(d,N):
    res=[]
    for st in range(0,len(d)-0x80*N,4):
        if d[st:st+0x80]!=bytes(0x80): continue
        if all(fontish(d[st+g*0x80:st+g*0x80+0x80]) and any(d[st+g*0x80:st+g*0x80+0x80]) for g in range(1,N)): res.append(st)
    return res
def ok_msg(m,p):
    e=msg_end(m,p)
    if e is None: return None
    ws=[u16(m,i) for i in range(p,e-2,2)]
    if any(0x400<=w<0xfff0 for w in ws): return None
    return e
out={}
for f in sorted(glob.glob('disc/PRG/MEN*.BIN')):
    nm=os.path.basename(f)[3:-4]
    m,g,best=analyze(f)
    if not best: print(nm,'skip');continue
    tg=[p for p in best[1] if ok_msg(m,p)]
    # region: start at median-ish cluster: take targets, sort, cluster contiguous
    tg=sorted(set(tg))
    # find contiguous chain from each target
    chains=[];cur=None
    for p in tg:
        if cur and p==cur[1]: cur[1]=ok_msg(m,p)
        elif cur and cur[0]<p<cur[1]: continue
        else:
            cur=[p,ok_msg(m,p)];chains.append(cur)
    # extend chains forward sequentially
    for c in chains:
        while True:
            e=ok_msg(m,c[1])
            if e and e-c[1]>2: c[1]=e
            else: break
    chains.sort(key=lambda c:c[1]-c[0],reverse=True)
    r0,r1=chains[0]
    # all pointers into region
    ptrs=[i for i in range(0,len(m)-3,2) if r0<=u32(m,i)-BASE<r1]
    mx=max(u16(m,i) for i in range(r0,r1,2) if u16(m,i)<0xff00)
    dn='disc/DAT/S'+nm.rstrip('M')+'.BIN'
    if not os.path.exists(dn): dn='disc/DAT/S'+nm[:-1]+'.BIN'
    d=open(dn,'rb').read()
    r=glyph_region(d,mx+1)
    print(nm,'region',hex(r0),hex(r1),'chains',len(chains),[(hex(a),hex(b)) for a,b in chains[1:4]],'ptrs',len(ptrs),'maxg',hex(mx),os.path.basename(dn),[hex(x) for x in r])
    out[nm]=dict(r0=r0,r1=r1,ptrs=ptrs,maxg=mx,dat=dn,glyph=r)
json.dump(out,open('scan.json','w'),indent=0)
