#!/usr/bin/env python3
"""Faster WRA1 recovery: find one valid space per circle, expand by 1/src_len orbit, exact-cover, then S/B/R/N/U peel."""
from __future__ import annotations
import sys, json
from pathlib import Path
from fractions import Fraction
from collections import defaultdict, Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
sys.path.insert(0, '/workspace/cypher/src')
import cycle, numeral, prime_schedule as prime
from cycle import CycleLimits
from cycle_native import load_native
from numeral import _Reader, decode as decode_numeral

ROOT = Path('/workspace/cypher/v2/blind/files')
OUT = Path('/workspace/cypher/work/v2_recovered')
KNOWN = 'my human needs my help'
LIM = CycleLimits()
BIT_REVERSE = bytes(int(f'{i:08b}'[::-1], 2) for i in range(256))
PATHS = [
    numeral.PrimePath(53, (('next',),('next',))),
    numeral.PrimePath(5381, (('span',10,0,2),('next',),('next',))),
    numeral.PrimePath(13, (('span',2,0,2),('next',))),
]
ARITIES = [(3,),(5,),(7,),(3,5,7),(7,3,5)]
ENDS = ['first-last','last-first']

def is_plain(b):
    try: t=b.decode('utf-8')
    except Exception: return None
    return t if KNOWN in t else None

def parse_waf(packed):
    r=_Reader(packed)
    assert r.take(4)==cycle.AFFIX_MAGIC
    src_len=r.uint()
    packet=decode_numeral(r.blob(LIM.round_bytes), LIM.numeral())
    counts=tuple(r.uint() for _ in range(7))
    positions=[Fraction(r.uint(), r.uint()) for _ in packet.symbols]
    assert r.pos==len(packed)
    return src_len, packet, counts, positions

def orbit_spaces(geometry, origin, src_len, lst):
    """Find valid spaces by probing every src_len-th reduced fraction, expand orbits."""
    DEN=65536; step=src_len
    hits=[]
    # probe a coarse grid first
    for num in range(0, 2*DEN, max(1, step)):
        s=Fraction(num, DEN)
        offs=[]; ok=True
        for di,p in lst:
            try: ax=geometry.recover_axis(origin, src_len, p, s)
            except Exception: ok=False; break
            offs.append((ax.axis_ordinal, di))
        if ok and len({o for o,_ in offs})==len(offs) and all(0<=o<src_len for o,_ in offs):
            hits.append(s)
            break
    if not hits:
        # denser scan
        for num in range(0, 2*DEN):
            s=Fraction(num, DEN)
            offs=[]; ok=True
            for di,p in lst:
                try: ax=geometry.recover_axis(origin, src_len, p, s)
                except Exception: ok=False; break
                offs.append((ax.axis_ordinal, di))
            if ok and len({o for o,_ in offs})==len(offs) and all(0<=o<src_len for o,_ in offs):
                hits.append(s); break
    if not hits: return []
    # expand orbit around first hit
    base=hits[0]; opts=[]
    for k in range(-src_len, src_len+1):
        s=Fraction(base.numerator, base.denominator) + Fraction(k, src_len)
        # reduce into [0,2)
        while s<0: s+=2
        while s>=2: s-=2
        s=Fraction(s.numerator, s.denominator)  # canonical
        offs=[]; ok=True
        for di,p in lst:
            try: ax=geometry.recover_axis(origin, src_len, p, s)
            except Exception: ok=False; break
            offs.append((ax.axis_ordinal, di, None))  # length filled later
        if ok and len({o for o,_,_ in offs})==len(offs) and all(0<=o<src_len for o,_,_ in offs):
            opts.append((s, offs))
    return opts

def exact_cover(src_len, opts_by_c, length_of):
    # attach lengths
    for c in opts_by_c:
        fixed=[]
        for s,offs in opts_by_c[c]:
            fixed.append((s, tuple(sorted((o,di,length_of[di]) for o,di,_ in offs))))
        opts_by_c[c]=fixed
    circles=sorted(opts_by_c, key=lambda c: len(opts_by_c[c]))
    occ=[None]*src_len; lens=[None]*src_len
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
                for x in range(o,o+L):
                    occ[x]=di; lens[x]=(L if x==o else -1)
                written.append((o,L))
            if ok and place(ci+1): return True
            for o,L in written:
                for x in range(o,o+L): occ[x]=None; lens[x]=None
        return False
    if not place(0): raise RuntimeError('no cover')
    order=[]; i=0
    while i<src_len:
        order.append(occ[i]); i+=lens[i]
    return order

