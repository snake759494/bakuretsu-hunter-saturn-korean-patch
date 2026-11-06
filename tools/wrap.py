"""tr/<scene>.txt (N<TAB>text) -> ko/<scene>.json
text: pages separated by '▼', '/' forces a line break, '\\' = literal raw (no wrap) message.
Quoted messages (starting with 「) get 「 + 14 cells first line and 　 + 14 cells continuation lines.
"""
import json,sys,os,re
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIDTH=15
NOSP=set(',.!?、。！？')
PUNCT=set('.,!?。、！？」』~～…)')
def cells(s): return len(re.findall(r'⟨\d+⟩|.',s))
def wrap_page(text,first_prefix,cont_prefix='　'):
    lines=[];segs=text.split('/')
    pre=first_prefix
    for seg in segs:
        words=seg.strip(' ').split(' ')
        cur=pre
        for w in words:
            if w=='': continue
            cand=(cur+w) if cur==pre else cur+('' if cur[-1] in NOSP else ' ')+w
            if cells(cand)<=WIDTH: cur=cand;continue
            # try break
            if cells(cur)>cells(pre):
                lines.append(cur); pre=cont_prefix; cur=pre
                cand=cur+w
                if cells(cand)<=WIDTH: cur=cand;continue
            # hard split long word
            toks=re.findall(r'⟨\d+⟩|.',w)
            for t in toks:
                if cells(cur)+1>WIDTH:
                    if t in PUNCT: cur+=t; continue  # allow punct overflow -> flagged later
                    lines.append(cur); pre=cont_prefix; cur=pre
                cur+=t
        lines.append(cur); pre=cont_prefix
    return lines
def wrap_msg(text):
    if text.startswith('\\'): return text[1:].replace('/','\n')
    quoted=text.startswith(('「','　'))
    pages=text.split('▼')
    out=[];first=True
    for pg in pages:
        pg=pg.strip(' ')
        if first and text.startswith('　'): lines=wrap_page(pg[1:],'　')
        elif first and quoted: lines=wrap_page(pg[1:],'「')
        elif quoted: lines=wrap_page(pg,'　')
        else: lines=wrap_page(pg,'')
        first=False
        # split into chunks of 3 lines
        for i in range(0,len(lines),3):
            out.append('\n'.join(lines[i:i+3]))
    return '▼\n'.join(out)
def convert(nm):
    src=os.path.join(W,'tr',nm+'.txt'); res={}
    for l in open(src,encoding='utf-8'):
        l=l.rstrip('\n')
        if not l.strip() or l.startswith('//'): continue
        k,_,t=l.partition('\t'); res[int(k)]=t
    ja=json.load(open(os.path.join(W,'scenes.json')))[nm]['msgs']  # message count only
    out=[]
    for i in range(len(ja)):
        if i not in res: print(nm,'missing',i); out.append(None); continue
        out.append(wrap_msg(res[i]))
    bad=[]
    for i,s in enumerate(out):
        if s is None: continue
        for ln in s.replace('▼','').split('\n'):
            if cells(ln)>WIDTH: bad.append((i,ln))
    os.makedirs(os.path.join(W,'ko'),exist_ok=True)
    if None not in out: json.dump(out,open(os.path.join(W,'ko',nm+'.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
    return out,bad
if __name__=='__main__':
    for nm in sys.argv[1:]:
        out,bad=convert(nm)
        for b in bad: print('LONG',nm,b)
        if '-v' in os.environ.get('V',''):
            for i,s in enumerate(out): print(f'#{i}\n{s}')
