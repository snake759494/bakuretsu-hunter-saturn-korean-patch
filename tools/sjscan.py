import sys
def scan(b,minlen=4):
    i=0;res=[]
    while i<len(b)-1:
        j=i;s=[]
        while j<len(b)-1:
            c=b[j]
            if (0x81<=c<=0x9f or 0xe0<=c<=0xea) and 0x40<=b[j+1]<=0xfc and b[j+1]!=0x7f: s.append(b[j:j+2]);j+=2
            else: break
        if len(s)>=minlen:
            try: res.append((i,b''.join(s).decode('cp932')))
            except: pass
            i=j
        else: i+=1
    return res
for f in sys.argv[1:]:
    r=scan(open(f,'rb').read())
    print(f,len(r))
    for o,t in r[:int(__import__('os').environ.get('N','5'))]: print(f'  {o:06x} {t}')
