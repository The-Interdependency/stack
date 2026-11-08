import numpy as np
from fast import flp,wire
def pat(b,nbits=None):
    p=np.unpackbits(np.frombuffer(b,dtype=np.uint8)); return p[:nbits] if nbits else p
def findall(S,p):
    n=len(S)-len(p); ok=np.ones(n,bool)
    for t in range(len(p)): ok&=(S[t:t+n]==p[t])
    return np.nonzero(ok)[0]
REC=pat(b'\x03\xee\x80',20); WAF=pat(b'WAF\x01'); WNC=pat(b'WNC\x01@')
def cands(k):
    bits=wire(k); n=len(bits); out=[]
    for pad in range(8):
      for where in ('end','start'):
        x=bits[:n-pad] if where=='end' else bits[pad:]
        for first in (True,False):
            p=flp(len(x),first); S=np.empty_like(x); S[p]=x
            SS=np.concatenate([S,S[:40]])
            for r in findall(SS,WAF):
                if r>=len(S): continue
                R=np.roll(S,-r)
                out.append((len(findall(R,REC)),len(findall(R,WNC)),pad,where,first,int(r),len(S)))
    out.sort(reverse=True); return out
if __name__=='__main__':
    import sys
    for k in sys.argv[1:]:
        c=cands(k); print(k,c[:5])
