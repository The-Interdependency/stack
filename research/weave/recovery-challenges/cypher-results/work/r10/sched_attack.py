#!/usr/bin/env python3
"""Round 10: schedule-trie attack over the PUBLIC schedule catalog (v2/matrix.py).

For every unrecovered file, walk the trie of reversed byte/reflection schedules
from matrix.schedules(), applying public inverses:
  B, R (involutions), W (whole inverse), N (literal extract data[44:44+L]),
  U (numeral restore), A (analytic space recovery, fastA.py),
  S (one of 30 public catalog specs; one spec shared per case as in matrix.parameters).
Accept only strict format: 'Prediction <32hex>: ...' + line 2 'my human needs my help'.
Outputs are FORMAT-VALID CANDIDATES, not oracle/byte-exact confirmations.
"""
import sys, os, signal, hashlib, time, json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
sys.path.insert(0,'/workspace/cypher/work/r10'); sys.path.insert(0,'/workspace/cypher/src'); sys.path.insert(0,'/workspace/cypher/v2')
ROOT=Path('/workspace/cypher/v2/blind/files'); OUT=Path('/workspace/cypher/work/v2_recovered')
NEWDIR=Path('/workspace/cypher/work/r10/new'); NEWDIR.mkdir(exist_ok=True)
KNOWN='my human needs my help'
HEX=set('0123456789abcdef')
def ok_text(b):
    try: t=b.decode('utf-8')
    except Exception: return None
    if not t.startswith('Prediction '): return None
    lines=t.splitlines()
    if len(lines)<2 or lines[1]!=KNOWN or ': ' not in lines[0]: return None
    hx=lines[0].split(': ',1)[0][len('Prediction '):]
    if len(hx)!=32 or any(c not in HEX for c in hx): return None
    return t if t.endswith('\n') else t+'\n'

def build_trie():
    import matrix
    rows=[r for r in matrix.schedules() if r['family'] in ('byte','reflection')]
    trie={}; 
    for r in rows:
        node=trie
        for op in reversed(r['schedule']):
            node=node.setdefault(op,{})
        node['$']=True
    return trie, len(rows)

_G={}
def init():
    import fastA, prime_schedule as prime, numeral
    from numeral import PrimePath
    _G['fastA']=fastA; _G['asm']=fastA.asm; _G['prime']=prime; _G['numeral']=numeral
    routes=[prime.Route.evaluate(p) for p in [PrimePath(53,(('next',),('next',))),PrimePath(5381,(('span',10,0,2),('next',),('next',))),PrimePath(13,(('span',2,0,2),('next',)))]]
    specs=[(ri,ar,end) for ri in range(3) for ar in [(3,),(5,),(7,),(3,5,7),(7,3,5)] for end in ['first-last','last-first']]
    _G['routes']=routes; _G['specs']=specs
    _G['trie'],_=build_trie()

class TO(Exception): pass
def _al(s,f): raise TO()

def inv(op, d, sspec, memo):
    key=(hashlib.blake2b(d,digest_size=12).digest(), op, sspec)
    if key in memo: return memo[key]
    asm=_G['asm']; res=[]
    try:
        if op=='B': res=[asm.do_B(d)]
        elif op=='R': res=[asm.do_R(d)]
        elif op=='W': res=[asm.do_W(d)]
        elif op=='N':
            if d.startswith(b'WNM\x01') and len(d)>44:
                L=int.from_bytes(d[4:12],'big')
                if 1<=L<=len(d)-44: res=[d[44:44+L]]
        elif op=='U':
            if d.startswith(b'WNC\x01'): res=[_G['numeral'].decode(d).restore().to_bytes()]
        elif op=='A':
            res=_G['fastA'].invert_A(d)
        elif op=='S':
            ri,ar,end=_G['specs'][sspec]; prime=_G['prime']
            split=prime.plan(len(d)*8,_G['routes'][ri],ar)
            res=[prime.interleave(d,split,inverse=True,end_order=end)]
    except TO: raise
    except Exception: res=[]
    res=[x for x in res if x]
    memo[key]=res
    return res

def dfs(d, node, sspec, memo, depth=0):
    if '$' in node:
        t=ok_text(d)
        if t: return t
    for op,child in node.items():
        if op=='$': continue
        specs=[sspec] if (op!='S' or sspec is not None) else range(30)
        for sp in specs:
            for nd in inv(op,d,sp if op=='S' else None,memo):
                t=dfs(nd,child,sp if op=='S' else sspec,memo,depth+1)
                if t: return t
    return None

def worker(args):
    path,secs=args
    if not _G: init()
    signal.signal(signal.SIGALRM,_al); signal.alarm(secs)
    t0=time.time()
    try:
        t=dfs(Path(path).read_bytes(),_G['trie'],None,{})
        st='hit' if t else 'miss'
    except TO: t=None; st='timeout'
    except RecursionError: t=None; st='recursion'
    finally: signal.alarm(0)
    return Path(path).name,t,st,round(time.time()-t0,1)

def main():
    secs=int(sys.argv[1]) if len(sys.argv)>1 else 120
    workers=int(sys.argv[2]) if len(sys.argv)>2 else 6
    only=sys.argv[3] if len(sys.argv)>3 else None
    rec=set((OUT/'RECOVERED_IDS.txt').read_text().split())
    done=set()
    prog=Path('/workspace/cypher/work/r10/progress.jsonl')
    if prog.exists():
        for l in prog.read_text().splitlines():
            r=json.loads(l)
            if r['secs']>=secs or r['st']=='hit': done.add(r['id'])
    files=[p for p in sorted(ROOT.glob('*.bin')) if p.name not in rec and p.name not in done]
    if only: files=[p for p in files if p.name in set(Path(only).read_text().split())]
    _,n=build_trie(); print('schedules',n,'targets',len(files),flush=True)
    new=0
    with ProcessPoolExecutor(max_workers=workers,initializer=init) as ex:
        futs=[ex.submit(worker,(str(p),secs)) for p in files]
        with prog.open('a') as pf:
            for i,f in enumerate(as_completed(futs)):
                name,t,st,el=f.result()
                if t:
                    (NEWDIR/(Path(name).stem+'.txt')).write_text(t)
                    (OUT/(Path(name).stem+'.txt')).write_text(t); new+=1
                    print('GOT',name,t.splitlines()[0][:60],el,flush=True)
                pf.write(json.dumps({'id':name,'st':st,'secs':secs,'el':el})+'\n'); pf.flush()
                if (i+1)%25==0: print(f'... {i+1}/{len(files)} new={new}',flush=True)
    print('done new',new,flush=True)
if __name__=='__main__': main()
