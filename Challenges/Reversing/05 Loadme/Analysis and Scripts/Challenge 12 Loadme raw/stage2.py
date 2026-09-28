import base64, zipfile
from Crypto.Cipher import AES

pkg = "com.mobisec.dexclassloader"
p = pkg.split(".")
key = ("!!!" + p[0] + p[1] + "key").encode()
iv = bytes([0xDE,0xAD,0xBE,0xEF]*4)
print("key", key, len(key))

def ds(b64):
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(base64.b64decode(b64))
    return pt[:-pt[-1]].decode()

vals = {
 "assets name": "VYsdn556h+cox7bnQV4UsA==",
 "code name":   "SXkAHK1O8Ssd6aCiqtpiAg==",
 "method":      "zkKQzoRGUwBJurGdAYVuMw==",
 "class":       "4hJIFOEdvGy81kngg5W2mh4ZMYOQVmqX+FqCg8UmFmc=",
}
res = {k: ds(v) for k, v in vals.items()}
print(res)

z = zipfile.ZipFile("stage1_dec.apk")
print([n for n in z.namelist() if n.startswith("assets/")])
data = z.read("assets/" + res["assets name"])
xk = b"weneedtogodeeper"
out = bytes(b ^ xk[i % len(xk)] for i, b in enumerate(data))
print(len(out), out[:4])
open("stage2.apk", "wb").write(out)
