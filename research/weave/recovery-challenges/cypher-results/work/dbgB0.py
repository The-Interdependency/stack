import sys
sys.path.insert(0,'/workspace/cypher/src')
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
import json,cycle,numeral
from cycle import CycleLimits
from cycle_native import load_native
from prime_schedule import plan,interleave,Route
from numeral import PrimePath,_Reader,decode as decode_numeral

SOURCES='/workspace/cypher/src/sources'
LIM=CycleLimits(); api,geometry=load_native(SOURCES)
pub=json.loads(Path('/workspace/cypher/src/profiles/cycle-v1.json').read_text())
engine=numeral._Primes(LIM.numeral())
specs=[]; routes=[]
for rd in pub['rounds']:
    pp=PrimePath(rd['prime_path']['seed'],tuple(tuple(s) for s in rd['prime_path']['steps']))
    specs.append((pp,tuple(rd['arities']),rd['end_order']))
    routes.append(Route.evaluate(pp,LIM.numeral(),engine=engine))

wire=Path('/workspace/cypher/v1/ciphertexts/b01.wvc').read_bytes()
r=_Reader(wire); r.take(4); r.take(32); r.take(32); root=r.take(32).hex(); rc=r.uint(); data=r.blob(LIM.round_bytes)
# undo rounds 2 then 1 using known spaces from previous run (we'll re-solve quickly via caching)
# Actually re-run solve for 2 and 1 then inspect round 0 packed
from recoverB import solve_round,parse_waf
for i in (2,1):
    pp,arities,end=specs[i]
    split=plan(len(data)*8,routes[i],arities,LIM.numeral(),engine=engine)
    packed=interleave(data,split,inverse=True,end_order=end)
    data,src_len,spaces=solve_round(packed)
    print('undid round',i,'->',src_len)
# now round 0
pp,arities,end=specs[0]
split=plan(len(data)*8,routes[0],arities,LIM.numeral(),engine=engine)
packed=interleave(data,split,inverse=True,end_order=end)
print('round0 packed',len(packed),packed[:4])
src_len,packet,counts,positions=parse_waf(packed)
print('src_len',src_len,'defs',len(packet.entries),'occ',len(packet.symbols),'counts',counts,'origin',packet.origin,'round',packet.round_id)
print('circles of defs', [e.circle for e in packet.entries[:20]],'...')
# check space candidates per circle
by_sym={e.symbol:i for i,e in enumerate(packet.entries)}
length_of=[e.block.length//8 for e in packet.entries]
percirc=defaultdict(list); cur=0
wire_idx=[by_sym[s] for s in packet.symbols]
for c in range(1,8):
    for _ in range(counts[c-1]):
        percirc[c].append((wire_idx[cur],positions[cur])); cur+=1
DEN=65536
def cand():
    seen=set()
    for num in range(0,2*DEN):
        s=Fraction(num,DEN); k=(s.numerator,s.denominator)
        if k in seen: continue
        seen.add(k); yield s
for c,lst in percirc.items():
    n_ok=0; samples=[]
    for s in cand():
        offs=[]; ok=True
        for di,p in lst:
            try: ax=geometry.recover_axis(packet.origin,src_len,p,s)
            except Exception: ok=False; break
            offs.append((ax.axis_ordinal,di))
        if ok and len({o for o,_ in offs})==len(offs) and all(0<=o<src_len for o,_ in offs):
            n_ok+=1
            if n_ok<=3: samples.append((str(s),sorted(offs)[:5],len(offs)))
    print('circle',c,'n_occ',len(lst),'n_ok_spaces',n_ok,'samples',samples)
