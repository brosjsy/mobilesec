import struct, sys

with open('classes2.dex', 'rb') as f:
    dex = f.read()

def u4(o): return struct.unpack_from('<I', dex, o)[0]
def u2(o): return struct.unpack_from('<H', dex, o)[0]
def s2(o): return struct.unpack_from('<h', dex, o)[0]

string_ids_off = u4(0x3C)
type_ids_off = u4(0x44)
field_ids_off = u4(0x54)
method_ids_off = u4(0x5C)

def read_uleb128(o):
    result=0; shift=0
    while True:
        b=dex[o]; o+=1
        result |= (b&0x7f)<<shift
        if not (b&0x80): break
        shift+=7
    return result,o

def get_string(idx):
    off=u4(string_ids_off+idx*4)
    size,o=read_uleb128(off)
    end=o; count=0
    while count<size and end<len(dex):
        if dex[end]==0: break
        end+=1; count+=1
    return dex[o:end].decode('utf-8',errors='replace')

def get_type_string(idx): return get_string(u4(type_ids_off+idx*4))

def get_method(idx):
    o=method_ids_off+idx*8
    class_idx=u2(o); name_idx=u4(o+4)
    return get_type_string(class_idx), get_string(name_idx)

def get_field(idx):
    o=field_ids_off+idx*8
    class_idx=u2(o); name_idx=u4(o+4)
    return get_type_string(class_idx), get_string(name_idx)

# Instruction format widths in CODE UNITS (2 bytes each), keyed by opcode value.
# Based on the standard Dalvik bytecode format table.
FORMATS = {
    0x00:1, 0x01:1, 0x02:2, 0x03:3, 0x04:1, 0x05:2, 0x06:3, 0x07:1, 0x08:2, 0x09:3,
    0x0a:1, 0x0b:1, 0x0c:1, 0x0d:1, 0x0e:1, 0x0f:1, 0x10:1, 0x11:1,
    0x12:1, 0x13:2, 0x14:3, 0x15:2, 0x16:2, 0x17:3, 0x18:5, 0x19:2, 0x1a:2, 0x1b:3,
    0x1c:2, 0x1d:1, 0x1e:1, 0x1f:2, 0x20:2, 0x21:1, 0x22:2, 0x23:2, 0x24:3, 0x25:3,
    0x26:3, 0x27:1, 0x28:1, 0x29:2, 0x2a:3, 0x2b:3, 0x2c:3,
    0x2d:2,0x2e:2,0x2f:2,0x30:2,0x31:2,
    0x32:2,0x33:2,0x34:2,0x35:2,0x36:2,0x37:2,0x38:2,0x39:2,0x3a:2,0x3b:2,0x3c:2,0x3d:2,
    0x44:2,0x45:2,0x46:2,0x47:2,0x48:2,0x49:2,0x4a:2,
    0x4b:2,0x4c:2,0x4d:2,0x4e:2,0x4f:2,0x50:2,0x51:2,
    0x52:2,0x53:2,0x54:2,0x55:2,0x56:2,0x57:2,0x58:2,0x59:2,0x5a:2,0x5b:2,0x5c:2,0x5d:2,0x5e:2,0x5f:2,
    0x60:2,0x61:2,0x62:2,0x63:2,0x64:2,0x65:2,0x66:2,0x67:2,0x68:2,0x69:2,0x6a:2,0x6b:2,0x6c:2,0x6d:2,
    0x6e:3,0x6f:3,0x70:3,0x71:3,0x72:3,
    0x74:3,0x75:3,0x76:3,0x77:3,0x78:3,
    0x7b:1,
    0x90:2,0x91:2,0x92:2,0x93:2,0x94:2,0x95:2,0x96:2,0x97:2,0x98:2,0x99:2,0x9a:2,0x9b:2,0x9c:2,0x9d:2,0x9e:2,0x9f:2,
    0xa0:2,0xa1:2,0xa2:2,0xa3:2,0xa4:2,0xa5:2,0xa6:2,0xa7:2,0xa8:2,0xa9:2,0xaa:2,0xab:2,0xac:2,0xad:2,0xae:2,0xaf:2,
    0xb0:1,0xb1:1,0xb2:1,0xb3:1,0xb4:1,0xb5:1,0xb6:1,0xb7:1,0xb8:1,0xb9:1,0xba:1,0xbb:1,0xbc:1,0xbd:1,0xbe:1,0xbf:1,
    0xc0:1,0xc1:1,0xc2:1,0xc3:1,0xc4:1,0xc5:1,0xc6:1,0xc7:1,0xc8:1,0xc9:1,0xca:1,0xcb:1,0xcc:1,0xcd:1,0xce:1,0xcf:1,
    0xd0:2,0xd1:2,0xd2:2,0xd3:2,0xd4:2,0xd5:2,0xd6:2,0xd7:2,0xd8:2,0xd9:2,0xda:2,0xdb:2,0xdc:2,0xdd:2,0xde:2,0xdf:2,
    0xe0:2,0xe1:2,0xe2:2,
    0x3e:1,0x3f:1,0x40:1,0x41:1,0x42:1,0x43:1,
    0x73:1,0x79:1,0x7a:1,
    0xe3:2,0xe4:2,0xe5:2,0xe6:2,0xe7:2,0xe8:2,0xe9:2,0xea:2,0xeb:2,0xec:2,0xed:2,0xee:2,0xef:2,0xf0:2,0xf1:2,0xf2:2,
    0xf3:2,0xf4:2,0xf5:2,0xf6:2,0xf7:2,0xf8:2,0xf9:2,0xfa:5,0xfb:5,0xfc:3,0xfd:3,0xfe:2,0xff:2,
}

