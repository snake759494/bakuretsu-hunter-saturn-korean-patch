import sys;sys.path.insert(0,'tools')
from cdimg import Image
src,dst,prg=sys.argv[1:4];key=sys.argv[4] if len(sys.argv)>4 else '/PRG/MEN1_01.BIN'
img=Image(src);e={x['name']:x for x in img.dir_entries()}['0.BIN']
d=bytearray(img.read(e['lba'],(e['size']+2047)//2048))
i=d.find(key.encode());L=len(key);n=('/PRG/'+prg).encode();d[i:i+L]=n+b'\0'*(L-len(n))
img.write_data(e['lba'],bytes(d));img.save(dst)
