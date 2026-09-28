import struct

with open('classes.dex', 'rb') as f:
    dex = f.read()

def u4(o): return struct.unpack_from('<I', dex, o)[0]
def u2(o): return struct.unpack_from('<H', dex, o)[0]

# DEX header
string_ids_size = u4(0x38)
string_ids_off = u4(0x3C)
type_ids_size = u4(0x40)
type_ids_off = u4(0x44)
proto_ids_size = u4(0x48)
proto_ids_off = u4(0x4C)
field_ids_size = u4(0x50)
field_ids_off = u4(0x54)
method_ids_size = u4(0x58)
method_ids_off = u4(0x5C)
class_defs_size = u4(0x60)
class_defs_off = u4(0x64)

def read_uleb128(o):
    result = 0
    shift = 0
    while True:
        b = dex[o]
        o += 1
        result |= (b & 0x7f) << shift
        if not (b & 0x80):
            break
        shift += 7
    return result, o

def get_string(idx):
    off = u4(string_ids_off + idx*4)
    size, o = read_uleb128(off)
    end = dex.index(b'\x00', o) if b'\x00' in dex[o:o+size*3+5] else o+size
    return dex[o:end].decode('utf-8', errors='replace')

def get_type_string(idx):
    string_idx = u4(type_ids_off + idx*4)
    return get_string(string_idx)

def get_proto(idx):
    o = proto_ids_off + idx*12
    shorty_idx = u4(o)
    return get_string(shorty_idx)

def get_method(idx):
    o = method_ids_off + idx*8
    class_idx = u2(o)
    proto_idx = u2(o+2)
    name_idx = u4(o+4)
    return get_type_string(class_idx), get_string(name_idx), get_proto(proto_idx)

def get_field(idx):
    o = field_ids_off + idx*8
    class_idx = u2(o)
    type_idx = u2(o+2)
    name_idx = u4(o+4)
    return get_type_string(class_idx), get_string(name_idx), get_type_string(type_idx)

# Find MainActivity class def
print("[*] Scanning class defs for MainActivity / FlagChecker...")
target_classes = {}
for i in range(class_defs_size):
    o = class_defs_off + i*32
    class_idx = u4(o)
    class_data_off = u4(o+24)
    cname = get_type_string(class_idx)
    if 'MainActivity' in cname or 'FlagChecker' in cname:
        target_classes[cname] = class_data_off
        print(f"  {cname} class_data_off=0x{class_data_off:x}")

print()

def parse_class_data(off):
    o = off
    static_fields_size, o = read_uleb128(o)
    instance_fields_size, o = read_uleb128(o)
    direct_methods_size, o = read_uleb128(o)
    virtual_methods_size, o = read_uleb128(o)

    def skip_fields(n, o):
        prev = 0
        for _ in range(n):
            diff, o = read_uleb128(o)
            access, o = read_uleb128(o)
        return o

    o = skip_fields(static_fields_size, o)
    o = skip_fields(instance_fields_size, o)

    methods = []
    prev_idx = 0
    for _ in range(direct_methods_size):
        diff, o = read_uleb128(o)
        access, o = read_uleb128(o)
        code_off, o = read_uleb128(o)
        prev_idx += diff
        methods.append((prev_idx, access, code_off, True))

    prev_idx = 0
    for _ in range(virtual_methods_size):
        diff, o = read_uleb128(o)
        access, o = read_uleb128(o)
        code_off, o = read_uleb128(o)
        prev_idx += diff
        methods.append((prev_idx, access, code_off, False))

    return methods

for cname, cdoff in target_classes.items():
    print(f"=== {cname} ===")
    methods = parse_class_data(cdoff)
    for method_idx, access, code_off, is_direct in methods:
        mclass, mname, mproto = get_method(method_idx)
        print(f"  method: {mname} {mproto} code_off=0x{code_off:x} direct={is_direct}")
    print()
