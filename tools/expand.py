"""SH-2 1bpp->4bpp glyph expander, placed in LWRAM inside the DAT's original glyph area.
Called instead of the copy routine 0x0602FBBC (r4=src, r5=dst, r6=size).
If dst==0x25E40000: each source byte -> one 32-bit word of nibbles (0/F), size/4 bytes consumed.
Otherwise tail-jumps to the original copy routine."""
import struct
ORIG=0x0602FBBC
def assemble(base):
    code=[]
    def w(x): code.append(x)
    # 0: mov.l K_VRAM,r0
    w(None)          # placeholder idx0  mov.l @(d,PC),r0
    w(0x3050)        # 1: cmp/eq r5,r0
    w(None)          # 2: bf passthru
    w(None)          # 3: mova TABLE,r0
    w(0x6303)        # 4: mov r0,r3
    w(0x4609)        # 5: shlr2 r6
    w(0xE70F)        # 6: mov #15,r7
    # loop (7):
    w(0x6144)        # 7: mov.b @r4+,r1
    w(0x611C)        # 8: extu.b r1,r1
    w(0x6213)        # 9: mov r1,r2
    w(0x4209)        # 10: shlr2 r2
    w(0x4209)        # 11: shlr2 r2
    w(0x2179)        # 12: and r7,r1
    w(0x322C)        # 13: add r2,r2
    w(0x6023)        # 14: mov r2,r0
    w(0x023D)        # 15: mov.w @(r0,r3),r2
    w(0x622D)        # 16: extu.w r2,r2
    w(0x311C)        # 17: add r1,r1
    w(0x6013)        # 18: mov r1,r0
    w(0x013D)        # 19: mov.w @(r0,r3),r1
    w(0x611D)        # 20: extu.w r1,r1
    w(0x4228)        # 21: shll16 r2
    w(0x221B)        # 22: or r1,r2
    w(0x2522)        # 23: mov.l r2,@r5
    w(0x7504)        # 24: add #4,r5
    w(0x4610)        # 25: dt r6
    w(None)          # 26: bf loop
    w(0x000B)        # 27: rts
    w(0x0009)        # 28: nop
    # passthru (29):
    w(None)          # 29: mov.l ORIG,r0
    w(0x402B)        # 30: jmp @r0
    w(0x0009)        # 31: nop
    n=len(code)      # 32 halfwords = 64 bytes -> literals at 64 (aligned)
    K=n*2; O=K+4; T=O+4
    def pcrel_l(i,target): # mov.l / mova displacement
        pc=base+i*2; d=(target-((pc&~3)+4))//4; assert 0<=d<256 and (target-((pc&~3)+4))%4==0; return d
    def br(i,target):
        d=(target-(base+i*2+4))//2; assert -128<=d<128; return d&0xff
    code[0]=0xD000|pcrel_l(0,base+K)
    code[2]=0x8B00|br(2,base+29*2)
    code[3]=0xC700|pcrel_l(3,base+T)
    code[26]=0x8B00|br(26,base+7*2)
    code[29]=0xD000|pcrel_l(29,base+O)
    b=b''.join(struct.pack('>H',x) for x in code)
    b+=struct.pack('>II',0x25E40000,ORIG)
    tab=[]
    for v in range(16):
        h=0
        for bit in range(4):
            if v&(8>>bit): h|=0xF<<(12-4*bit)
        tab.append(h)
    b+=b''.join(struct.pack('>H',x) for x in tab)
    return b
def pack1(P):
    """16x16 0/1 array -> 32 bytes in cell order (TL,TR,BL,BR), 8 rows each, MSB=left pixel"""
    out=bytearray()
    for c in range(4):
        for y in range(8):
            v=0
            for x in range(8):
                v=(v<<1)|(1 if P[(c//2)*8+y][(c%2)*8+x] else 0)
            out.append(v)
    return bytes(out)
if __name__=='__main__':
    import capstone as cs
    base=0x00240204
    b=assemble(base)
    md=cs.Cs(cs.CS_ARCH_SH,cs.CS_MODE_SH2|cs.CS_MODE_BIG_ENDIAN)
    for i in md.disasm(b[:64],base): print(hex(i.address),i.mnemonic,i.op_str)
    print(len(b), b[64:].hex(' '))
