"""Synthetic self-test: forward-encode a fake template message with a random
corpus via public transport_cases.run, then recover with wln_coupled.solve."""
import sys, os, random, collections; sys.argv=['x']; sys.path.insert(0,'.')
import wln_coupled as w
c=collections.Counter(); errs=collections.Counter()
for s,n,t,r,a in w.candidates(None):
    try:
        L=w.layouts(s,n,t,r,a); c['ok' if L else 'none']+=1
    except Exception as e: errs[repr(e)[:70]]+=1
print(c, errs.most_common(3))
random.seed(1)
msg=w.PREFIX+bytes(random.choice(b'0123456789abcdef') for _ in range(32))+w.TEMPLATE[w.HEXHI:]
tests=[(('X','C'),1,3,0,3),(('X','I','C'),1,5,0,5),(('X','C','I'),1,7,0,3)]
for s,n,t,r,a in tests:
    p={'initial_lanes':n,'thread_count':t,'lane_rotation':r,'inter_arity':a,'corpus_hex':os.urandom(256).hex(),'corpus_bit_offset':random.randrange(8192)}
    if (s,n) not in [(tuple(x),y) for x,y in w.matrix.transport_schedules()[0]]: print('not accepted',s); continue
    wire=w.tc.run(msg,list(s),p)
    st=w.tc.decode_lanes(wire); wl=[list(l) for l in st.lanes]
    u,v,final=w.layouts(s,n,t,r,a)
    sols,steps=w.solve(wl,u,v,maxsol=3)
    print(s,t,[x==msg for x in sols],steps)
