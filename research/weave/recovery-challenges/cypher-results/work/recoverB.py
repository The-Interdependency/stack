import sys,json
sys.path.insert(0,'/workspace/cypher/src')
from pathlib import Path
from fractions import Fraction
import cycle, numeral
from cycle import Profile, CycleLimits, _prepared, NORMAL_MAGIC
from cycle_native import load_native
from prime_schedule import plan, interleave
from numeral import _Reader, decode as decode_numeral

SOURCES='/workspace/cypher/src/sources'
LIM=CycleLimits()
api,geometry=load_native(SOURCES)

# public group-B profile basis: start from cycle-v1.json, keep public_unchanged fields.
# We need per-round: prime_path(public), arities(public), end_order(public). circle_order/spaces secret -> solved.
pub=json.loads(Path('/workspace/cypher/src/profiles/cycle-v1.json').read_text())

def parse_waf(packed):
    r=_Reader(packed)
    assert r.take(4)==cycle.AFFIX_MAGIC
    src_len=r.uint()
    packet=decode_numeral(r.blob(LIM.round_bytes),LIM.numeral())
    counts=tuple(r.uint() for _ in range(7))
    syms=packet.symbols
    positions=[]
    for _ in range(len(syms)):
        num,den=r.uint(),r.uint(); positions.append(Fraction(num,den))
    assert r.pos==len(packed)
    return src_len,packet,counts,positions

def solve_round(packed):
    src_len,packet,counts,positions=parse_waf(packed)
    ents=packet.entries
    by_sym={e.symbol:i for i,e in enumerate(ents)}
    circ_of=[e.circle for e in ents]         # circle per definition (from packet, not secret)
    length_of=[e.block.length//8 for e in ents]
    origin=packet.origin
    # wire order of occurrences: grouped by circle (counts), each pos in order
    wire_idx=[by_sym[s] for s in packet.symbols]
    # positions are in same wire order
    # brute-force space per circle
    # build per-circle list of (occurrence_pos_index, def_index, position)
    from collections import defaultdict
    percirc=defaultdict(list)
    cur=0
    for c in range(1,8):
        for _ in range(counts[c-1]):
            percirc[c].append((wire_idx[cur],positions[cur])); cur+=1
    DEN=65536
    def cand_spaces():
        seen=set()
        for num in range(0,2*DEN):
            s=Fraction(num,DEN)
            if (s.numerator,s.denominator) in seen: continue
            seen.add((s.numerator,s.denominator)); yield s
    offset_of={}  # def_index-occurrence -> offset ; we collect global list
    results={}
    for c,lst in percirc.items():
        good=None
        for s in cand_spaces():
            ok=True; offs=[]
            for di,p in lst:
                try:
                    ax=geometry.recover_axis(origin,src_len,p,s)
                except Exception:
                    ok=False;break
                offs.append((ax.axis_ordinal,di))
            if ok and len({o for o,_ in offs})==len(offs) and all(0<=o<src_len for o,_ in offs):
                if good is None: good=[(s,offs)]
                else: good.append((s,offs))
                if len(good)>6: break
        results[c]=good
    # combine: choose one space per circle so that all offsets tile [0,src_len)
    import itertools
    choices=[]
    for c in range(1,8):
        g=results[c] or [(None,[])]
        choices.append(g)
    for combo in itertools.product(*choices):
        allo=[]
        bad=False
        for (s,offs) in combo:
            allo+=offs
        offs_sorted=sorted(allo)
        off=0; order=[]; ok=True
        used=set()
        pos_set={o for o,_ in allo}
        if len(pos_set)!=len(allo): continue
        d={o:di for o,di in allo}
        cur=0; order=[]
        while cur<src_len:
            if cur not in d: ok=False;break
            di=d[cur]; order.append(di); cur+=length_of[di]
        if ok and cur==src_len and len(order)==len(allo):
            restored=b''.join(ents[i].block.to_bytes() for i in order)
            return restored,src_len,[s for s,_ in combo]
    raise RuntimeError('no tiling found')

def reverse_B(wire):
    r=_Reader(wire); assert r.take(4)==cycle.MAGIC
    r.take(32); r.take(32); root=r.take(32).hex(); rc=r.uint(); data=r.blob(LIM.round_bytes)
    # build public routes using public prime paths (same as cycle-v1 per README: prime_path public)
    from numeral import PrimePath
    from prime_schedule import Route
    engine=numeral._Primes(LIM.numeral())
    specs=[]
    for rd in pub['rounds']:
        pp=PrimePath(rd['prime_path']['seed'],tuple(tuple(s) for s in rd['prime_path']['steps']))
        specs.append((pp,tuple(rd['arities']),rd['end_order']))
    routes=[Route.evaluate(pp,LIM.numeral(),engine=engine) for pp,_,_ in specs]
    for i in range(rc-1,-1,-1):
        pp,arities,end_order=specs[i]; route=routes[i]
        split=plan(len(data)*8,route,arities,LIM.numeral(),engine=engine)
        packed=interleave(data,split,inverse=True,end_order=end_order)
        data,src_len,spaces=solve_round(packed)
        print(f'   round {i}: src_len {src_len} spaces {[str(x) for x in spaces]}')
    return data,root

if __name__=='__main__':
    for k in ['b01','b02','b03','b04']:
        wire=Path(f'/workspace/cypher/v1/ciphertexts/{k}.wvc').read_bytes()
        try:
            data,root=reverse_B(wire)
            assert data[:4]==NORMAL_MAGIC,data[:8]
            length=int.from_bytes(data[4:12],'big'); ch=data[12:44].hex(); msg=data[44:44+length]
            rec=api.ByteOrigin(data,pub['scope'],0,geometry).message_origin
            Path(f'/workspace/cypher/work/{k}.recovered').write_bytes(msg)
            print(f'=== {k}: RECOVERED {length} bytes corpus_sha256={ch} root_ok={rec==root}')
            print('   preview',msg[:280])
        except Exception as e:
            import traceback;print(f'=== {k} FAILED',repr(e)); traceback.print_exc()
