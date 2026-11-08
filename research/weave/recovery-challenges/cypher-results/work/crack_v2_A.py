#!/usr/bin/env python3
"""Recover WRA1 (standalone affix) via recover_axis space search + exact cover.
No corpus needed; circle_order is in the WNC packet.
"""
from __future__ import annotations
import sys, json
from pathlib import Path
from fractions import Fraction
from collections import defaultdict, Counter
sys.path.insert(0, '/workspace/cypher/src')
import cycle, numeral
from cycle import CycleLimits
from cycle_native import load_native
from numeral import _Reader, decode as decode_numeral

ROOT = Path('/workspace/cypher/v2/blind/files')
OUT = Path('/workspace/cypher/work/v2_recovered')
KNOWN = 'my human needs my help'
LIM = CycleLimits()
api, geometry = load_native('/workspace/cypher/src/sources')
BIT_REVERSE = bytes(int(f'{i:08b}'[::-1], 2) for i in range(256))

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

def candidates(packed):
    src_len,packet,counts,positions=parse_waf(packed)
    by_sym={e.symbol:i for i,e in enumerate(packet.entries)}
    length_of=[e.block.length//8 for e in packet.entries]
    wire_idx=[by_sym[s] for s in packet.symbols]
    percirc=defaultdict(list); cur=0
    for c in range(1,8):
        for _ in range(counts[c-1]):
            percirc[c].append((wire_idx[cur], positions[cur])); cur+=1
    DEN=65536
    def cand():
        seen=set()
        for num in range(0, 2*DEN):
            s=Fraction(num,DEN); k=(s.numerator,s.denominator)
            if k in seen: continue
            seen.add(k); yield s
    out={}
    for c,lst in percirc.items():
        opts=[]
        for s in cand():
            offs=[]; ok=True
            for di,p in lst:
                try: ax=geometry.recover_axis(packet.origin, src_len, p, s)
                except Exception: ok=False; break
                offs.append((ax.axis_ordinal, di, length_of[di]))
            if ok and len({o for o,_,_ in offs})==len(offs) and all(0<=o<src_len for o,_,_ in offs):
                opts.append((s, tuple(sorted(offs))))
        out[c]=opts
    return src_len, packet, out

def exact_cover(src_len, opts_by_c):
    circles=sorted(opts_by_c, key=lambda c: len(opts_by_c[c]))
    occ=[None]*src_len; lens=[None]*src_len; choice={}
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
                    occ[x]=di; lens[x]=L if x==o else -1
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
    return choice, order

def restore_wra1(d):
    assert d[:4]==b'WRA1'
    root=d[4:36].hex(); wire=d[36:]
    src_len, packet, opts = candidates(wire)
    # if any circle has 0 opts, fail
    if any(len(opts[c])==0 for c in range(1,8)):
        raise RuntimeError('empty opts')
    choice, order = exact_cover(src_len, opts)
    data=b''.join(packet.entries[di].block.to_bytes() for di in order)
    # verify root optionally
    return data, root, choice

def main():
    recovered=set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    new=0; methods=Counter()
    files=[p for p in sorted(ROOT.glob('*.bin')) if p.name not in recovered]
    # prioritize WRA1
    wra1=[p for p in files if p.read_bytes()[:4]==b'WRA1']
    print('WRA1 unrecovered', len(wra1))
    for i,p in enumerate(wra1):
        d=p.read_bytes()
        # try raw and after B/R (unlikely for WRA1 magic)
        trials=[('A', d)]
        for label,fn in [('B+A', lambda x: x.translate(BIT_REVERSE))]:
            try:
                t=fn(d)
                if t[:4]==b'WRA1': trials.append((label,t))
            except Exception: pass
        got=None
        for lab, blob in trials:
            try:
                data, root, choice = restore_wra1(blob)
            except Exception as e:
                continue
            # data may still need N peel or be plaintext
            t=is_plain(data)
            path=[lab]
            if t is None and data.startswith(b'WNM\x01') and len(data)>=44:
                L=int.from_bytes(data[4:12],'big')
                if 1<=L<=len(data)-44:
                    msg=data[44:44+L]; t=is_plain(msg); path.append('N')
            if t is None and data.startswith(b'WNC\x01'):
                try:
                    msg=numeral.decode(data).restore().to_bytes(); t=is_plain(msg); path.append('U')
                except Exception: pass
            if t is not None:
                got=(t,path); break
        if got:
            t,path=got; new+=1; recovered.add(p.name); methods['/'.join(path)]+=1
            (OUT/(p.stem+'.txt')).write_text(t)
            print('GOT', p.name, path, t[:50].replace('\n','|'))
        if (i+1)%20==0:
            print(f'… {i+1}/{len(wra1)} new={new}', flush=True)
    (OUT/'RECOVERED_IDS.txt').write_text('\n'.join(sorted(recovered)))
    print(json.dumps({'new':new,'total':len(recovered),'methods':methods.most_common()}, indent=2))

if __name__=='__main__':
    main()
