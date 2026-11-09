"""Synthetic self-test with random corpora (public forward code); not challenge data."""
import sys, os, random; sys.argv=['x']; sys.path.insert(0,'.')
import wln_multiC as M, wln_coupled as W
random.seed(7)
msg=W.PREFIX+bytes(random.choice(b'0123456789abcdef') for _ in range(32))+W.TEMPLATE[W.HEXHI:]
for s,t in [(('X','C'),3),(('X','C','C'),3),(('C','X','C'),5),(('X','C','C','C'),7),(('C','X'),3)]:
    p={'initial_lanes':1,'thread_count':t,'lane_rotation':0,'inter_arity':3,'corpus_hex':os.urandom(256).hex(),'corpus_bit_offset':random.randrange(8192)}
    wire=W.tc.run(msg,list(s),p); st=W.tc.decode_lanes(wire); wl=[list(l) for l in st.lanes]
    stages,fl,final=M.build(s,1,t,0,3)
    sols,steps,exh=M.solve(wl,stages,fl,maxsol=2,budget=3_000_000)
    print(s,t,'nsol',len(sols),'match',[x==msg for x in sols],'steps',steps,'exhausted',exh,flush=True)
