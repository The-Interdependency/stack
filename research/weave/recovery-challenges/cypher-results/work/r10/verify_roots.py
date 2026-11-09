#!/usr/bin/env python3
"""Round 10: root-verify A layers using a scope leaked by U in the same case.

operations.transform uses ONE parameters['scope'] per case for both U and A.
U's numeral packet stores that scope as packet.origin (public decode).  A's
WRA1 header stores message_origin = digest(schema, version, scope, byte_length,
sha256(A input)) (native_binary.ByteOrigin).  So for cases containing U and A,
ByteOrigin(recovered A input, scope).message_origin == header root is a
digest-level byte-exact check of that layer, needing no private material.
Tiers:  T1 = verified A input IS the final candidate plaintext (A innermost);
        T2 = a verified A layer lies on the recovery path (plaintext then follows
             by public deterministic inverses); T3 = format filter only.
"""
import sys, json, signal
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
sys.path.insert(0,'/workspace/cypher/work/r10')
import sched_attack as S
OUT=S.OUT; ROOT=S.ROOT

def dfs(d,node,sspec,memo,path):
    if '$' in node:
        t=S.ok_text(d)
        if t: return t,list(path)
    for op,child in node.items():
        if op=='$': continue
        for sp in ([sspec] if (op!='S' or sspec is not None) else range(30)):
            for nd in S.inv(op,d,sp if op=='S' else None,memo):
                path.append((op,d,nd))
                r=dfs(nd,child,sp if op=='S' else sspec,memo,path)
                path.pop()
                if r: return r
    return None

def worker(name):
    if not S._G: S.init()
    import fastA, numeral
    asm=fastA.asm
    signal.signal(signal.SIGALRM,S._al); signal.alarm(240)
    try:
        r=dfs((ROOT/name).read_bytes(),S._G['trie'],None,{},[])
    except Exception as e: return name,{'st':'timeout' if isinstance(e,S.TO) else 'err'}
    finally: signal.alarm(0)
    if not r: return name,{'st':'nohit'}
    t,path=r
    want=(OUT/(Path(name).stem+'.txt')).read_text()
    if t!=want: return name,{'st':'differs'}
    scopes=set()
    for op,a,b in path:
        if op=='U':
            try: scopes.add(numeral.decode(a).origin)
            except Exception: pass
    alayers=[(a,b) for op,a,b in path if op=='A']
    ver=[]
    for a,b in alayers:
        ok=False
        for sc in scopes:
            try:
                if asm.api.ByteOrigin(b,sc,0,asm.geometry).message_origin==a[4:36].hex(): ok=True
            except Exception: pass
        ver.append(ok)
    ptb=t.encode()
    tier=3
    if any(ver): tier=2
    if any(v and b==ptb for v,(a,b) in zip(ver,alayers)): tier=1
    return name,{'st':'ok','sched':''.join(op for op,_,_ in path),'nA':len(alayers),'nU':sum(op=='U' for op,_,_ in path),'Averified':sum(ver),'tier':tier}

def main():
    ids=sorted((OUT/'RECOVERED_IDS.txt').read_text().split())
    res={}
    with ProcessPoolExecutor(7,initializer=S.init) as ex:
        futs=[ex.submit(worker,i) for i in ids]
        for k,f in enumerate(as_completed(futs)):
            n,r=f.result(); res[n]=r
            if (k+1)%100==0: print(k+1,flush=True)
    json.dump(res,open('/workspace/cypher/work/r10/root_verify.json','w'),indent=0,sort_keys=True)
    from collections import Counter
    print(Counter(r['st'] for r in res.values()), Counter(r.get('tier') for r in res.values()))
if __name__=='__main__': main()
