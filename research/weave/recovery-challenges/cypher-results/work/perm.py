import glob,lzma,zlib,itertools
import numpy as np
def body(d):
    i=101
    while d[i]&0x80:i+=1
    return d[i+1:]
def fl_fwd(n):  # out[k] = in[p[k]]: first,last,second,second-last
    p=[];i,j=0,n-1
    while i<=j:
        p.append(i); 
        if i!=j: p.append(j)
        i+=1;j-=1
    return np.array(p)
def riffle_fwd(n):
    h=(n+1)//2
    p=[]
    for k in range(h):
        p.append(k)
        if h+k<n:p.append(h+k)
    return np.array(p)
def inv(p):
    q=np.empty_like(p);q[p]=np.arange(len(p));return q
def units(b,w):
    bits=np.unpackbits(np.frombuffer(b,dtype=np.uint8))
    n=len(bits)//w*w
    return bits[:n].reshape(-1,w)
def pack(u):
    bits=u.reshape(-1)
    return np.packbits(bits).tobytes()
def score(x): return len(zlib.compress(x,9))
for f in sorted(glob.glob('../v1/ciphertexts/*.wvc')):
    b=body(open(f,'rb').read())
    base=score(b)
    res=[]
    for w in [1,2,4,8,16]:
        u=units(b,w); n=len(u)
        for name,P in [('fl',fl_fwd(n)),('rf',riffle_fwd(n))]:
            for direction in ['undo','do']:
                q=inv(P) if direction=='undo' else P
                x=u
                for r in range(1,4):
                    x=x[q]
                    res.append((score(pack(x))/base,w,name,direction,r))
    res.sort()
    print(f[-7:],base,[ (round(s,3),w,nm,d,r) for s,w,nm,d,r in res[:5]])
