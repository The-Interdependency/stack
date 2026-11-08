import sys
import numpy as np
def body(d):
    i=101
    while d[i]&0x80:i+=1
    return d[i+1:]
k=sys.argv[1]; P=int(sys.argv[2]); st=int(sys.argv[3]); en=int(sys.argv[4])
cols=[list(map(int,c.split(','))) for c in sys.argv[5:]]
b=np.frombuffer(body(open(f'../v1/ciphertexts/{k}.wvc','rb').read()),dtype=np.uint8)
seg=b[st:en]
seg=seg[(len(seg))%P:] if en==len(b) else seg[:len(seg)//P*P]
bits=np.unpackbits(seg.reshape(-1,P),axis=1)
for cl in cols:
    v=[int(''.join(str(bits[r,j]) for j in cl),2) for r in range(len(bits))]
    print(cl); print(' vals',v[:80]); d=np.diff(v); print(' diffs',list(d[:80]))
