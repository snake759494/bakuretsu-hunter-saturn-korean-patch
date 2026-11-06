import socket,sys
from PIL import Image
def c(*a):
    s=socket.create_connection(('127.0.0.1',5577));s.send(' '.join(a).encode());s.settimeout(3000);r=s.recv(65536).decode();s.close();return r
def mash(tag,n,every,keys='A',wait=40):
    shots=[]
    for i in range(n):
        c(keys,str(wait))
        if i%every==every-1: k=f'{tag}{i:04d}';c('shot:'+k);shots.append(k)
    return shots
def sheet(shots,out,cols=6):
    w,h=213,150;rows=(len(shots)+cols-1)//cols;m=Image.new('RGB',(w*cols,h*rows))
    for i,k in enumerate(shots): m.paste(Image.open(f'shots/{k}.png').convert('RGB').resize((w,h)),((i%cols)*w,(i//cols)*h))
    m.save(out)
if __name__=='__main__':
    tag=sys.argv[1];n=int(sys.argv[2]);ev=int(sys.argv[3]);keys=sys.argv[4] if len(sys.argv)>4 else 'A'
    sheet(mash(tag,n,ev,keys),f'shots/sh_{tag}.png')
def tofile():
    for i in range(40):
        c('A' if i%2 else 'S','120','shot:_t');im=Image.open('shots/_t.png').convert('RGB').resize((320,224))
        r,g,b=im.getpixel((160,100))
        if r>120 and g>100 and b<90 and abs(r-g)<70: return True
    return False
def newgame():
    assert tofile(); c('D','30','A','300','A','300')
