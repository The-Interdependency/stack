import sys
sys.path.insert(0,'/workspace/cypher/src')
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
import json,cycle,numeral
from cycle import CycleLimits,NORMAL_MAGIC
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
    circles=sorted(opts_by_c, key=lambda c: len(opts_by_c[c]))
    occ=[None]*src_len
    lens=[None]*src_len
    choice={}
    def place(ci):
        if ci==len(circles): return True
        c=circles[ci]
        for s,offs in opts_by_c[c]:
            ok=True; written=[]
            for o,di,L in offs:
                if o+L>src_len: ok=False; break
                for x in range(o,o+L):
                    if occ[x] is not None: ok=False; break
                if not ok: break
                for x in range(o,o+L): occ[x]=di; lens[x]=L if x==o else -1
                written.append((o,L))
            if ok:
                choice[c]=s
                if place(ci+1): return True
            for o,L in written:
                for x in range(o,o+L): occ[x]=None; lens[x]=None
        return False
    if not place(0): raise RuntimeError('no cover')
    order=[]; i=0
    while i<src_len:
        di=occ[i]; L=lens[i]; order.append(di); i+=L
    return choice,order

def recover(k):
    wire=Path(f'/workspace/cypher/v1/ciphertexts/{k}.wvc').read_bytes()
    r=_Reader(wire); r.take(4); r.take(32); r.take(32); root=r.take(32).hex(); rc=r.uint(); data=r.blob(LIM.round_bytes)
    spaces_all=[]
    for i in range(rc-1,-1,-1):
        pp,arities,end=specs[i]
        split=plan(len(data)*8,routes[i],arities,LIM.numeral(),engine=engine)
        packed=interleave(data,split,inverse=True,end_order=end)
        if i>0:
            data,src_len,spaces=solve_round(packed)
            spaces_all.append((i,spaces))
            print(f'  round {i}: len={src_len}')
        else:
            src_len,packet,opts=candidates_for(packed)
            print(f'  round 0: src_len={src_len} opt_sizes={[len(opts[c]) for c in range(1,8)]}')
            choice,order=exact_cover(src_len,opts)
            data=b''.join(packet.entries[di].block.to_bytes() for di in order)
            spaces_all.append((0,[choice[c] for c in range(1,8)]))
            print(f'  round 0 spaces: {[str(choice[c]) for c in range(1,8)]}')
    assert data[:4]==NORMAL_MAGIC
    length=int.from_bytes(data[4:12],'big'); ch=data[12:44].hex(); msg=data[44:44+length]
    # verify root
    rec=api.ByteOrigin(data,pub['scope'],0,geometry).message_origin
    Path(f'/workspace/cypher/work/{k}.recovered').write_bytes(msg)
    print(f'=== {k}: {length} bytes corpus={ch} root_ok={rec==root}')
    print('   preview',msg[:220])
    return msg,spaces_all

for k in ['b01','b02','b03','b04']:
    try: recover(k)
    except Exception as e:
        import traceback; print(f'=== {k} FAILED',e); traceback.print_exc()