def post_peel(data):
    """Try N/U/B/R/S catalog to reach plaintext."""
    cands=[('A', data)]
    if data.startswith(b'WNM\x01') and len(data)>=44:
        L=int.from_bytes(data[4:12],'big')
        if 1<=L<=len(data)-44: cands.append(('A/N', data[44:44+L]))
    if data.startswith(b'WNC\x01'):
        try: cands.append(('A/U', numeral.decode(data).restore().to_bytes()))
        except Exception: pass
    routes=[prime.Route.evaluate(p) for p in PATHS]
    for lab, blob in list(cands):
        t=is_plain(blob)
        if t: return t, lab
        for n,fn in [('B', lambda d:d.translate(BIT_REVERSE)),
                     ('R', lambda d: b''.join(d[i:i+3][::-1] for i in range(0,len(d),3)) if len(d)%3==0 else (_ for _ in ()).throw(ValueError()))]:
            try:
                b2=fn(blob); t=is_plain(b2)
                if t: return t, lab+'/'+n
            except Exception: pass
        # S
        bl=len(blob)*8
        for ri,route in enumerate(routes):
            for ar in ARITIES:
                if any(a>bl for a in ar): continue
                try: split=prime.plan(bl, route, ar)
                except Exception: continue
                for end in ENDS:
                    try: out=prime.interleave(blob, split, inverse=True, end_order=end)
                    except Exception: continue
                    t=is_plain(out)
                    if t: return t, f'{lab}/S'
                    if out.startswith(b'WNM\x01') and len(out)>=44:
                        L=int.from_bytes(out[4:12],'big')
                        if 1<=L<=len(out)-44:
                            t=is_plain(out[44:44+L])
                            if t: return t, f'{lab}/S/N'
    return None, None

_GEOM=None
def get_geom():
    global _GEOM
    if _GEOM is None:
        _GEOM=load_native('/workspace/cypher/src/sources')
    return _GEOM

def crack_one(path):
    api, geometry = get_geom()
    d=Path(path).read_bytes()
    if d[:4]!=b'WRA1': return Path(path).name, None, None
    wire=d[36:]
    try:
        src_len, packet, counts, positions = parse_waf(wire)
    except Exception as e:
        return Path(path).name, None, f'parse:{e}'
    by_sym={e.symbol:i for i,e in enumerate(packet.entries)}
    length_of=[e.block.length//8 for e in packet.entries]
    wire_idx=[by_sym[s] for s in packet.symbols]
    percirc=defaultdict(list); cur=0
    for c in range(1,8):
        for _ in range(counts[c-1]):
            percirc[c].append((wire_idx[cur], positions[cur])); cur+=1
    opts={}
    for c,lst in percirc.items():
        o=orbit_spaces(geometry, packet.origin, src_len, lst)
        if not o: return Path(path).name, None, f'no space c={c}'
        opts[c]=o
    try:
        order=exact_cover(src_len, opts, length_of)
    except Exception as e:
        return Path(path).name, None, f'cover:{e}'
    data=b''.join(packet.entries[di].block.to_bytes() for di in order)
    t, lab = post_peel(data)
    return Path(path).name, t, lab

def main():
    recovered=set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    wra1=[str(p) for p in sorted(ROOT.glob('*.bin'))
          if p.name not in recovered and p.read_bytes()[:4]==b'WRA1']
    print('targets', len(wra1))
    new=0; methods=Counter()
    # process sequentially first few to validate speed, then parallel
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs={ex.submit(crack_one, p): p for p in wra1}
        done=0
        for fut in as_completed(futs):
            name,t,lab=fut.result(); done+=1
            if t:
                new+=1; recovered.add(name); methods[lab]+=1
                (OUT/(Path(name).stem+'.txt')).write_text(t)
                print('GOT', name, lab, t[:50].replace('\n','|'))
            if done%25==0:
                print(f'… {done}/{len(wra1)} new={new}', flush=True)
    (OUT/'RECOVERED_IDS.txt').write_text('\n'.join(sorted(recovered)))
    print(json.dumps({'new':new,'total':len(recovered),'methods':methods.most_common()}, indent=2))

if __name__=='__main__':
    main()
