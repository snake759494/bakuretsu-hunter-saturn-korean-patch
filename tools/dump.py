import json,struct,hashlib,os
from PIL import Image
s=json.load(open('scan2.json'))
def u16(m,i): return struct.unpack('>H',m[i:i+2])[0]
def u32(m,i): return struct.unpack('>I',m[i:i+4])[0]
cat={}   # hash -> gid
cimgs=[]
scenes={}
for nm,e in s.items():
    m=open('disc/PRG/MEN'+nm+'.BIN','rb').read(); d=open(e['dat'],'rb').read()
    # glyph count from MEN entry
    a=0x200000+e['glyph'];i=m.find(struct.pack('>I',a));N=u32(m,i+4)//0x80
    gmap=[]
    for g in range(N):
        blk=d[e['glyph']+g*0x80:e['glyph']+g*0x80+0x80]
        h=hashlib.md5(blk).hexdigest()
        if h not in cat: cat[h]=len(cimgs);cimgs.append(blk)
        gmap.append(cat[h])
    # messages sequential in region
    msgs=[];p=e['r0']
    while p<e['r1']:
        ws=[];st=p
        while True:
            x=u16(m,p);p+=2;ws.append(x)
            if x==0xffff: break
        msgs.append(dict(off=st,w=ws))
    tg=set(e['targets'])
    for mm in msgs: mm['ref']=mm['off'] in tg
    scenes[nm]=dict(N=N,gmap=gmap,msgs=msgs,gentry=i)
    print(nm,N,len(msgs),sum(1 for mm in msgs if not mm['ref']))
json.dump(scenes,open('scenes.json','w'))
open('glyphs.bin','wb').write(b''.join(cimgs))
print('unique glyphs',len(cimgs))
