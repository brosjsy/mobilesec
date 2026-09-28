import struct
import sys

with open('classes.dex', 'rb') as f:
    dex = f.read()

def u4(o): return struct.unpack_from('<I', dex, o)[0]
def u2(o): return struct.unpack_from('<H', dex, o)[0]

string_ids_off = u4(0x3C)
type_ids_off = u4(0x44)
proto_ids_off = u4(0x48)
field_ids_off = u4(0x54)
method_ids_off = u4(0x5C)

def read_uleb128(o):
    result = 0; shift = 0
    while True:
        b = dex[o]; o += 1
        result |= (b & 0x7f) << shift
        if not (b & 0x80): break
        shift += 7
    return result, o

def get_string(idx):
    off = u4(string_ids_off + idx*4)
    size, o = read_uleb128(off)
    # find null terminator, MUTF-8 close enough for ascii
    end = o
    count = 0
    while count < size and end < len(dex):
        if dex[end] == 0:
            break
        end += 1
        count += 1
    return dex[o:end].decode('utf-8', errors='replace')

def get_type_string(idx):
    return get_string(u4(type_ids_off + idx*4))

def get_method(idx):
    o = method_ids_off + idx*8
    class_idx = u2(o); proto_idx = u2(o+2); name_idx = u4(o+4)
    return get_type_string(class_idx), get_string(name_idx)

def get_field(idx):
    o = field_ids_off + idx*8
    class_idx = u2(o); type_idx = u2(o+2); name_idx = u4(o+4)
    return get_type_string(class_idx), get_string(name_idx)

def disasm_code_item(code_off, label):
    o = code_off
    registers_size = u2(o)
    ins_size = u2(o+2)
    outs_size = u2(o+4)
    tries_size = u2(o+6)
    debug_info_off = u4(o+8)
    insns_size = u4(o+12)
    insns_off = o + 16
    print(f"=== {label} === regs={registers_size} ins={ins_size} outs={outs_size} insns_size={insns_size} (code units)")

    insns = dex[insns_off:insns_off + insns_size*2]
    i = 0
    while i < len(insns):
        op = insns[i]
        start = i
        if op == 0x1a:  # const-string vAA, string@BBBB
            vAA = insns[i+1]
            idx = insns[i+2] | (insns[i+3] << 8)
            s = get_string(idx)
            print(f"  [{i//2:04x}] const-string v{vAA}, \"{s}\"")
            i += 4
        elif op == 0x1b:  # const-string/jumbo
            vAA = insns[i+1]
            idx = insns[i+2] | (insns[i+3]<<8) | (insns[i+4]<<16) | (insns[i+5]<<24)
            s = get_string(idx)
            print(f"  [{i//2:04x}] const-string/jumbo v{vAA}, \"{s}\"")
            i += 6
        elif op in (0x6e, 0x6f, 0x70, 0x71, 0x72):  # invoke-*
            names_map = {0x6e:'invoke-virtual',0x6f:'invoke-super',0x70:'invoke-direct',0x71:'invoke-static',0x72:'invoke-interface'}
            argc_regs = insns[i+1] >> 4
            method_idx = insns[i+2] | (insns[i+3]<<8)
            cls, name = get_method(method_idx)
            regs_byte = insns[i+4] | (insns[i+5]<<8)
            print(f"  [{i//2:04x}] {names_map[op]} {{...}}, {cls}->{name}  (argc={argc_regs})")
            i += 6
        elif op in (0x74,0x75,0x76,0x77,0x78):
            names_map = {0x74:'invoke-virtual/range',0x75:'invoke-super/range',0x76:'invoke-direct/range',0x77:'invoke-static/range',0x78:'invoke-interface/range'}
            method_idx = insns[i+2] | (insns[i+3]<<8)
            cls, name = get_method(method_idx)
            print(f"  [{i//2:04x}] {names_map[op]} {cls}->{name}")
            i += 6
        elif op == 0x62 or op == 0x63:  # sget-object / sput-object etc could vary; handle generic sget/sput with field
            vAA = insns[i+1]
            fidx = insns[i+2] | (insns[i+3]<<8)
            cls, name = get_field(fidx)
            print(f"  [{i//2:04x}] sget/sput v{vAA}, {cls}->{name}")
            i += 4
        elif op == 0x0e:  # return-void
            print(f"  [{i//2:04x}] return-void")
            i += 2
        elif op in (0x0f,0x10,0x11):  # return, return-wide, return-object
            vAA = insns[i+1]
            names_map={0x0f:'return',0x10:'return-wide',0x11:'return-object'}
            print(f"  [{i//2:04x}] {names_map[op]} v{vAA}")
            i += 2
        elif op == 0x22:  # new-instance
            vAA = insns[i+1]
            tidx = insns[i+2] | (insns[i+3]<<8)
            t = get_type_string(tidx)
            print(f"  [{i//2:04x}] new-instance v{vAA}, {t}")
            i += 4
        else:
            # unknown/other opcode - skip minimal 2 bytes (best-effort, may misalign)
            print(f"  [{i//2:04x}] op=0x{op:02x} (raw skip 2)")
            i += 2
        if i == start:
            i += 2  # safety

if __name__ == '__main__':
    offset = int(sys.argv[1], 16)
    label = sys.argv[2] if len(sys.argv) > 2 else "method"
    disasm_code_item(offset, label)
