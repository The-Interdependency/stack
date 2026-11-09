#!/usr/bin/env python3
"""Relaxed probe for trie misses: allow independent S spec per S layer and up to
16 A cover solutions (A without the 2^-16 space prior as fallback)."""
import sys; sys.path.insert(0,'/workspace/cypher/work/r10')
import sched_attack as s, fastA
from pathlib import Path
s.init()
orig=fastA.invert_A
fastA.invert_A=lambda d,prior=True,maxsol=16: orig(d,prior,16)
def dfs(d,node,memo):
    if '$' in node:
        t=s.ok_text(d)
        if t: return t
    for op,child in node.items():
        if op=='$': continue
        for sp in (range(30) if op=='S' else [None]):
            for nd in s.inv(op,d,sp,memo):
                t=dfs(nd,child,memo)
                if t: return t
for name in sys.argv[1:]:
    t=dfs((s.ROOT/name).read_bytes(),s._G['trie'],{})
    print(name, repr(t))
    if t: (s.NEWDIR/(Path(name).stem+'.txt')).write_text(t); (s.OUT/(Path(name).stem+'.txt')).write_text(t)
