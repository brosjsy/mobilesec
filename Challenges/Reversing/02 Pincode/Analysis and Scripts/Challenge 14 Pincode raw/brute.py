import hashlib
import multiprocessing as mp

TARGET = "d04988522ddfed3133cc24fb6924eae9"

def check(pin):
    b = pin.encode()
    for _ in range(25):
        for _ in range(400):
            md = hashlib.md5()
            md.update(b)
            b = md.digest()
    return b.hex() == TARGET

def worker(rng):
    lo, hi = rng
    for i in range(lo, hi):
        pin = "%06d" % i
        if check(pin):
            return pin
    return None

def main():
    n = mp.cpu_count()
    chunk = 1000000 // n + 1
    ranges = [(i, min(i + chunk, 1000000)) for i in range(0, 1000000, chunk)]
    with mp.Pool(n) as p:
        for res in p.imap_unordered(worker, ranges):
            if res:
                print("FOUND:", res)
                p.terminate()
                return
    print("not found")

if __name__ == "__main__":
    main()
