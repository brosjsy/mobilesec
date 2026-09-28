import struct, sys
from capstone import *
d=open('x86_64.so','rb').read()
shoff=struct.unpack_from('<Q',d,0x28)[0]
shentsize,shnum,shstrndx=struct.unpack_from('<HHH',d,0x3A)
secs=[]
for i in range(shnum):
    o=shoff+i*shentsize
    name,typ,flags,addr,off,size,link,info,align,entsize=struct.unpack_from('<IIQQQQIIQQ',d,o)
    secs.append((name,typ,addr,off,size,link,entsize))
def cstr(o):
    e=d.index(b'\0',o);return d[o:e].decode()
shstr=secs[shstrndx][3]
names={cstr(shstr+s[0]):s for s in secs}
dynsym=names['.dynsym'];dynstr=names['.dynstr']
for i in range(dynsym[4]//24):
    o=dynsym[3]+i*24
    n,info,other,shndx,val,size=struct.unpack_from('<IBBHQQ',d,o)
    nm=cstr(dynstr[3]+n)
    if 'Java' in nm: fn=(nm,val,size); print(nm,hex(val),size)
text=names['.text']
print('text',hex(text[2]),hex(text[3]),text[4])
nm,val,size=fn
off=val-text[2]+text[3]
md=Cs(CS_ARCH_X86,CS_MODE_64)
for ins in md.disasm(d[off:off+size],val):
    print("%x:\t%s\t%s"%(ins.address,ins.mnemonic,ins.op_str))
