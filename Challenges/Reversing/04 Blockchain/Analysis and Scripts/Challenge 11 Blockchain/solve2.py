import hashlib
from Crypto.Cipher import AES

target_hex = "0eef68c5ef95b67428c178f045e6fc8389b36a67bbbd800148f7c285f938a24e696ee2925e12ecf7c11f35a345a2a142639fe87ab2dd7530b29db87ca71ffda2af558131d7da615b6966fb0360d5823b79c26608772580bf14558e6b7500183ed7dfd41dbb5686ea92111667fd1eff9cec8dc29f0cfe01e092607da9f7c2602f5463a361ce5c83922cb6c3f5b872dcc088eb85df80503c92232bf03feed304d669ddd5ed1992a26674ecf2513ab25c20f95a5db49fdf6167fda3465a74e0418b2ea99eb2673d4c7e1ff7c4921c4e2d7b"
ct = bytes.fromhex(target_hex)
nblocks = len(ct) // 16
print("ct length", len(ct), "blocks", nblocks)

def md5(b): return hashlib.md5(b).digest()

# key3 (3 bytes) -> currKey0 = md5(key3). Only 256^3 possibilities for currKey0.
# Build key schedule K0..K9 forward from currKey0, but we only need last block of ct
# decrypted through successive keys K9,K8,...
found = None
last_block = ct[-16:]

for b0 in range(256):
    for b1 in range(256):
        # batch over b2 using a single AES call trick isn't easy across keys, just loop
        for b2 in range(256):
            key3 = bytes((b0, b1, b2))
            k = md5(key3)  # K0
            # need K9 = md5^9(K0) chain to decrypt last block first (outermost stage uses K9)
            keys = [k]
            for _ in range(9):
                k = md5(k)
                keys.append(k)
            # keys[9] = K9 used for outermost decrypt
            dec = AES.new(keys[9], AES.MODE_ECB).decrypt(last_block)
            if dec != b"\x10" * 16:
                continue
            # survived stage 9 filter; continue peeling with full ct
            # decrypt ALL blocks with K9, drop last padding block
            full = AES.new(keys[9], AES.MODE_ECB).decrypt(ct)
            cur = full[:-16]
            ok = True
            for stage in range(8, -1, -1):
                kk = keys[stage]
                lastblk = cur[-16:]
                dd = AES.new(kk, AES.MODE_ECB).decrypt(lastblk)
                if stage == 0:
                    padlen = dd[-1]
                    if not (1 <= padlen <= 16) or dd[-padlen:] != bytes([padlen]) * padlen:
                        ok = False
                        break
                    # decrypt full cur with kk, strip generic pad
                    fulld = AES.new(kk, AES.MODE_ECB).decrypt(cur)
                    flag_bytes = fulld[:-padlen]
                    cur = flag_bytes
                else:
                    if dd != b"\x10" * 16:
                        ok = False
                        break
                    fulld = AES.new(kk, AES.MODE_ECB).decrypt(cur)
                    cur = fulld[:-16]
            if ok:
                found = (key3, cur)
                print("FOUND key3=", key3.hex(), "flag=", cur)
                break
        if found:
            break
    if found:
        break

if not found:
    print("no key3 found in 256^3 search")
else:
    print("key3:", found[0].hex())
    print("flag bytes:", found[1])
    try:
        print("flag text:", found[1].decode())
    except Exception as e:
        print("decode err", e)