MNEM = {
    0x00:'nop',0x01:'move',0x02:'move/from16',0x03:'move/16',0x04:'move-wide',0x05:'move-wide/from16',
    0x06:'move-wide/16',0x07:'move-object',0x08:'move-object/from16',0x09:'move-object/16',
    0x0a:'move-result',0x0b:'move-result-wide',0x0c:'move-result-object',0x0d:'move-exception',
    0x0e:'return-void',0x0f:'return',0x10:'return-wide',0x11:'return-object',
    0x12:'const/4',0x13:'const/16',0x14:'const',0x15:'const/high16',0x16:'const-wide/16',
    0x17:'const-wide/32',0x18:'const-wide',0x19:'const-wide/high16',0x1a:'const-string',
    0x1b:'const-string/jumbo',0x1c:'const-class',0x1d:'monitor-enter',0x1e:'monitor-exit',
    0x1f:'check-cast',0x20:'instance-of',0x21:'array-length',0x22:'new-instance',0x23:'new-array',
    0x24:'filled-new-array',0x25:'filled-new-array/range',0x26:'fill-array-data',0x27:'throw',
    0x28:'goto',0x29:'goto/16',0x2a:'goto/32',0x2b:'packed-switch',0x2c:'sparse-switch',
    0x2d:'cmpl-float',0x2e:'cmpg-float',0x2f:'cmpl-double',0x30:'cmpg-double',0x31:'cmp-long',
    0x32:'if-eq',0x33:'if-ne',0x34:'if-lt',0x35:'if-ge',0x36:'if-gt',0x37:'if-le',
    0x38:'if-eqz',0x39:'if-nez',0x3a:'if-ltz',0x3b:'if-gez',0x3c:'if-gtz',0x3d:'if-lez',
    0x44:'aget',0x45:'aget-wide',0x46:'aget-object',0x47:'aget-boolean',0x48:'aget-byte',0x49:'aget-char',0x4a:'aget-short',
    0x4b:'aput',0x4c:'aput-wide',0x4d:'aput-object',0x4e:'aput-boolean',0x4f:'aput-byte',0x50:'aput-char',0x51:'aput-short',
    0x52:'iget',0x53:'iget-wide',0x54:'iget-object',0x55:'iget-boolean',0x56:'iget-byte',0x57:'iget-char',0x58:'iget-short',
    0x59:'iput',0x5a:'iput-wide',0x5b:'iput-object',0x5c:'iput-boolean',0x5d:'iput-byte',0x5e:'iput-char',0x5f:'iput-short',
    0x60:'sget',0x61:'sget-wide',0x62:'sget-object',0x63:'sget-boolean',0x64:'sget-byte',0x65:'sget-char',0x66:'sget-short',
    0x67:'sput',0x68:'sput-wide',0x69:'sput-object',0x6a:'sput-boolean',0x6b:'sput-byte',0x6c:'sput-char',0x6d:'sput-short',
    0x6e:'invoke-virtual',0x6f:'invoke-super',0x70:'invoke-direct',0x71:'invoke-static',0x72:'invoke-interface',
    0x74:'invoke-virtual/range',0x75:'invoke-super/range',0x76:'invoke-direct/range',0x77:'invoke-static/range',0x78:'invoke-interface/range',
    0x7b:'neg-int',
    0x90:'add-int',0x91:'sub-int',0x92:'mul-int',0x93:'div-int',0x94:'rem-int',0x95:'and-int',0x96:'or-int',0x97:'xor-int',
    0x98:'shl-int',0x99:'shr-int',0x9a:'ushr-int',
    0xb0:'add-int/2addr',0xb1:'sub-int/2addr',0xb2:'mul-int/2addr',0xb3:'div-int/2addr',0xb7:'and-int/2addr',
    0xd0:'add-int/lit16',0xd1:'rsub-int',0xd2:'mul-int/lit16',0xd8:'add-int/lit8',0xda:'mul-int/lit8',
    0xe3:'const-method-handle',
    0xfa:'invoke-polymorphic',0xfc:'invoke-custom',
}

