import json,sys,numpy as np
from PIL import Image
def bdf(path):
    G={};L=open(path,encoding='utf8',errors='ignore').read().split('\n');i=0
    while i<len(L):
        if L[i].startswith('ENCODING'):
            cp=int(L[i].split()[1]);dw=bb=None;j=i
            while not L[j].startswith('BITMAP'):
                if L[j].startswith('DWIDTH'): dw=int(L[j].split()[1])
                if L[j].startswith('BBX'): bb=list(map(int,L[j].split()[1:]))
                j+=1
            rows=[];j+=1
            while not L[j].startswith('ENDCHAR'): rows.append(int(L[j],16));j+=1
            G[cp]=(dw,bb,rows,len(L[j-1].strip())*4 if rows else 8);i=j
        i+=1
    return G
F9=bdf('fonts/Galmuri9-2.40.4.bdf');F7=bdf('fonts/Galmuri7-2.40.4.bdf')
def render(s,F,asc):
    W=sum(F[ord(c)][0] for c in s);img=np.zeros((16,max(W,1)),np.uint8);x=0
    for c in s:
        dw,(w,h,ox,oy),rows,bits=F[ord(c)]
        for r,v in enumerate(rows):
            y=asc-oy-h+r
            for b in range(w):
                if v>>(bits-1-b)&1 and 0<=y<16: img[y,x+ox+b]=15
        x+=dw
    return img,W
def name(s):
    img,W=render(s,F9,13)
    if W>48: img,W=render(s,F7,12)
    assert W<=49,s
    out=np.zeros((16,48),np.uint8);o=(48-W)//2
    w=min(W,48-o);out[:,o:o+w]=img[:,:w];return out
def enc(P):
    b=bytearray(0x80)
    for y in range(16):
        for x in range(0,16,2):
            c=(y//8)*2+(x//8);b[c*32+(y%8)*4+(x%8)//2]=(P[y,x]<<4)|P[y,x+1]
    return bytes(b)
KO=['','아모레','안','바르바라','코우','메리나','고양이','고양이','오페라','린','장로','다니엘','캐롯','도터','가토','맘','마론','티라','쇼콜라','집사','수행원','수행원','내레이터','마을 남자','마을여자3','마을여자1','마을여자1','마을여자1','마을여자2','마을여자2','','와상','']
def patch(d,groups):
    d=bytearray(d)
    for gr,k in zip(groups,KO):
        if not k or not gr[0]: continue
        P=name(k)
        for j,t in enumerate(gr):
            off=0x1104+(t-0x380)*0x80;d[off:off+0x80]=enc(P[:,j*16:j*16+16])
    return bytes(d)
if __name__=='__main__':
    im=np.vstack([np.vstack([name(k)*16,np.zeros((2,48),np.uint8)]) for k in KO if k])
    Image.fromarray(im).resize((192,im.shape[0]*4),0).save('shots/kn.png')
