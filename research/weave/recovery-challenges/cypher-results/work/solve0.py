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
from recoverB import solve_round,parse_waf

SOURCES='/workspace/cypher/src/sources'
LIM=CycleLimits(); api,geometry=load_native(SOURCES)
pub=json.loads(Path('/workspace/cypher/src/profiles/cycle-v1.json').read_text())
engine=numeral._Primes(LIM.numeral())
specs=[]; routes=[]
for rd in pub['rounds']:
    pp=PrimePath(rd['prime_path']['seed'],tuple(tuple(s) for s in rd['prime_path']['steps']))
    specs.append((pp,tuple(rd['arities']),rd['end_order']))
    routes.append(Route.evaluate(pp,LIM.numeral(),engine=engine))

def undo_to_round0(k):
    wire=Path(f'/workspace/cypher/v1/ciphertexts/{k}.wvc').read_bytes()
    r=_Reader(wire); r.take(4); r.take(32); r.take(32); root=r.take(32).hex(); rc=r.uint(); data=r.blob(LIM.round_bytes)
    for i in (2,1):
        pp,arities,end=specs[i]
        split=plan(len(data)*8,routes[i],arities,LIM.numeral(),engine=engine)
        packed=interleave(data,split,inverse=True,end_order=end)
        data,_,_=solve_round(packed)
    pp,arities,end=specs[0]
    split=plan(len(data)*8,routes[0],arities,LIM.numeral(),engine=engine)
    packed=interleave(data,split,inverse=True,end_order=end)
    return packed,root

def candidates_for(packed):
    src_len,packet,counts,positions=parse_waf(packed)
    by_sym={e.symbol:i for i,e in enumerate(packet.entries)}
    length_of=[e.block.length//8 for e in packet.entries]
    wire_idx=[by_sym[s] for s in packet.symbols]
    percirc=defaultdict(list); cur=0
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
    out={}
    for c,lst in percirc.items():
        opts=[]
        for s in cand():
            offs=[]; ok=True
            for di,p in lst:
                try: ax=geometry.recover_axis(packet.origin,src_len,p,s)
                except Exception: ok=False; break
                offs.append((ax.axis_ordinal,di,length_of[di]))
            if ok and len({o for o,_,_ in offs})==len(offs) and all(0<=o<src_len for o,_,_ in offs):
                opts.append((s,tuple(sorted(offs))))
        out[c]=opts
    return src_len,packet,out

def exact_cover(src_len, opts_by_c):
    # recursive place circles in order of fewest options
    circles=sorted(opts_by_c, key=lambda c: len(opts_by_c[c]))
    occ=[None]*src_len  # di or None
    choice={}
    def place(ci):
        if ci==len(circles):
            return True
        c=circles[ci]
        for s,offs in opts_by_c[c]:
            # check fit
            ok=True
            written=[]
            for o,di,L in offs:
                if o+L>src_len: ok=False;break
                for x in range(o,o+L):
                    if occ[x] is not None: ok=False;break
                if not ok: break
                for x in range(o,o+L): occ[x]=di
                written.append((o,L))
            if ok:
                choice[c]=s
                if place(ci+1): return True
            for o,L in written:
                for x in range(o,o+L): occ[x]=None
        return False
    if not place(0): raise RuntimeError('no cover')
    # rebuild
    order=[]; i=0
    while i<src_len:
        di=occ[i]; order.append(di)
        # find length
        L=1
        while i+L<src_len and occ[i+L]==di and (i+L==0 or True):
            # need exact block length - look up from first occurrence of di
            break
        # get L from opts
        L=None
        for s,offs in opts_by_c[list(opts_by_c)[0]]: pass
        # better: from any circle's offs that contain this di at i
        for c,opts in opts_by_c.items():
            for s,offs in opts:
                for o,di2,LL in offs:
                    if o==i and di2==di: L=LL; break
                if L is not None: break
            if L is not None: break
        i+=L
    return choice,order,occ

# test on b01
packed,root=undo_to_round0('b01')
src_len,packet,opts=candidates_for(packed)
print('opts sizes',[ (c,len(opts[c])) for c in range(1,8)])
choice,order,occ=exact_cover(src_len,opts)
print('spaces',[str(choice[c]) for c in range(1,8)])
# also need spaces[0]; try using recover_sequences which needs all 8
# spaces[0] is for whole-circle attachment only; SequenceTable.restore doesn't need it for bytes
ents=packet.entries
restored=b''.join(ents[di].block.to_bytes() for di in order)
print('restored',len(restored),restored[:4], 'NORMAL?',restored[:4]==b'WNM\x01')
if restored[:4]==b'WNM\x01':
    length=int.from_bytes(restored[4:12],'big')
    msg=restored[44:44+length]
    print('MSG',length,msg[:200])
