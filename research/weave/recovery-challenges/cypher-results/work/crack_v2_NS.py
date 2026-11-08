#!/usr/bin/env python3
"""N/U-first then S catalog (and B/R/W), for wires that still show WNM/WNC."""
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
    if not (t.startswith('Prediction ') and KNOWN in t): return None
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
    if not d.startswith(b'WNM\x01') or len(d)<44: raise ValueError
    L=int.from_bytes(d[4:12],'big')
    if not 1<=L<=len(d)-44: raise ValueError
    return d[44:44+L]

def all_S(d):
    bl=len(d)*8
    for ri,route in enumerate(_ROUTES):
        for ar in ARITIES:
            if any(a>bl for a in ar): continue
            try: split=prime.plan(bl,route,ar)
            except: continue
            for end in ENDS:
                try: yield f'S{ri}{ar}{end}', prime.interleave(d,split,inverse=True,end_order=end)
                except: continue

def search(seed, max_s=2):
    # BFS of peels: N/U/B/R/W and up to max_s S applications
    from collections import deque
    q=deque([(seed,(),0)]); seen={seed}
    while q:
        cur,path,sc=q.popleft()
        t=ok(cur)
        if t: return t,list(path)
        if len(path)>=6: continue
        # N/U if magic
        if cur.startswith(b'WNM\x01'):
            try:
                nxt=do_N(cur)
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt,path+('N',),sc))
            except: pass
        if cur.startswith(b'WNC\x01'):
            try:
                nxt=do_U(cur)
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt,path+('U',),sc))
            except: pass
        for name,fn in (('B',do_B),('R',do_R)):
            try:
                nxt=fn(cur)
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt,path+(name,),sc))
            except: pass
        if len(cur)<=8192 and 'W' not in path:
            try:
                nxt=do_W(cur)
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt,path+('W',),sc))
            except: pass
        if sc<max_s and len(cur)<=12000:
            for lab,nxt in all_S(cur):
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt,path+(lab,),sc+1))
    return None,None

def main():
    rec=set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    new=0; meth=Counter()
    targets=[]
    for p in ROOT.glob('*.bin'):
        if p.name in rec: continue
        d=p.read_bytes()
        # remaining WNM/WNC or B-scrambled forms, or opaque small
        if d.startswith((b'WNM\x01',b'WNC\x01')) or len(d)<8000:
            targets.append(p)
    print('targets',len(targets),flush=True)
    for i,p in enumerate(targets):
        t,path=search(p.read_bytes(), max_s=2)
        if t:
            new+=1; meth['/'.join(path)]+=1
            (OUT/(p.stem+'.txt')).write_text(t if t.endswith('\n') else t+'\n')
            print('GOT',p.name,path[:4],flush=True)
        if (i+1)%100==0: print(f'…{i+1} new={new}',flush=True)
    ids=sorted(x.stem+'.bin' for x in OUT.glob('*.txt') if x.name!='RECOVERED_IDS.txt')
    Path(OUT/'RECOVERED_IDS.txt').write_text('\n'.join(ids)+'\n')
    print('new',new,'total',len(ids)); print(meth.most_common(25))
if __name__=='__main__': main()
