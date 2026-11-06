import json
sc=json.load(open('scenes.json'))
v=json.load(open('votes.json')); lab={int(k):x[0][0] for k,x in v.items()}
for k,c in json.load(open('glyph_fix.json')).items(): lab[int(k)]=c
miss=set()
def dec(e,ws):
    s=''
    for w in ws:
        if w==0xfffe: s+='\n'
        elif w==0xfffc: s+='▼\n'
        elif w==0xffff: pass
        elif w>=0xff00: s+='{%04x}'%w
        else:
            g=e['gmap'][w]
            if g not in lab: miss.add(g)
            s+=lab.get(g,'⟨?%d⟩'%g)
    return s
out={}
for nm,e in sc.items():
    out[nm]=[dec(e,m['w']) for m in e['msgs']]
json.dump(out,open('ja.json','w'),ensure_ascii=False,indent=1)
print('missing',sorted(miss))
