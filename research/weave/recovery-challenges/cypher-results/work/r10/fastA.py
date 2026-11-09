#!/usr/bin/env python3
"""Round 10: analytic WRA1 space recovery (no brute over 2^17 space numerators).

From ucns direct_mobius: recover_axis(position p, space s) is valid iff
q = (p + s) mod 2 lies in [0,1) (positive frame) and q*src is an integer;
the source byte offset is q*src.  So per circle, s is pinned to the coset
-p0 + Z/src; with the generator prior s in Z/65536 (matrix.round_parameters),
only O(gcd(src,65536)) shifts survive.  Exact cover then concatenates blocks.
"""
import sys, importlib.util
from fractions import Fraction
from collections import defaultdict
from math import gcd, floor, ceil
sys.path.insert(0,'/workspace/cypher/src')
spec=importlib.util.spec_from_file_location('asm','/workspace/cypher/work/crack_v2_Asmall.py')
asm=importlib.util.module_from_spec(spec); spec.loader.exec_module(asm)
parse=asm.parse

def circle_options(src, lst, lengths, prior=True, cap=4096):
    """lst: [(entry_index, position Fraction)]. Returns list of tuple offsets."""
    p0=lst[0][1]
    lo=ceil(p0*src); hi=ceil((2+p0)*src)  # m in [lo,hi): s=m/src-p0 in [0,2)
    opts=[]; seen=set()
    for m in range(lo,hi):
        s=Fraction(m,src)-p0
        if prior and (s*65536).denominator!=1: continue
        offs=[]; good=True
        for di,p in lst:
            q=(p+s)%2
            if q>=1: good=False; break
            o=q*src
            if o.denominator!=1: good=False; break
            o=int(o)
            if o+lengths[di]>src: good=False; break
            offs.append((o,di))
        if not good: continue
        key=tuple(sorted(offs))
        if len({o for o,_ in key})!=len(key) or key in seen: continue
        seen.add(key); opts.append(key)
        if len(opts)>=cap: break
    return opts

def cover_all(src, packet, counts, positions, prior=True, maxsol=4):
    by_sym={e.symbol:i for i,e in enumerate(packet.entries)}
    lengths=[e.block.length//8 for e in packet.entries]
    wire=[by_sym[s] for s in packet.symbols]
    percirc=defaultdict(list); cur=0
    for c in range(1,8):
        for _ in range(counts[c-1]):
            percirc[c].append((wire[cur],positions[cur])); cur+=1
    if sum(lengths[w] for w in wire)!=src: return []
    opts={}
    for c,lst in percirc.items():
        o=circle_options(src,lst,lengths,prior)
        if not o: return []
        # convert to bitmask
        opts[c]=[]
        for key in o:
            mask=0; ok=True
            for off,di in key:
                seg=((1<<lengths[di])-1)<<off
                if mask&seg: ok=False; break
                mask|=seg
            if ok: opts[c].append((mask,key))
        if not opts[c]: return []
    circles=sorted(opts,key=lambda c: len(opts[c]))
    full=(1<<src)-1; sols=[]
    def rec(i,mask,chosen):
        if len(sols)>=maxsol: return
        if i==len(circles):
            if mask==full: sols.append(list(chosen))
            return
        for m,key in opts[circles[i]]:
            if m&mask: continue
            chosen.append(key); rec(i+1,mask|m,chosen); chosen.pop()
            if len(sols)>=maxsol: return
    rec(0,0,[])
    out=[]
    for ch in sols:
        allo=sorted(x for key in ch for x in key)
        out.append(b''.join(packet.entries[di].block.to_bytes() for _,di in allo))
    return out

def invert_A(d, prior=True, maxsol=4):
    if not d.startswith(b'WRA1') or len(d)<37: return []
    try: src,packet,counts,pos=parse(d[36:])
    except Exception: return []
    try: res=cover_all(src,packet,counts,pos,prior,maxsol)
    except RecursionError: return []
    if not res and prior:
        try: res=cover_all(src,packet,counts,pos,False,maxsol)
        except RecursionError: return []
    return res
