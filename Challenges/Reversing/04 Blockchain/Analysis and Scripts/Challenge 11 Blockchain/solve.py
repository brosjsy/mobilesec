import hashlib
from Crypto.Cipher import AES

target_hex = "0eef68c5ef95b67428c178f045e6fc8389b36a67bbbd800148f7c285f938a24e696ee2925e12ecf7c11f35a345a2a142639fe87ab2dd7530b29db87ca71ffda2af558131d7da615b6966fb0360d5823b79c26608772580bf14558e6b7500183ed7dfd41dbb5686ea92111667fd1eff9cec8dc29f0cfe01e092607da9f7c2602f5463a361ce5c83922cb6c3f5b872dcc088eb85df80503c92232bf03feed304d669ddd5ed1992a26674ecf2513ab25c20f95a5db49fdf6167fda3465a74e0418b2ea99eb2673d4c7e1ff7c4921c4e2d7b"
ct = bytes.fromhex(target_hex)

def md5(b): return hashlib.md5(b).digest()

KEY = "anykey123"
d = md5(KEY.encode())
currKey = md5(bytes([d[0], d[len(d)//2], d[-1]]))

keys = []
k = currKey
for i in range(10):
    keys.append(k)
    k = md5(k)

data = ct
for i in reversed(range(10)):
    pt = AES.new(keys[i], AES.MODE_ECB).decrypt(data)
    padlen = pt[-1]
    if not (1 <= padlen <= 16) or pt[-padlen:] != bytes([padlen]) * padlen:
        print("bad padding at round", i, padlen)
        break
    data = pt[:-padlen]

print("recovered flag bytes:", data)
try:
    print("as text:", data.decode())
except Exception as e:
    print("decode error:", e)

# sanity check: re-run the app's forward algorithm
currPt = data
ck = currKey
for i in range(10):
    padlen = 16 - (len(currPt) % 16)
    currPt = AES.new(ck, AES.MODE_ECB).encrypt(currPt + bytes([padlen]) * padlen)
    ck = md5(ck)
print("forward check matches target:", currPt.hex() == target_hex)
print("KEY used:", KEY)
