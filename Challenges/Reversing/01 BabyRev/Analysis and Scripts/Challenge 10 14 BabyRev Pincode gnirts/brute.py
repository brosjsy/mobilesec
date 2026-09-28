import hashlib
import itertools
import multiprocessing as mp
import string
import sys

JOBS = [
    ("part0", string.ascii_lowercase, 5, "6e9a4d130a9b316e9201238844dd5124"),
    ("part1", string.digits, 7, "7c51a5e6ea3214af970a86df89793b19"),
    ("part2", string.ascii_uppercase, 5, "e5f20324ae520a11a86c7602e29ecbb8"),
    ("part3", string.ascii_letters + string.digits, 4, "1885eca5a40bc32d5e1bca61fcd308a5"),
    ("part4", string.digits, 7, "da5062d64347e5e020c5419cebd149a2"),
]

def worker(args):
    charset, length, target, start_idx, step, n = args
    target_bytes = bytes.fromhex(target)
    idx = start_idx
    for _ in range(idx, n, step):
        pass
    # generate all combos, only process every `step`-th starting at start_idx
    count = 0
    for combo in itertools.product(charset, repeat=length):
        if count % step == start_idx % step:
            s = "".join(combo)
            if hashlib.md5(s.encode()).digest() == target_bytes:
                return s
        count += 1
    return None

def brute(charset, length, target, nproc):
    target_bytes = bytes.fromhex(target)
    n = len(charset) ** length
    chunk_args = [(charset, length, target, i, nproc, n) for i in range(nproc)]
    with mp.Pool(nproc) as p:
        for res in p.imap_unordered(worker, chunk_args):
            if res:
                p.terminate()
                return res
    return None

if __name__ == "__main__":
    nproc = 4
    for name, charset, length, target in JOBS:
        print(f"solving {name} (len={length}, charset_size={len(charset)}, space={len(charset)**length})...", flush=True)
        res = brute(charset, length, target, nproc)
        print(name, "=>", res, flush=True)
