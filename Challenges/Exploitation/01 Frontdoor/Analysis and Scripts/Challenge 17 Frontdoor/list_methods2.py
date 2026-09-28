import struct, sys

dex_path = sys.argv[1]
class_off = int(sys.argv[2], 16)
label = sys.argv[3] if len(sys.argv)>3 else 'cls'

dex = open(dex_path,'rb').read()
def u4(o): return struct.unpack_from('<I', dex, o)[0]
def u2(o): return struct.unpack_from('<H', dex, o)[0]
string_ids_off = u4(0x3C)
type_ids_off = u4(0x44)
proto_ids_off = u4(0x4C)
method_ids_off = u4(0x5C)
def read_uleb128(o):
    result=0;shift=0
    while True:
        b=dex[o];o+=1
        result |= (b&0x7f)<<shift
        if not(b&0x80): break
        shift+=7
    return result,o
def get_string(idx):
    off=u4(string_ids_off+idx*4)
    size,o=read_uleb128(off)
    end=o;count=0
    while count<size and end<len(dex):
        if dex[end]==0: break
        end+=1;count+=1
    return dex[o:end].decode('utf-8',errors='replace')
def get_type_string(idx): return get_string(u4(type_ids_off+idx*4))
def get_proto(idx):
    o=proto_ids_off+idx*12
    return get_string(u4(o))
def get_method(idx):
    o=method_ids_off+idx*8
    class_idx=u2(o); proto_idx=u2(o+2); name_idx=u4(o+4)
    return get_type_string(class_idx), get_string(name_idx), get_proto(proto_idx)
def get_field(idx):
    field_ids_off=u4(0x54)
    o=field_ids_off+idx*8
    class_idx=u2(o); type_idx=u2(o+2); name_idx=u4(o+4)
    return get_type_string(class_idx), get_string(name_idx), get_type_string(type_idx)

def parse_class_data(off):
    o=off
    static_fields_size,o=read_uleb128(o)
    instance_fields_size,o=read_uleb128(o)
    direct_methods_size,o=read_uleb128(o)
    virtual_methods_size,o=read_uleb128(o)
    fields=[]
    def do_fields(n,o):
        prev=0
        for _ in range(n):
            diff,o=read_uleb128(o); access,o=read_uleb128(o)
            prev+=diff
            fields.append(prev)
        return o
    o=do_fields(static_fields_size,o)
    o=do_fields(instance_fields_size,o)
    methods=[]
    prev=0
    for _ in range(direct_methods_size):
        diff,o=read_uleb128(o); access,o=read_uleb128(o); code_off,o=read_uleb128(o)
        prev+=diff; methods.append((prev,access,code_off,True))
    prev=0
    for _ in range(virtual_methods_size):
        diff,o=read_uleb128(o); access,o=read_uleb128(o); code_off,o=read_uleb128(o)
        prev+=diff; methods.append((prev,access,code_off,False))
    return fields, methods

print('===',label,'===')
fields, methods = parse_class_data(class_off)
for fidx in fields:
    cls,name,ftype = get_field(fidx)
    print(f'  field: {name} : {ftype}')
for midx,access,code_off,direct in methods:
    cls,name,proto = get_method(midx)
    print(f'  method: {name} {proto} code_off={hex(code_off)} direct={direct}')
