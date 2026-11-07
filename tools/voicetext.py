"""Text-mode + voice patch for PRG/MEN*.BIN.

Message start (0x0602d010) picks the voice handler (0x0602d404) when the option
word 0x0605694c != 0, else the text (typewriter) handler 0x0602d064.
We rewrite the voice handler area (0x0602d404..0x0602d4cf) as:
  voice_entry  : same behaviour as before (request voice, draw name, -> 0x0602d4d0)
  text_entry   : request voice, then jump to the text handler 0x0602d064
  req          : stop the current voice (0x0602f6bc) and request this message's voice
and point the text branch literal (0x0602d060) at text_entry.
BSS addresses differ per file, so constants are read from the original pool.
"""
import struct
BASE = 0x0602C000
A0, A1 = 0x0602d404, 0x0602d4d0          # rewritten region
POOL_OLD = 0x0602d4ac                    # 490bc 53920 48a4c 49dcc 43eb4 25e78304 427e0 fb40 d4d0
TEXT_LIT = 0x0602d060                    # literal holding 0x0602d064
STOP = 0x0602f6bc
TEXT = 0x0602d064

R = lambda n: int(n[1:])

class Asm:
    def __init__(s, org): s.org = org; s.items = []; s.lab = {}; s.lits = {}
    def L(s, name): s.items.append(('L', name))
    def w(s, v): s.items.append(('w', v))
    def j(s, kind, op, lab): s.items.append(('j', kind, op, lab))   # branch to label
    def lit(s, rn, val): s.items.append(('lit', rn, val))            # mov.l @(disp,PC),Rn
    def build(s):
        s.lab.setdefault('TEXT', TEXT)
        # pass 1: sizes are fixed (2 bytes each), literals after code, 4-aligned
        pc = s.org; pos = {}
        for it in s.items:
            if it[0] == 'L': s.lab[it[1]] = pc
            else: pc += 2
        end = pc
        lp = (end + 3) & ~3
        vals = []
        for it in s.items:
            if it[0] == 'lit' and it[2] not in vals: vals.append(it[2])
        laddr = {v: lp + 4 * i for i, v in enumerate(vals)}
        out = bytearray(); pc = s.org
        for it in s.items:
            if it[0] == 'L': continue
            if it[0] == 'w': op = it[1]
            elif it[0] == 'lit':
                a = laddr[it[2]]; d = (a - ((pc & ~3) + 4)) // 4
                assert 0 <= d < 256, d
                op = 0xD000 | (it[1] << 8) | d
            else:
                kind, op0, lab = it[1], it[2], it[3]
                d = (s.lab[lab] - (pc + 4)) // 2
                if kind == 8: assert -128 <= d < 128; op = op0 | (d & 0xff)
                else: assert -2048 <= d < 2048; op = op0 | (d & 0xfff)
            out += struct.pack('>H', op); pc += 2
        out += bytes(lp - end)
        for v in vals: out += struct.pack('>I', v)
        return bytes(out)

def u32(m, a): return struct.unpack('>I', m[a - BASE:a - BASE + 4])[0]

