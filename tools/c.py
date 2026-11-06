import socket,sys
from PIL import Image
args=sys.argv[1:]
s=socket.create_connection(('127.0.0.1',5577));s.send(' '.join(args).encode());s.settimeout(3000)
r=s.recv(65536).decode();print(r)
shots=[t[5:] for t in args if t.startswith('shot:')]
if len(shots)>1:
    w,h=320,224;n=len(shots);cols=min(4,n);rows=(n+cols-1)//cols
    m=Image.new('RGB',(w*cols,h*rows))
    for i,k in enumerate(shots): m.paste(Image.open(f'shots/{k}.png').convert('RGB').resize((w,h)),((i%cols)*w,(i//cols)*h))
    m.save('shots/m.png')
