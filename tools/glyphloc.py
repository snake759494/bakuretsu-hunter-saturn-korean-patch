import json,os
def fontish(blk): return all((x>>4) in (0,15) and (x&15) in (0,15) for x in blk)
s=json.load(open('scan2.json'))
for nm,e in s.items():
    dn='disc/DAT/S'+nm+'.BIN'
    if not os.path.exists(dn): dn='disc/DAT/S'+nm[:-1]+'.BIN'
    d=open(dn,'rb').read(); N=e['maxg']+1;res=[]
    for st in range(4,len(d)-0x80*N,0x100):
        if d[st:st+0x80]!=bytes(0x80): continue
        if all(fontish(d[st+g*0x80:st+g*0x80+0x80]) and any(d[st+g*0x80:st+g*0x80+0x80]) for g in range(1,N)): res.append(st)
    # also check how many glyphs continue past N
    k=N
    if res:
        while fontish(d[res[0]+k*0x80:res[0]+k*0x80+0x80]) and any(d[res[0]+k*0x80:res[0]+k*0x80+0x80]): k+=1
    e['dat']=dn;e['glyph']=res[0] if len(res)==1 else res
    print(nm,os.path.basename(dn),hex(len(d)),[hex(x) for x in res],'N',hex(N),'cont',hex(k))
json.dump(s,open('scan2.json','w'))
