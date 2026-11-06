import sys,os,socket
sys.path.insert(0,os.path.dirname(__file__))
from emu import *
e=Emu(sys.argv[1],"bup.bin")
BT={'S':START,'A':A,'B':B,'C':C,'U':UP,'D':DOWN,'L':LEFT,'R':RIGHT,'X':X,'Y':Y,'Z':Z}
s=socket.socket();s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);s.bind(('127.0.0.1',5577));s.listen(1)
while True:
    c,_=s.accept();seq=c.recv(65536).decode();out=[]
    if seq.strip()=='quit': e.quit();c.send(b'bye');break
    try:
        for t in seq.split():
            if t.isdigit(): e.run(int(t))
            elif t.startswith('shot:'): e.shot('shots/'+t[5:]+'.png'); out.append(t)
            elif t.startswith('save:'): e.cmd('save '+t[5:],'SAVED')
            elif t.startswith('load:'): e.cmd('load '+t[5:],'LOADED')
            elif t.startswith('dump:'): e.cmd('dump shots/'+t[5:],'DUMPED')
            elif t.startswith('vdump:'): e.cmd('vdump shots/'+t[6:],'VDUMPED')
            elif t.startswith('disc:'): out.append(e.cmd('disc '+t[5:],'DISC'))
            elif t=='reset': e.cmd('reset','RESET')
            else:
                m=0
                for ch in t: m|=BT[ch]
                e.press(m)
    except Exception as ex: out.append('ERR '+repr(ex))
    c.send((' '.join(out) or 'ok').encode());c.close()
