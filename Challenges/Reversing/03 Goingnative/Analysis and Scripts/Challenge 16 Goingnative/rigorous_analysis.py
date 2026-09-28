import struct
from capstone import *

d = open('x86_64.so', 'rb').read()

# Parse ELF section headers
shoff = struct.unpack_from('<Q', d, 0x28)[0]
shentsize, shnum, shstrndx = struct.unpack_from('<HHH', d, 0x3A)
secs = []
for i in range(shnum):
    o = shoff + i*shentsize
    name, typ, flags, addr, off, size, link, info, align, entsize = struct.unpack_from('<IIQQQQIIQQ', d, o)
    secs.append((name, typ, addr, off, size, link, entsize))

def cstr(o):
    e = d.index(b'\0', o)
    return d[o:e].decode()

shstr = secs[shstrndx][2] if False else secs[shstrndx][3]  # offset field index 3
names = {cstr(shstr+s[0]): s for s in secs}

dynsym = names['.dynsym']
dynstr = names['.dynstr']

# find the JNI function symbol precisely (name, value/vaddr, size)
target_fn = None
for i in range(dynsym[4]//24):
    o = dynsym[3] + i*24
    n, info, other, shndx, val, size = struct.unpack_from('<IBBHQQ', d, o)
    nm = cstr(dynstr[3]+n)
    if 'helloFromTheOtherSide' in nm:
        target_fn = (nm, val, size)
        print("Function:", nm, "vaddr=", hex(val), "size=", size)

text = names['.text']
text_vaddr, text_foff, text_size = text[2], text[3], text[4]
print("text section: vaddr=%s foff=%s size=%d" % (hex(text_vaddr), hex(text_foff), text_size))

nm, val, size = target_fn
func_foff = val - text_vaddr + text_foff
print("function file offset:", hex(func_foff))
print()

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

code = d[func_foff:func_foff+size]

print("=== FULL DISASSEMBLY WITH RIP-RELATIVE TARGET RESOLUTION ===")
for ins in md.disasm(code, val):
    line = "%x:\t%s\t%s" % (ins.address, ins.mnemonic, ins.op_str)
    # detect rip-relative operand like [rip + 0x92]
    if 'rip' in ins.op_str and '[' in ins.op_str:
        # capstone gives absolute displacement resolution via ins.disp when detail available
        try:
            for op in ins.operands:
                if op.type == 3:  # X86_OP_MEM (approx)
                    pass
        except Exception:
            pass
        # Manually parse "rip + 0xNN" or "rip - 0xNN"
        import re
        m = re.search(r'rip\s*([+-])\s*(0x[0-9a-fA-F]+)', ins.op_str)
        if m:
            sign = 1 if m.group(1) == '+' else -1
            disp = int(m.group(2), 16) * sign
            next_rip = ins.address + ins.size
            target_vaddr = next_rip + disp
            target_foff = target_vaddr - text_vaddr + text_foff
            snippet = d[target_foff:target_foff+16]
            ascii_snip = ''.join(chr(b) if 32<=b<127 else '.' for b in snippet)
            line += "   ; -> vaddr=%s foff=%s bytes=%s ascii='%s'" % (hex(target_vaddr), hex(target_foff), snippet.hex(), ascii_snip)
    print(line)
