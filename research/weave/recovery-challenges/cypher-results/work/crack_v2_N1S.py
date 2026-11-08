#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
from collections import Counter
sys.path.insert(0,'/workspace/cypher/src')
import numeral, prime_schedule as prime
from stages.api import Streams
from stages import whole as whole_stage

ROOT=Path('/workspace/cypher/v2/blind/files')
OUT=Path('/workspace/cypher/work/v2_recovered')
KNOWN='my human needs my help'
BT=bytes(int(f'{i:08b}'[::-1],2) for i in range(256))
PATHS=[
    {'seed':53,'steps':[('next',),('next',)]},
    {'seed':5381,'steps':[('span',10,0,2),('next',),('next',)]},
    {'seed':13,'steps':[('span',2,0,2),('next',)]},
]
ARITIES=[(3,),(5,),(7,),(3,5,7),(7,3,5)]
ENDS=['first-last','last-first']
_ROUTES=[prime.Route.evaluate(numeral.PrimePath(p['seed'],tuple(p['steps']))) for p in PATHS]

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
def do_U(d): return numeral.decode(d).restore().to_bytes()
def do_N(d):
    L=int.from_bytes(d[4:12],'big')
    if not 1<=L<=len(d)-44: raise ValueError
    return d[44:44+L]

def S_list(d):
    out=[]; bl=len(d)*8
    for route in _ROUTES:
        for ar in ARITIES:
            if any(a>bl for a in ar): continue
            try: split=prime.plan(bl,route,ar)
            except: continue
            for end in ENDS:
                try: out.append(prime.interleave(d,split,inverse=True,end_order=end))
                except: continue
    return out

def refine(blob):
    cands=[blob]
    for fn in (do_B,do_R):
        try: cands.append(fn(blob))
        except: pass
    if len(blob)<=8192:
        try: cands.append(do_W(blob))
        except: pass
    for c in cands:
        t=ok(c)
        if t: return t
        if c.startswith(b'WNM\x01'):
            try:
                m=do_N(c); t=ok(m)
                if t: return t
                for fn in (do_B,do_R):
                    try:
                        t=ok(fn(m))
                        if t: return t
                    except: pass
            except: pass
        if c.startswith(b'WNC\x01'):
            try:
                m=do_U(c); t=ok(m)
                if t: return t
            except: pass
    return None

def crack(d):
    bases=[('id',d)]
    for n,f in (('B',do_B),('R',do_R)):
        try: bases.append((n,f(d)))
        except: pass
    for pref,cur in bases:
        body=None; tag=None
        if cur.startswith(b'WNM\x01'):
            try: body=do_N(cur); tag='N'
            except: pass
        elif cur.startswith(b'WNC\x01'):
            try: body=do_U(cur); tag='U'
            except: pass
        if body is None: continue
        t=refine(body)
        if t: return t,[pref,tag]
        s1s=S_list(body)
        for s in s1s:
            t=refine(s)
            if t: return t,[pref,tag,'S']
        if len(body)<=500:
            for s1 in s1s:
                for s2 in S_list(s1):
                    t=refine(s2)
                    if t: return t,[pref,tag,'S','S']
    return None,None

def main():
    rec=set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    new=0; meth=Counter()
    targets=[]
    for p in sorted(ROOT.glob('*.bin')):
        if p.name in rec: continue
        d=p.read_bytes()
        if d.startswith((b'WNM\x01',b'WNC\x01')) or do_B(d).startswith((b'WNM\x01',b'WNC\x01')):
            targets.append(p)
    print('targets',len(targets),flush=True)
    for i,p in enumerate(targets):
        t,path=crack(p.read_bytes())
        if t:
            new+=1; meth['/'.join(path)]+=1
            (OUT/(p.stem+'.txt')).write_text(t if t.endswith('\n') else t+'\n')
            print('GOT',p.name,path,flush=True)
        if (i+1)%50==0: print(f'…{i+1}/{len(targets)} new={new}',flush=True)
    ids=sorted(x.stem+'.bin' for x in OUT.glob('*.txt') if x.name!='RECOVERED_IDS.txt')
    Path(OUT/'RECOVERED_IDS.txt').write_text('\n'.join(ids)+'\n')
    print('new',new,'total',len(ids)); print(meth.most_common())
if __name__=='__main__': main()
