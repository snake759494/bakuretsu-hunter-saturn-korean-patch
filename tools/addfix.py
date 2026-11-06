import json,sys
f=json.load(open('glyph_fix.json'))
for a in sys.argv[1:]:
    k,v=a.split('=',1); f[k]=v
json.dump(f,open('glyph_fix.json','w'),ensure_ascii=False)
print(len(f))
