import struct
from capstone import *

d = open('x86_64.so', 'rb').read()

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

shstr = secs[shstrndx][3]
names = {cstr(shstr+s[0]): s for s in secs}

text = names['.text']
text_vaddr, text_foff = text[2], text[3]

stub_vaddr = 0x6d0
stub_foff = stub_vaddr - text_vaddr + text_foff
stub_size = 0x720 - 0x6d0

md = Cs(CS_ARCH_X86, CS_MODE_64)
code = d[stub_foff:stub_foff+stub_size]
print("=== PLT STUBS 0x6d0 - 0x720 ===")
for ins in md.disasm(code, stub_vaddr):
    print("%x:\t%s\t%s" % (ins.address, ins.mnemonic, ins.op_str))

print()
for relname in ['.rela.plt', '.rela.dyn']:
    if relname in names:
        rel = names[relname]
        rel_off, rel_size, rel_link, rel_entsize = rel[3], rel[4], rel[5], rel[6]
        if rel_entsize == 0:
            rel_entsize = 24
        print(f"=== {relname} (size={rel_size}, entsize={rel_entsize}) ===")
        dynsym = names['.dynsym']
        dynstr = names['.dynstr']
        n_entries = rel_size // rel_entsize if rel_entsize else 0
        for i in range(n_entries):
            o = rel_off + i * rel_entsize
            r_offset, r_info, r_addend = struct.unpack_from('<QQq', d, o)
            sym_idx = r_info >> 32
            sym_o = dynsym[3] + sym_idx*24
            n, info, other, shndx, val, size = struct.unpack_from('<IBBHQQ', d, sym_o)
            symname = cstr(dynstr[3]+n) if n else "(none)"
            print(f"  r_offset={hex(r_offset)} sym={symname} addend={r_addend}")
