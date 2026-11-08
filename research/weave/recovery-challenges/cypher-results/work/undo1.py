import glob
import numpy as np
def body(d):
    i=101
    while d[i]&0x80:i+=1
    return d[i+1:]
for f in sorted(glob.glob('../v1/ciphertexts/*.wvc')):
    k=f[-7:-4]
    bits=np.unpackbits(np.frombuffer(body(open(f,'rb').read()),dtype=np.uint8))
    S=np.concatenate([bits[0::2],bits[1::2][::-1]])
    open(f'{k}.s1','wb').write(np.packbits(S).tobytes())
    W=len(S)//60
    print(k,' '.join(str(int(S[i:i+W].mean()*100)) for i in range(0,len(S)-W+1,W)))
