from parse import parse
from fractions import Fraction as F
def chunks(k):
    d,j,h,hdr,recs,i=parse(k)
    return [r for r in recs if r[4]==8*len(r[6]) and r[4]>=16][:150]
def pr(b): return sum(32<=x<127 or x==10 for x in b)/max(1,len(b))
def letters(b): return sum((97<=x<=122) or x==32 for x in b)/max(1,len(b))
def ops():
    for k in range(1,17):
        yield f'invxorshr{k}',lambda N,n,k=k: invx(N,n,k,'r')
        yield f'invxorshl{k}',lambda N,n,k=k: invx(N,n,k,'l')
    yield 'gray',lambda N,n: invx(N,n,1,'r',full=True)
    for r in range(1,8):
        yield f'rotl{r}',lambda N,n,r=r: ((N<<r)|(N>>(n-r)))&((1<<n)-1)
        yield f'rotr{r}',lambda N,n,r=r: ((N>>r)|(N<<(n-r)))&((1<<n)-1)
def invx(N,n,k,d,full=False):
    # solve P where N = P ^ (P>>k)  (d='r') or P ^ (P<<k)
    m=(1<<n)-1; P=N
    for _ in range(n//k+1):
        P = N ^ ((P>>k) if d=='r' else ((P<<k)&m))
    return P
import collections
res=collections.defaultdict(list)
for k in ['a02','a03','a04','b01','b02','b04']:
    cs=chunks(k)
    for endian in ('big','little'):
        for name,f in ops():
            out=b''
            for r in cs:
                b=r[6]; n=8*len(b); N=int.from_bytes(b,endian)
                out+=f(N,n).to_bytes(len(b),endian)
            res[(endian,name)].append((k,round(letters(out),2),out[:40]))
base=[ (endian,name) for (endian,name) in res]
ranked=sorted(res.items(),key=lambda kv:-sum(x[1] for x in kv[1]))
for key,v in ranked[:6]:
    print(key,[(a,b) for a,b,c in v]); print('   ',v[0][2],v[2][2])
ident=[(a,round(letters(b''.join(r[6] for r in chunks(a))),2)) for a in ['a02','a03','a04','b01','b02','b04']]
print('identity letters',ident)
