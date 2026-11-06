import json,sys,os,re
sys.path.insert(0,'tools')
from wrap import convert,cells
ja=json.load(open('ja.json',encoding='utf-8'))
for nm in sys.argv[1:]:
    out,bad=convert(nm)
    for b in bad: print('LONG',nm,b)
    for i,(j,k) in enumerate(zip(ja[nm],out)):
        if k is None: continue
        if '\n' not in j and '▼' not in j:
            if '\n' in k or '▼' in k: print('MULTI',nm,i,repr(j),repr(k))
            elif cells(k)>cells(j) and cells(j)<15: print('WIDER',nm,i,cells(j),cells(k),k)
