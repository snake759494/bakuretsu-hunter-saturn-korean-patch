import sys,glob
word=sys.argv[1]; files=sys.argv[2:]
def check(seq):
    m={};r={}
    for ch,v in zip(word,seq):
        if m.setdefault(ch,v)!=v: return False
        if r.setdefault(v,ch)!=ch: return False
    return True
n=len(word)
for f in files:
    b=open(f,'rb').read()
    for w in (1,2):
        for st in range(0,w):
            vals=[b[i:i+w] for i in range(st,len(b)-w+1,w)]
            for i in range(len(vals)-n):
                if vals[i]==vals[i+1]: continue
                if check(vals[i:i+n]):
                    print(f,w,hex(st+i*w),b[st+i*w:st+(i+n)*w].hex(' '))
