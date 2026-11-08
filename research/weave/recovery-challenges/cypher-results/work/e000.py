import numpy as np,sys
from best import findall,pat
from parse import varint
P=pat(b'\x03\xee\x80\x80')
for k in sys.argv[1:]:
    S=np.unpackbits(np.frombuffer(open(f'{k}.S','rb').read(),dtype=np.uint8))
    for name,X in (('fwd',S),('rev',S[::-1].copy())):
        for p in findall(X,P):
            B=np.packbits(X[p:p+8*40]).tobytes()
            i=4; num,i=varint(B,i); den,i=varint(B,i); c=B[i]
            print(k,name,'bit',p,'num/den',num,den,round(num/den,5),'circle',c,B[i+1:i+6].hex())
