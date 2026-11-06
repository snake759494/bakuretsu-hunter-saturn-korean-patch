import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from cdimg import Image
img=Image(sys.argv[1]); out=sys.argv[2]
want=sys.argv[3:]  # dir prefixes
for line in open('files.txt'):
    lba,size,p=line.split(); lba=int(lba); size=int(size)
    if want and not any(p.strip('/').startswith(w) for w in want): continue
    d=os.path.join(out,p.strip('/').replace(';1',''))
    os.makedirs(os.path.dirname(d),exist_ok=True)
    open(d,'wb').write(img.read(lba,(size+2047)//2048)[:size])
