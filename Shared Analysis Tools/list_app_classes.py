import struct, sys

def list_classes(dex_path, filter_str):
    dex = open(dex_path,'rb').read()
    def u4(o): return struct.unpack_from('<I', dex, o)[0]
    string_ids_off = u4(0x3C)
    type_ids_off = u4(0x44)
    class_defs_size = u4(0x60)
    class_defs_off = u4(0x64)
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
    out=[]
    for i in range(class_defs_size):
        o = class_defs_off + i*32
        class_idx = u4(o)
        class_data_off = u4(o+24)
        cname = get_type_string(class_idx)
        if filter_str in cname.lower():
            out.append((cname, class_data_off))
    return out

if __name__ == '__main__':
    path = sys.argv[1]
    filt = sys.argv[2] if len(sys.argv)>2 else 'mobisec'
    for cname, off in list_classes(path, filt):
        print(cname, hex(off))
