from parse import parse
import itertools
def inv(C,mode,init=0):
    P=[];prev=init;cprev=init
    for c in C:
        if mode=='xorP': p=c^prev
        elif mode=='subP': p=(c-prev)&255
        elif mode=='addP': p=(c+prev)&255
        elif mode=='xorC': p=c^cprev
        elif mode=='subC': p=(c-cprev)&255
        elif mode=='id': p=c
        elif mode=='not': p=c^0xff
        elif mode=='rev': p=int('{:08b}'.format(c)[::-1],2)
        P.append(p);prev=p;cprev=c
    return bytes(P)
def pr(b): return sum(32<=x<127 or x in (9,10,13) for x in b)/max(1,len(b))
for k in ['a02','a03','a04','b01','b02','b04']:
    d,j,h,hdr,recs,i=parse(k)
    lit=[r[6] for r in recs if r[4]%8==0][:200]
    for mode in ['id','xorP','subP','addP','xorC','subC','rev']:
        for scope in ('chunk','stream'):
            if scope=='chunk': out=b''.join(inv(c,mode) for c in lit)
            else: out=inv(b''.join(lit),mode)
            s=pr(out)
            if s>0.6 or mode=='id': print(k,mode,scope,round(s,3),out[:60])
