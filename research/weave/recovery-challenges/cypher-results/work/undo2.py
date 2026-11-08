import numpy as np,glob
from undo import body,undo_fl
pat=np.unpackbits(np.frombuffer(b'WAF\x01',dtype=np.uint8))
def find(S,pat):
    SS=np.concatenate([S,S[:len(pat)]])
    n=len(S);m=len(pat)
    ok=np.ones(n,bool)
    for t in range(m): ok&=(SS[t:t+n]==pat[t])
    return np.nonzero(ok)[0]
res={}
for f in sorted(glob.glob('../v1/ciphertexts/*.wvc')):
    k=f[-7:-4]
    bits=np.unpackbits(np.frombuffer(body(open(f,'rb').read()),dtype=np.uint8))
    n=len(bits)
    for pad in range(8):
        for first in (True,False):
            for lead in ('end','start'):
                x=bits[:n-pad] if lead=='end' else bits[pad:]
                S=undo_fl(x,first)
                for p in find(S,pat):
                    R=np.roll(S,-p)
                    B=np.packbits(R).tobytes()
                    print(k,'pad',pad,lead,'first' if first else 'last','rot',p,'L',len(S),B[:24])
