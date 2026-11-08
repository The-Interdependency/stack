import sys
import numpy as np
def body(d):
    i=101
    while d[i]&0x80:i+=1
    return d[i+1:]
k=sys.argv[1]; P=int(sys.argv[2])
b=np.frombuffer(body(open(f'../v1/ciphertexts/{k}.wvc','rb').read()),dtype=np.uint8)
eq=(b[P:]==b[:-P]).astype(float)
W=P*10
sm=np.convolve(eq,np.ones(W)/W,mode='valid')
# report segments with sm>0.5
inside=False
for i,v in enumerate(sm):
    if v>0.45 and not inside: st=i;inside=True
    if v<=0.45 and inside:
        if i-st>P*20: print('seg',st,i+W+P,'len',i+W+P-st, 'mean',round(float(sm[st:i].mean()),2))
        inside=False
if inside: print('seg',st,len(b),'len',len(b)-st)
print('total',len(b))