def get_str(idx):
    try: return get_string(idx)
    except Exception: return f"<str{idx}>"

def disasm(code_off, label):
    o=code_off
    registers_size=u2(o); ins_size=u2(o+2); outs_size=u2(o+4)
    insns_size=u4(o+12)
    insns_off=o+16
    insns=dex[insns_off:insns_off+insns_size*2]
    print(f"=== {label} === regs={registers_size} ins={ins_size} outs={outs_size} units={insns_size}")
    i=0
    unit=0
    while unit < insns_size:
        op = insns[i]
        width_units = FORMATS.get(op, 1)
        raw = insns[i:i+width_units*2]
        mnem = MNEM.get(op, f"op_{op:02x}")
        desc = ""
        # decode a few important formats fully
        if width_units==1 and op==0x12:  # const/4 vA, #+B  (11n)
            b0=raw[0]; b1=raw[1]
            vA = b1 & 0x0f
            lit = (b1 >> 4) & 0x0f
            if lit & 0x8: lit -= 16
            desc=f"v{vA}, #{lit}"
        elif op == 0x13 and len(raw)>=4:  # const/16 21s
            vAA=raw[1]; lit=struct.unpack_from('<h', raw, 2)[0]
            desc=f"v{vAA}, #{lit}"
        elif op == 0x14 and len(raw)>=6:  # const 31i
            vAA=raw[1]; lit=struct.unpack_from('<i', raw, 2)[0]
            desc=f"v{vAA}, #{lit}"
        elif op == 0x15 and len(raw)>=4:  # const/high16 21h
            vAA=raw[1]; hi=struct.unpack_from('<h', raw, 2)[0]
            desc=f"v{vAA}, #{hi<<16}"
        elif op in (0x02,0x08) and len(raw)>=4:  # move/from16, move-object/from16  22x
            vAA=raw[1]; vBBBB=raw[2]|(raw[3]<<8)
            desc=f"v{vAA}, v{vBBBB}"
        elif op in (0xd0,0xd8) and len(raw)>=4:  # add-int/lit16 (22s) / add-int/lit8 (22b)
            if op==0xd8:
                vAA=raw[1]; vBB=raw[2]
                lit = struct.unpack_from('<b', raw, 3)[0]
                desc=f"v{vAA}, v{vBB}, #{lit}"
            else:
                b1=raw[1]; vA=b1&0xf; vB=(b1>>4)&0xf
                lit=struct.unpack_from('<h', raw, 2)[0]
                desc=f"v{vA}, v{vB}, #{lit}"
        elif op in (0x1a,) and len(raw)>=4:  # 21c const-string
            vAA=raw[1]; idx=raw[2] | (raw[3]<<8)
            desc=f"v{vAA}, \"{get_str(idx)}\""
        elif op in (0x1b,) and len(raw)>=6:
            vAA=raw[1]; idx=raw[2]|(raw[3]<<8)|(raw[4]<<16)|(raw[5]<<24)
            desc=f"v{vAA}, \"{get_str(idx)}\""
        elif op in (0x22,) and len(raw)>=4:  # new-instance 21c
            vAA=raw[1]; idx=raw[2]|(raw[3]<<8)
            desc=f"v{vAA}, {get_type_string(idx)}"
        elif op in (0x1f,) and len(raw)>=4:  # check-cast 21c
            vAA=raw[1]; idx=raw[2]|(raw[3]<<8)
            desc=f"v{vAA}, {get_type_string(idx)}"
        elif op in (0x52,0x53,0x54,0x55,0x56,0x57,0x58,0x59,0x5a,0x5b,0x5c,0x5d,0x5e,0x5f) and len(raw)>=4:
            b0=raw[0]; b1=raw[1]
            vA = b1 & 0x0f; vB=(b1>>4)&0x0f
            fidx = raw[2] | (raw[3]<<8)
            cls,name = get_field(fidx)
            desc=f"v{vA}, v{vB}, {cls}->{name}"
        elif op in (0x60,0x61,0x62,0x63,0x64,0x65,0x66,0x67,0x68,0x69,0x6a,0x6b,0x6c,0x6d) and len(raw)>=4:
            vAA=raw[1]; fidx=raw[2]|(raw[3]<<8)
            cls,name=get_field(fidx)
            desc=f"v{vAA}, {cls}->{name}"
        elif op in (0x6e,0x6f,0x70,0x71,0x72) and len(raw)>=6:  # invoke 35c
            b0=raw[0]; b1=raw[1]
            argc = (b1>>4)&0x0f
            midx = raw[2] | (raw[3]<<8)
            regs_packed = raw[4] | (raw[5]<<8)
            cls,name=get_method(midx)
            regs=[]
            rp=regs_packed
            for k in range(argc):
                regs.append(str((rp >> (4*k)) & 0xf))
            desc=f"{{{', '.join('v'+r for r in regs)}}}, {cls}->{name}  (argc={argc})"
        elif op in (0x74,0x75,0x76,0x77,0x78) and len(raw)>=6:
            argc = raw[1]
            midx = raw[2]|(raw[3]<<8)
            first_reg = raw[4]|(raw[5]<<8)
            cls,name=get_method(midx)
            desc=f"v{first_reg}..v{first_reg+argc-1}, {cls}->{name} (argc={argc})"
        elif op in (0x38,0x39,0x3a,0x3b,0x3c,0x3d) and len(raw)>=4:  # if-eqz etc (21t)
            vAA=raw[1]
            offset = s2(0) if False else struct.unpack_from('<h', raw, 2)[0]
            desc=f"v{vAA}, +{offset} (target unit {unit+offset})"
        elif op in (0x32,0x33,0x34,0x35,0x36,0x37) and len(raw)>=4:  # if-eq etc (22t)
            b1=raw[1]; vA=b1&0xf; vB=(b1>>4)&0xf
            offset = struct.unpack_from('<h', raw, 2)[0]
            desc=f"v{vA}, v{vB}, +{offset} (target unit {unit+offset})"
        elif op == 0x21 and len(raw)>=2:  # array-length 12x
            b1=raw[1]; vA=b1&0xf; vB=(b1>>4)&0xf
            desc=f"v{vA}, v{vB}"
        elif op == 0x23 and len(raw)>=4:  # new-array 22c
            b1=raw[1]; vA=b1&0xf; vB=(b1>>4)&0xf
            tidx=raw[2]|(raw[3]<<8)
            desc=f"v{vA}, v{vB}, {get_type_string(tidx)}"
        elif op in (0x07,0x01) and len(raw)>=2:  # move/move-object 12x
            b1=raw[1]; vA=b1&0xf; vB=(b1>>4)&0xf
            desc=f"v{vA}, v{vB}"
        elif op in (0x0a,0x0c,0x0b) and len(raw)>=2:  # move-result*
            vAA=raw[1]
            desc=f"v{vAA}"
        elif op in (0x0f,0x11,0x10) and len(raw)>=2:
            vAA=raw[1]
            desc=f"v{vAA}"
        elif op in (0x44,0x45,0x46,0x47,0x48,0x49,0x4a,0x4b,0x4c,0x4d,0x4e,0x4f,0x50,0x51) and len(raw)>=4:
            # 23x: op AA BB CC  (aget-object dest=AA, array=BB, index=CC)
            vAA=raw[1]; vBB=raw[2]; vCC=raw[3]
            desc=f"v{vAA}, v{vBB}, v{vCC}"
        print(f"  [{unit:04x}] {mnem:20s} {desc}")
        i += width_units*2
        unit += width_units

if __name__=='__main__':
    off=int(sys.argv[1],16)
    label=sys.argv[2] if len(sys.argv)>2 else "method"
    disasm(off,label)
