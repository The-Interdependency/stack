import numpy as np,itertools,glob
from undo import body,fl_perm
def fwd_perm(L,orders):
    # out = x[p]; compose rounds
    idx=np.arange(L)
    for f in orders:
        idx=idx[fl_perm(L,f)]
    return idx
def score(B):
    s=0
    if B[:4]==b'WAF\x01': s+=2
    if b'WNC\x01@' in B[:16]: s+=1
    return s
if __name__=='__main__':
  for f in sorted(glob.glob('../v1/ciphertexts/*.wvc')):
    k=f[-7:-4]
    bits=np.unpackbits(np.frombuffer(body(open(f,'rb').read()),dtype=np.uint8))
    n=len(bits); out=[]
    for pad in range(8):
        L=n-pad
        for R in (1,2,3):
            for orders in itertools.product((True,False),repeat=R):
                p=fwd_perm(L,orders)
                for lead in ('end','start'):
                    x=bits[:L] if lead=='end' else bits[pad:]
                    S=np.empty(L,np.uint8);S[p]=x
                    B=np.packbits(S).tobytes()
                    sc=score(B)
                    if sc==3: out.append((pad,R,orders,lead))
    print(k,n,out[:6])
