#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
from fractions import Fraction
from collections import defaultdict, Counter
sys.path.insert(0,'/workspace/cypher/src')
import cycle, numeral, prime_schedule as prime
from cycle import CycleLimits
from cycle_native import load_native
from numeral import _Reader, decode as decode_numeral, PrimePath
from stages.api import Streams
from stages import whole as whole_stage

ROOT=Path('/workspace/cypher/v2/blind/files')
OUT=Path('/workspace/cypher/work/v2_recovered')
KNOWN='my human needs my help'
LIM=CycleLimits()
api,geometry=load_native('/workspace/cypher/src/sources')
BT=bytes(int(f'{i:08b}'[::-1],2) for i in range(256))
ROUTES=[prime.Route.evaluate(p) for p in [
    PrimePath(53,(('next',),('next',))),
    PrimePath(5381,(('span',10,0,2),('next',),('next',))),
    PrimePath(13,(('span',2,0,2),('next',))),
]]
ARITIES=[(3,),(5,),(7,),(3,5,7),(7,3,5)]; ENDS=['first-last','last-first']

def ok(b):
    try: t=b.decode('utf-8')
    except: return None
    if not t.startswith('Prediction '): return None
    lines=t.splitlines()
    return t if len(lines)>=2 and lines[1]==KNOWN else None

def do_B(d): return d.translate(BT)
def do_R(d):
    if len(d)%3: raise ValueError
    return b''.join(d[i:i+3][::-1] for i in range(0,len(d),3))
def do_W(d):
    bits=tuple((b>>s)&1 for b in d for s in range(7,-1,-1))
    inv=whole_stage.inverse(Streams((bits,)),None).lanes[0]
    return bytes(sum(inv[i+k]<<(7-k) for k in range(8)) for i in range(0,len(inv),8))
def S_list(d):
    out=[]; bl=len(d)*8
    for route in ROUTES:
        for ar in ARITIES:
            if any(a>bl for a in ar): continue
            try: split=prime.plan(bl,route,ar)
            except: continue
            for end in ENDS:
                try: out.append(prime.interleave(d,split,inverse=True,end_order=end))
                except: continue
    return out

def peel(msg):
    t=ok(msg)
    if t: return t
    for fn in (do_B,do_R,do_W):
        try:
            t=ok(fn(msg))
            if t: return t
        except: pass
    for s in S_list(msg):
        t=ok(s)
        if t: return t
        for fn in (do_B,do_R,do_W):
            try:
                t=ok(fn(s))
                if t: return t
            except: pass
    return None

def parse(waf):
    r=_Reader(waf)
    assert r.take(4)==cycle.AFFIX_MAGIC
    src=r.uint()
    packet=decode_numeral(r.blob(LIM.round_bytes),LIM.numeral())
    counts=tuple(r.uint() for _ in range(7))
    positions=[Fraction(r.uint(),r.uint()) for _ in packet.symbols]
    assert r.pos==len(waf)
    return src,packet,counts,positions

def try_cover(src,packet,counts,positions):
    by_sym={e.symbol:i for i,e in enumerate(packet.entries)}
    length_of=[e.block.length//8 for e in packet.entries]
    wire_idx=[by_sym[s] for s in packet.symbols]
    percirc=defaultdict(list); cur=0
    for c in range(1,8):
        for _ in range(counts[c-1]):
            percirc[c].append((wire_idx[cur],positions[cur])); cur+=1
    # find one valid space per circle via coarse then fine
    opts_by_c={}
    DEN=65536
    for c,lst in percirc.items():
        if not lst:
            opts_by_c[c]=[(Fraction(0,1),())]; continue
        hit=None
        step=max(1,src)
        for num in list(range(0,2*DEN,step))+list(range(0,2*DEN)):
            s=Fraction(num,DEN)
            offs=[]; ok_=True
            for di,p in lst:
                try: ax=geometry.recover_axis(packet.origin,src,p,s)
                except Exception: ok_=False; break
                offs.append((ax.axis_ordinal,di,length_of[di]))
            if ok_ and len({o for o,_,_ in offs})==len(offs) and all(0<=o<src for o,_,_ in offs):
                hit=s; break
        if hit is None: return None
        # orbit expand
        opts=[]
        for k in range(-src,src+1):
            s=hit+Fraction(k,src)
            while s<0: s+=2
            while s>=2: s-=2
            offs=[]; ok_=True
            for di,p in lst:
                try: ax=geometry.recover_axis(packet.origin,src,p,s)
                except Exception: ok_=False; break
                offs.append((ax.axis_ordinal,di,length_of[di]))
            if ok_ and len({o for o,_,_ in offs})==len(offs) and all(0<=o<src for o,_,_ in offs):
                opts.append((s,tuple(sorted(offs))))
        # dedupe
        uniq=[]; seen=set()
        for s,offs in opts:
            if offs in seen: continue
            seen.add(offs); uniq.append((s,offs))
        opts_by_c[c]=uniq
    # exact cover
    circles=sorted(opts_by_c,key=lambda c: len(opts_by_c[c]))
    occ=[None]*src; lens=[None]*src
    def place(ci):
        if ci==len(circles): return True
        c=circles[ci]
        for s,offs in opts_by_c[c]:
            ok_=True; written=[]
            for o,di,L in offs:
                if o+L>src: ok_=False; break
                for x in range(o,o+L):
                    if occ[x] is not None: ok_=False; break
                if not ok_: break
                for x in range(o,o+L):
                    occ[x]=di; lens[x]=(L if x==o else -1)
                written.append((o,L))
            if ok_ and place(ci+1): return True
            for o,L in written:
                for x in range(o,o+L): occ[x]=None; lens[x]=None
        return False
    if not place(0): return None
    parts=[]; i=0
    while i<src:
        di=occ[i]; parts.append(packet.entries[di].block.to_bytes()); i+=lens[i]
    return b''.join(parts)

def main():
    rec=set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    new=0
    targets=[]
    for p in sorted(ROOT.glob('*.bin')):
        if p.name in rec: continue
        raw=p.read_bytes()
        for d in (raw, raw.translate(BT)):
            if not d.startswith(b'WRA1'): continue
            try:
                src,packet,counts,pos=parse(d[36:])
            except Exception: continue
            if src<=220:
                targets.append((p,d,src)); break
    print('small WRA1',len(targets),flush=True)
    for i,(p,d,src) in enumerate(targets):
        try:
            src,packet,counts,pos=parse(d[36:])
            msg=try_cover(src,packet,counts,pos)
        except Exception as e:
            print('fail',p.name,e); continue
        if msg is None:
            print('no cover',p.name,src); continue
        t=peel(msg)
        if t:
            (OUT/(p.stem+'.txt')).write_text(t if t.endswith('\n') else t+'\n')
            new+=1; print('GOT',p.name,src,flush=True)
        else:
            print('cover but no peel',p.name,src,msg[:40],flush=True)
        if (i+1)%5==0: print(f'…{i+1}/{len(targets)} new={new}',flush=True)
    ids=sorted(x.stem+'.bin' for x in OUT.glob('*.txt') if x.name!='RECOVERED_IDS.txt')
    Path(OUT/'RECOVERED_IDS.txt').write_text('\n'.join(ids)+'\n')
    print('new',new,'total',len(ids))
if __name__=='__main__': main()
