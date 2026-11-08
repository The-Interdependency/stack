import numpy as np,itertools,glob
from undo import body
def flp(L,first=True):
    k=np.arange(L); p=np.empty(L,np.int64)
    if first:
        p[0::2]=np.arange((L+1)//2); p[1::2]=L-1-np.arange(L//2)
    else:
        p[0::2]=L-1-np.arange((L+1)//2); p[1::2]=np.arange(L//2)
    return p  # out[k]=in[p[k]]
def undo_rounds(x,orders):
    for f in reversed(orders):
        p=flp(len(x),f); S=np.empty_like(x); S[p]=x; x=S
    return x
def wire(k):
    return np.unpackbits(np.frombuffer(body(open(f'../v1/ciphertexts/{k}.wvc','rb').read()),dtype=np.uint8))
def rec_count(B): return B.count(b'\x03\xee\x80')+B.count(b'\x03\xee\x81')
if __name__=='__main__':
  for k in ['a01','a02','a03','a04','b01','b02','b03','b04']:
    bits=wire(k); n=len(bits); res=[]
    for pad in range(8):
      for lead in ('end','start'):
        x=bits[:n-pad] if lead=='end' else bits[pad:]
        for R in (1,2,3):
          for orders in itertools.product((True,False),repeat=R):
            S=undo_rounds(x,orders); B=np.packbits(S).tobytes()
            res.append((B[:4]==b'WAF\x01', B.find(b'WNC\x01@')>=0 and B.find(b'WNC\x01@')<20, rec_count(B), pad,lead,orders))
    res.sort(key=lambda r:(r[0],r[1],r[2]),reverse=True)
    print(k,res[:4])