def patch(m):
    """m: bytearray of a MEN file (original layout). Returns True if patched."""
    if u32(m, TEXT_LIT) != TEXT or u32(m, POOL_OLD + 32) != A1: return False
    K = [u32(m, POOL_OLD + 4 * i) for i in range(9)]
    k490bc, k53920, k48a4c, k49dcc, k43eb4, kvram, k427e0, kfb40, kd4d0 = K
    a = Asm(A0)
    # ---- voice_entry (0x0602d404, entry kept) ----
    a.w(0x4F22)            # sts.l pr,@-r15
    a.w(0x2F86)            # mov.l r8,@-r15
    a.j(12, 0xB000, 'req'); a.w(0x6843)   # bsr req ; mov r4,r8
    a.w(0x2008)            # tst r0,r0
    a.j(8, 0x8900, 'skip') # bt skip
    a.lit(2, k43eb4)
    a.w(0x4008); a.w(0x4000)   # shll2 r0 ; shll r0   (id*8)
    a.w(0x320C)            # add r0,r2
    a.w(0x8521)            # mov.w @(2,r2),r0
    a.lit(1, k427e0)
    a.w(0x2008)            # tst r0,r0
    a.j(8, 0x8B00, 'first')   # bf first
    a.w(0x6021)            # mov.w @r2,r0
    a.w(0x600D)            # extu.w r0,r0
    a.w(0x4008)            # shll2 r0
    a.w(0x041E)            # mov.l @(r0,r1),r4
    a.j(12, 0xA000, 'draw'); a.w(0x0009)   # bra draw
    a.L('first'); a.w(0x6412)  # mov.l @r1,r4
    a.L('draw')
    a.lit(5, kvram)
    a.w(0xE603); a.w(0xE700)   # mov #3,r6 ; mov #0,r7
    a.w(0xE108); a.w(0x4118)   # mov #8,r1 ; shll8 r1
    a.w(0x2F16)            # mov.l r1,@-r15
    a.lit(0, kfb40)
    a.w(0x400B); a.w(0x0009)   # jsr @r0 ; nop
    a.w(0x7F04)            # add #4,r15
    a.L('skip')
    a.lit(1, kd4d0)
    a.w(0x1813)            # mov.l r1,@(12,r8)
    a.w(0x410B); a.w(0x6483)   # jsr @r1 ; mov r8,r4
    a.w(0x68F6)            # mov.l @r15+,r8
    a.w(0x000B); a.w(0x4F26)   # rts ; lds.l @r15+,pr
    # ---- text_entry ----
    a.L('text')
    a.w(0x4F22)                # sts.l pr,@-r15
    a.j(12, 0xB000, 'req'); a.w(0x2F46)   # bsr req ; mov.l r4,@-r15
    a.w(0x64F6)                # mov.l @r15+,r4
    a.j(12, 0xA000, 'TEXT'); a.w(0x4F26)  # bra text handler ; lds.l @r15+,pr
    # ---- req(r4) -> r0 = voice id or 0 ----
    a.L('req')
    a.w(0x4F22)            # sts.l pr,@-r15
    a.w(0x6143)            # mov r4,r1
    a.w(0x7144)            # add #68,r1
    a.w(0x6211)            # mov.w @r1,r2
    a.w(0x6143)            # mov r4,r1
    a.w(0x7170)            # add #112,r1
    a.w(0x6312)            # mov.l @r1,r3
    a.w(0xE006)            # mov #6,r0
    a.w(0x220E)            # mulu.w r0,r2
    a.w(0x001A)            # sts macl,r0   (idx*6)
    a.w(0x013D)            # mov.w @(r0,r3),r1
    a.w(0x611D)            # extu.w r1,r1
    a.w(0x2118)            # tst r1,r1
    a.j(8, 0x8900, 'none') # bt none
    a.w(0x2F16)            # mov.l r1,@-r15
    a.lit(0, STOP)
    a.w(0x400B); a.w(0x0009)   # jsr @r0 (stop current voice)
    a.w(0x61F6)            # mov.l @r15+,r1
    a.lit(2, k53920); a.w(0xE001); a.w(0x2202)   # flag=1
    a.lit(2, k49dcc); a.w(0x2211)                # mov.w r1,@r2
    a.lit(2, k48a4c); a.w(0x2211)
    a.w(0x6013)            # mov r1,r0
    a.L('out')
    a.lit(2, k490bc); a.w(0xE300); a.w(0x2232)   # @490bc = 0
    a.w(0x4F26); a.w(0x000B); a.w(0x0009)
    a.L('none'); a.j(12, 0xA000, 'out'); a.w(0xE000)   # bra out ; mov #0,r0
    code = a.build()
    assert A0 + len(code) <= A1, hex(A0 + len(code))
    m[A0 - BASE:A0 - BASE + len(code)] = code
    m[A0 - BASE + len(code):A1 - BASE] = bytes(A1 - A0 - len(code))
    m[TEXT_LIT - BASE:TEXT_LIT - BASE + 4] = struct.pack('>I', a.lab['text'])
    return True

if __name__ == '__main__':
    import sys
    m = bytearray(open(sys.argv[1], 'rb').read())
    print(patch(m))
    open(sys.argv[2], 'wb').write(m)
