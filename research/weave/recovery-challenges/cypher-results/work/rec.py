import sys
import numpy as np
def body(d):
    i=101
    while d[i]&0x80:i+=1
    return d[i+1:]
k=sys.argv[1]; P=int(sys.argv[2]); st=int(sys.argv[3]); en=int(sys.argv[4])
b=np.frombuffer(body(open(f'../v1/ciphertexts/{k}.wvc','rb').read()),dtype=np.uint8)
seg=b[st:en]
seg=seg[(len(seg))%P:] if en==len(b) else seg[:len(seg)//P*P]
R=seg.reshape(-1,P)
bits=np.unpackbits(R,axis=1)
var=[j for j in range(P*8) if 0<bits[:,j].mean()<1]
print(k,'records',len(R),'varying bit cols',len(var),var)
# for each varying col print its period of flipping
for j in var:
    col=bits[:,j]
    s=''.join(map(str,col[:120]))
    print('%4d %.2f %s'%(j,col.mean(),s))
