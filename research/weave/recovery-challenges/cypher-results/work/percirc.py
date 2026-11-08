from parse import parse
import collections,sys
EN=b' etaoinshrdlucmfwypvbgkjqxzETAOINSHRDLUCMFWYPVBGKJQXZ.,"\n:{}[]0123456789-\''
W={c:(len(EN)-i) for i,c in enumerate(EN)}
def sc(b): return sum(W.get(x,-20) for x in b)/max(1,len(b))
for k in sys.argv[1:]:
    d,j,h,hdr,recs,i=parse(k)
    byc=collections.defaultdict(bytes)
    for r in recs:
        if r[4]%8==0: byc[r[3]]+=r[6]
    res={}
    for c,b in sorted(byc.items()):
        best=max(range(256),key=lambda kk: sc(bytes(x^kk for x in b)))
        res[c]=best
        print(k,'circle',c,'n',len(b),'bestXOR %02x'%best,round(sc(bytes(x^best for x in b)),1),bytes(x^best for x in b)[:50])
