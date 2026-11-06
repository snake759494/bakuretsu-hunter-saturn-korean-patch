import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from emu import *
e=Emu(sys.argv[1],"bup.bin")
seq=sys.argv[2] # e.g. "600 S 300 A ..." frames or button
k=0
for t in seq.split():
    if t.isdigit(): e.run(int(t))
    elif t=='shot': e.shot(f'shots/{k:02d}.png'); k+=1
    elif t.startswith('save:'): e.cmd('save '+t[5:],'SAVED')
    elif t.startswith('dump:'): e.cmd('dump shots/'+t[5:],'DUMPED')
    else: e.press({'S':START,'A':A,'B':B,'C':C,'U':UP,'D':DOWN,'L':LEFT,'R':RIGHT}[t])
e.quit()
