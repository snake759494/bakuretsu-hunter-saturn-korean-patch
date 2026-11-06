import json,struct,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from cdimg import Image
import kfont
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT=os.path.dirname(W)
SRC=os.path.join(ROOT,'Bakuretsu Hunter (Japan) (Disc 1) (Track 1).bin')
BASE=0x0602C000
def u16(m,i): return struct.unpack('>H',m[i:i+2])[0]
def u32(m,i): return struct.unpack('>I',m[i:i+4])[0]
TOK=re.compile(r'⟨\d+⟩|▼\n?|\n|.',re.S)
MAXW=15;MAXL=3
errors=[]
def tokens(s):
    return TOK.findall(s)
def encode_msg(s,idx,where):
    out=[];line=0;nl=1
    for t in tokens(s):
        if t=='\n': out.append(0xfffe);line=0;nl+=1
        elif t.startswith('▼'): out.append(0xfffc);line=0;nl=1
        else:
            if t in (' ','　'): out.append(0)
            else: out.append(idx[t])
            line+=1
            if line>MAXW: errors.append(f'{where}: line too long: {s!r}')
        if nl>MAXL: errors.append(f'{where}: too many lines: {s!r}'); nl=1
    out.append(0xffff)
    return out
def glyphset(msgs):
    seen=[]
    for s in msgs:
        for t in tokens(s):
            if t in ('\n',' ','　') or t.startswith('▼'): continue
            if t not in seen: seen.append(t)
    return seen
def build(out_bin,only=None,report=None):
    scan=json.load(open(os.path.join(W,'scan2.json')))
    sc=json.load(open(os.path.join(W,'scenes.json')))
    jp=os.path.join(W,'ja.json'); ja=json.load(open(jp,encoding='utf-8')) if os.path.exists(jp) else None
    img=Image(SRC)
    ents={e['name']:e for e in img.dir_entries()}
    files={}  # path -> bytearray
    def get(p):
        if p not in files:
            e=ents[p]; files[p]=bytearray(img.read(e['lba'],(e['size']+2047)//2048)[:e['size']])
        return files[p]
    rep={}
    # group scenes by DAT
    bydat={}
    for nm,e in scan.items():
        if only and nm.rstrip('M') not in only: continue
        bydat.setdefault(os.path.basename(e['dat']),[]).append(nm)
    for datn,nms in bydat.items():
        base=[n for n in nms if not n.endswith('M')][0] if any(not n.endswith('M') for n in nms) else nms[0]
        kp=os.path.join(W,'ko',base+'.json')
        if not os.path.exists(kp): continue
        ko=json.load(open(kp,encoding='utf-8'))
        if ja and len(ko)!=len(ja[base]): errors.append(f'{base}: message count {len(ko)}!={len(ja[base])}');continue
        gs=glyphset(ko)
        idx={t:i+1 for i,t in enumerate(gs)}
        N=len(gs)+1
        if N>384: errors.append(f'{base}: too many glyphs {N}')
        import expand
        dat=get('DAT/'+datn)
        import kname; _NM=json.load(open('names.json'))
        if base in _NM: dat[:]=kname.patch(bytes(dat),_NM[base]['groups'])
        e0=scan[base]; goff=e0['glyph']
        men0=get('PRG/MEN'+base+'.BIN'); gi=sc[base]['gentry']; oldsz=u32(men0,gi+4) if u32(men0,gi)==0x200000+goff else rep['_oldsz'][datn]
        rep.setdefault('_oldsz',{})[datn]=oldsz
        code=expand.assemble(0x200000+goff)
        g1=bytes(32)+b''.join(expand.pack1(kfont.pixels(t)) for t in gs)
        blob=code+g1
        if len(blob)>oldsz: errors.append(f'{base}: glyph blob too big {len(blob):x}>{oldsz:x}')
        dat[goff:goff+len(blob)]=blob
        dataddr=0x200000+goff+len(code); gsize=N*0x80
        tail=[goff+len(blob)]
        enc=[encode_msg(s,idx,f'{base}#{i}') for i,s in enumerate(ko)]
        for nm in nms:
            men=get('PRG/MEN'+nm+'.BIN'); e=scan[nm]; gi=sc[nm]['gentry']
            men[gi:gi+8]=struct.pack('>II',dataddr,gsize)
            assert u32(men,0x298C)==0x0602FBBC or u32(men,0x298C)==0x200000+goff
            men[0x298C:0x2990]=struct.pack('>I',0x200000+goff)
            msgs=sc[nm]['msgs']; assert len(msgs)==len(enc)
            r0,r1=e['r0'],e['r1']
            # layout
            newaddr={};p=r0;over=[]
            for m,w in zip(msgs,enc):
                b=b''.join(struct.pack('>H',x) for x in w)
                if p+len(b)<=r1: men[p:p+len(b)]=b; newaddr[m['off']]=BASE+p; p+=len(b)
                else: over.append((m,b))
            men[p:r1]=b'\xff\xff'*((r1-p)//2)
            for m,b in over:
                tail[0]+=(-tail[0])%4
                if tail[0]+len(b)>goff+oldsz: errors.append(f'{nm}: no room for overflow text'); break
                dat[tail[0]:tail[0]+len(b)]=b; newaddr[m['off']]=0x200000+tail[0]; tail[0]+=len(b)
            # pointers: use original MEN bytes
            orig=img.read(ents['PRG/MEN'+nm+'.BIN']['lba'],(ents['PRG/MEN'+nm+'.BIN']['size']+2047)//2048)
            for pi in e['ptrs']:
                old=u32(orig,pi)-BASE
                if old not in newaddr: errors.append(f'{nm}: pointer {pi:x} -> {old:x} not msg start'); continue
                men[pi:pi+4]=struct.pack('>I',newaddr[old])
            rep[nm]=dict(N=N,oldN=oldsz//0x80,cap=(oldsz-104)//32,overflow=len(over))
    # extra hooks (names, menus)
    try:
        import extras
        extras.apply(get,img,errors)
    except ImportError: pass
    # write files back
    end=img.nsec
    for p,data in files.items():
        e=ents[p]; ns=(len(data)+2047)//2048; old=(e['size']+2047)//2048
        if ns<=old: img.write_data(e['lba'],bytes(data)); lba=e['lba']
        else:
            lba=img.nsec; img.write_data(lba,bytes(data))
        img.set_entry(e,lba,len(data))
    img.set_volume_size(img.nsec)
    img.save(out_bin)
    if report: json.dump(dict(scenes=rep,errors=errors),open(report,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    return rep
if __name__=='__main__':
    out=sys.argv[1]; only=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2] else None
    r=build(out,only,os.path.join(W,'build_report.json'))
    for k,v in r.items():
        if not k.startswith('_'): print(k,v)
    print('errors',len(errors))
    for e in errors[:30]: print(' ',e)
