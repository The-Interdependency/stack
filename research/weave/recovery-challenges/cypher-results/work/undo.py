import numpy as np
def body(d):
    i=101
    while d[i]&0x80:i+=1
    return d[i+1:]
def fl_perm(L,first=True):
    # out index k -> source index
    p=[];i,j=0,L-1;t=first
    while i<=j:
        if t: p.append(i);i+=1
        else: p.append(j);j-=1
        t=not t
    return np.array(p)
def undo_fl(bits,first=True):
    L=len(bits);p=fl_perm(L,first)
    S=np.empty_like(bits);S[p]=bits;return S
if __name__=='__main__':
    import glob
    for f in sorted(glob.glob('../v1/ciphertexts/*.wvc')):
        k=f[-7:-4]
        bits=np.unpackbits(np.frombuffer(body(open(f,'rb').read()),dtype=np.uint8))
        n=len(bits)
        for pad in range(8):
            for lead in ('start','end'):
              for first in (True,False):
                x=bits[pad:] if lead=='start' else bits[:n-pad]
                S=undo_fl(x,first)
                B=np.packbits(S).tobytes()
                if B[:4]==b'WAF\x01':
                    print(k,'pad',pad,lead,'first' if first else 'last','L=',len(S),B[:12].hex(),'tailbits',''.join(map(str,S[-16:])))
                    open(f'{k}.S','wb').write(np.packbits(S).tobytes()); np.save(f'{k}.S.npy',S)
