import json,collections
lines=json.load(open('lines.json'))
ocr={}
for l in open('ocr.txt',encoding='utf-8-sig'):
    k,_,t=l.rstrip('\n').partition('\t'); ocr[int(k)]=t.replace(' ','')
V=collections.defaultdict(collections.Counter);ok=0
for i,l in enumerate(lines):
    t=ocr.get(i)
    if t is None: continue
    if len(t)==len(l['g']):
        ok+=1
        for g,c in zip(l['g'],t): V[g][c]+=1
print('aligned',ok,len(ocr))
lab={}
for g,c in V.items(): lab[g]=c.most_common(3)
json.dump({str(k):v for k,v in lab.items()},open('votes.json','w'),ensure_ascii=False)
G=open('glyphs.bin','rb').read()
print('glyphs voted',len(lab),'of',len(G)//128)
