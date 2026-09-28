import hashlib
import math

LOTTO_PATH = r"C:\Users\Admin\Desktop\MOBISEC_Challenge\Challenges\Challenge_16_UPOS\Analysis_and_Scripts\Challenge_16_UPOS\assets\lotto.dat"

# ---- load 256x256 matrix ----
with open(LOTTO_PATH) as f:
    rows = f.read().strip().split('\n')
assert len(rows) == 256, len(rows)
m = []
for row in rows:
    vals = [int(x) for x in row.split(' ')]
    assert len(vals) == 256, len(vals)
    m.append(vals)

# ---- Streamer (LFSR), exact port of Streamer.java ----
class Streamer:
    def __init__(self, seed="01101000010", tap=8):
        self.lfsr = [c == '1' for c in seed]
        self.tap = (len(seed) - 1) - tap

    def step(self):
        new_bit = self.lfsr[self.tap] ^ self.lfsr[0]
        self.lfsr = self.lfsr[1:] + [new_bit]
        return 1 if new_bit else 0

    def g2(self):
        val = 0
        for i in range(16):
            val |= self.step() << i
        return val

def is_prime_ip(x):
    # exact port of FC.ip(int x): for i in 2..x-1: if x%i==0: return False; return True
    for i in range(2, x):
        if x % i == 0:
            return False
    return True

def inverse_r(c):
    # r() forward is Caesar shift +7 mod 26 on a-z and A-Z; inverse is shift -7 (== +19)
    if 'a' <= c <= 'z':
        return chr((ord(c) - ord('a') - 7) % 26 + ord('a'))
    if 'A' <= c <= 'Z':
        return chr((ord(c) - ord('A') - 7) % 26 + ord('A'))
    return c

s = Streamer()

# 12 "decoy" s.step() calls happen earlier in checkFlag() before the main
# loop is reached, on the normal (non-throwing) execution path:
#   lines 66,70,71,84,107,113,117,129,135,136 (=10), then inside the
#   IllformedLocaleException catch: lines 281,289 (=2 more) = 12 total.
# (Lines 139-143, five more step() calls, are DEAD CODE - unreachable,
# since the throw at line 136-137 always fires before reaching them.)
for _ in range(12):
    s.step()

core_chars = [None] * 60

for i in range(30):
    if is_prime_ip(i):
        for _ in range(i):
            s.step()
    j2 = s.g2()
    mX = j2 & 0xFF
    j3 = s.g2()
    mY = (j3 & 0xFF00) >> 8
    target = m[mX][mY]
    n = math.isqrt(target)
    if n * n != target:
        print(f"WARNING: i={i} mX={mX} mY={mY} target={target} not a perfect square! n={n}")
    byte0 = n & 0xFF
    byte1 = (n >> 8) & 0xFF
    tc0 = chr(byte0)
    tc1 = chr(byte1)
    c0 = inverse_r(tc0)
    c1 = inverse_r(tc1)
    core_chars[i*2] = c0
    core_chars[i*2 + 1] = c1
    print(f"i={i:2d} mX={mX:3d} mY={mY:3d} n={n:6d} bytes=({byte0},{byte1}) -> '{c0}{c1}'")

core = ''.join(core_chars) + '}'
flag = "MOBISEC{" + core

print()
print("Recovered core (61 chars):", repr(core))
print("Full flag:", flag)
print("Flag length:", len(flag), "(expect 69)")
print()

# sanity checks matching the decoy string constraints (should hold automatically)
print("starts with MOBISEC{:", flag.startswith("MOBISEC{"))
print("core ends with }:", core.endswith("}"))
print("core starts with this_is_:", core.startswith("this_is_"))
print("core contains really_:", "really_" in core)
print("core[9:13] endswith bam:", core[9:13].endswith("bam"))
print("core.substring(22) upper startswith MAYB:", core[22:].upper().startswith("MAYB"))

h = hashlib.sha256(flag.encode()).hexdigest()
print()
print("SHA256(flag):", h)
print("expected:    4193d9b72a5c4805e9a5cc739f8a8fc23b2890e13b83bb887d96f86c30654a12")
print("MATCH:", h == "4193d9b72a5c4805e9a5cc739f8a8fc23b2890e13b83bb887d96f86c30654a12")
