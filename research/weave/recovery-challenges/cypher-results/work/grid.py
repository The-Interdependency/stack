import sys,itertools,zlib
import numpy as np
from perm import body,fl_fwd,riffle_fwd,inv
k=sys.argv[1]
b=body(open(f'../v1/ciphertexts/{k}.wvc','rb').read())
bits=np.unpackbits(np.frombuffer(b,dtype=np.uint8))
N=len(bits)
cache={}
def op(name,w):
    key=(name,w)
    if key not in cache:
        n=N//w
        P=fl_fwd(n) if name=='fl' else riffle_fwd(n)
        q=inv(P)
        idx=(np.repeat(q*w,w)+np.tile(np.arange(w),n))
        idx=np.concatenate([idx,np.arange(n*w,N)])
        cache[key]=idx
    return cache[key]
def sc(x): return len(zlib.compress(np.packbits(x).tobytes(),9))
base=sc(bits)
ops=[(n,w) for n in ('fl','rf') for w in (1,2,3,4,8,16)]
res=[]
for depth in (1,2,3):
    for seq in itertools.product(ops,repeat=depth):
        x=bits
        for o in seq: x=x[op(*o)]
        res.append((sc(x)/base,seq))
res.sort()
for r in res[:10]: print(round(r[0],3),r[1])
