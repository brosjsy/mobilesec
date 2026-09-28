import base64
from Crypto.Cipher import AES

pkg = "com.mobisec.dexclassloader"
parts = pkg.split(".")
key = (parts[1] + parts[0] + "key!!!").encode("utf-8")
iv = bytes([0xDE,0xAD,0xBE,0xEF]*4)
print("key", key, len(key))

def ds(enc_b64):
    raw = base64.b64decode(enc_b64)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(raw)
    padlen = pt[-1]
    pt = pt[:-padlen]
    return pt.decode()

vals = {
 "gu (url)": "MAi9CEe4K9a+JzgsNqdYYh13dk7SQQ/yo5BN5HF39nYtgnOBmO4EV9Y2sQDthTG9",
 "gf (filename)": "QLrdlqkhOkxIe5FEfpCLWw==",
 "gc (classname)": "ca9O9YbCZ/+vIYUvxPQUHA4SgyL/m3cwlvVZ4ArkBFQ=",
 "gm (methodname)": "6RSjLOfRkvb/qXa34Y7cOQ==",
}
for k,v in vals.items():
    print(k, "=>", ds(v))
