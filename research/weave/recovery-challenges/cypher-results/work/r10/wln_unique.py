#!/usr/bin/env python3
"""Round 11: uniqueness re-check of coupled single-C WLN1 candidates.
Re-runs wln_coupled.solve for every accepted parameter set with maxsol=1000 and a
larger budget; records distinct messages and whether the DFS finished below budget
(exhaustive for that parameter set). Format-valid candidates only."""
import sys, json; sys.argv=['x']; sys.path.insert(0,'/workspace/cypher/work/r10')
from pathlib import Path
import wln_coupled as w
ROOT=Path('/workspace/cypher/v2/blind/files'); BUD=20_000_000
out={}
for l in open('/workspace/cypher/work/r10/wln_real.jsonl'):
    if not l.startswith('{'): continue
    d=json.loads(l)
    if not d['found']: continue
    st=w.tc.decode_lanes((ROOT/d['file']).read_bytes()); wl=[list(x) for x in st.lanes]
    msgs=set(); exh=True; ps=[]
    for p,_,_ in d['found']:
        s,n,t,r,a=p; u,v,final=w.layouts(tuple(s),n,t,r,a)
        sols,steps=w.solve(wl,u,v,maxsol=1000,budget=BUD)
        fin=steps<=BUD and len(sols)<1000; exh&=fin
        msgs|={x.decode() for x in sols}; ps.append([p,len(sols),steps,fin])
    out[d['file']]={'distinct_messages':len(msgs),'exhaustive_all_paramsets':exh,'paramsets':ps,'message':sorted(msgs)[0] if len(msgs)==1 else None}
    print(d['file'],len(msgs),exh,flush=True)
json.dump(out,open('/workspace/cypher/work/r10/wln_unique.json','w'),indent=1,sort_keys=True)
