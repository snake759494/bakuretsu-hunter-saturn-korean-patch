"""Korean messages for TIT_DT (movie list/save warnings) and MGAME_DT (doppel game) — 16x16 glyph-index text."""
import struct,os,sys
sys.path.insert(0,os.path.dirname(__file__))
import numpy as np
from kslotmsg import cell,enc
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS={
 'TIT':dict(fb=0x4c500,ng=123,msg0=0x50280,msgend=0x507b4,ptrs=list(range(0x507c8,0x5083c,4)),txt='tit_ko.txt'),
 'MGAME':dict(fb=0xbbab0,ng=193,msg0=0xbaf98,msgend=0xbb942,ptrs=list(range(0xbb954,0xbbab0,4)),txt='mgame_ko.txt'),
}
def u16(t,o): return struct.unpack('>H',bytes(t[o:o+2]))[0]
def orig_lines(t,o):
    lines=[[]]
    while True:
        v=u16(t,o);o+=2
        if v==0xffff: return lines
        if v in (0xfffe,0xfffc): lines.append([])
        else: lines[-1].append(v)
def apply(t,key):
    s=SPECS[key]
    L=[l.rstrip('\n') for l in open(os.path.join(W,s['txt']),encoding='utf-8') if l.strip('\n')]
    assert len(L)==len(s['ptrs']),(len(L),len(s['ptrs']))
    chars=[' ']+sorted(set(''.join(L))-set('/| '))
    assert len(chars)<=s['ng'],len(chars)
    idx={c:i for i,c in enumerate(chars)}
    # pad widths from original (only where original lines were space padded)
    pads=[]
    for pa in s['ptrs']:
        o=struct.unpack('>I',bytes(t[pa:pa+4]))[0]-0x200000
        ol=orig_lines(t,o);pads.append(max(len(x) for x in ol) if any(x and x[-1]==0 for x in ol) else 0)
    for i in range(s['ng']):
        P=cell(chars[i]) if i<len(chars) else np.zeros((16,16),np.uint8)
        t[s['fb']+i*128:s['fb']+(i+1)*128]=enc(P)
    o=s['msg0']
    for pa,l,pw in zip(s['ptrs'],L,pads):
        t[pa:pa+4]=struct.pack('>I',0x200000+o)
        parts=[];cur=''
        for ch in l:
            if ch in '/|': parts.append((cur,ch));cur=''
            else: cur+=ch
        parts.append((cur,None))
        for seg,sep in parts:
            seg=seg.ljust(pw) if pw else seg
            for ch in seg: t[o:o+2]=struct.pack('>H',idx[ch]);o+=2
            if sep: t[o:o+2]=struct.pack('>H',0xfffe if sep=='/' else 0xfffc);o+=2
        t[o:o+2]=b'\xff\xff';o+=2
    assert o<=s['msgend'],(key,hex(o))
    t[o:s['msgend']]=bytes(s['msgend']-o)
    return chars
if __name__=='__main__':
    from gmsg import text
    for key,f in (('TIT','disc/DAT/TIT_DT.BIN'),('MGAME','disc/DAT/MGAME_DT.BIN')):
        t=bytearray(open(os.path.join(W,f),'rb').read());ch=apply(t,key);s=SPECS[key]
        import gmsg
        for pa in s['ptrs'][:3]+s['ptrs'][-2:]:
            o=struct.unpack('>I',bytes(t[pa:pa+4]))[0]-0x200000
            print(key,hex(o),repr(text(gmsg.msg(bytes(t),o),ch)))
        gmsg.font_sheet(bytes(t),s['fb'],len(ch),os.path.join(W,'shots/kf_%s.png'%key),cols=16)
