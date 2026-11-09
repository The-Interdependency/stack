#!/usr/bin/env python3
"""Re-validate every on-disk v2 output under the strict format filter; rebuild
RECOVERED_IDS.txt and print family/tag counts. Format-valid candidates only."""
import json, sys
from pathlib import Path
from collections import Counter
OUT=Path('/workspace/cypher/work/v2_recovered'); ROOT=Path('/workspace/cypher/v2/blind/files')
KNOWN='my human needs my help'; HEX=set('0123456789abcdef')
def ok(t):
    if not t.startswith('Prediction '): return False
    L=t.splitlines()
    if len(L)<2 or L[1]!=KNOWN or ': ' not in L[0]: return False
    hx=L[0].split(': ',1)[0][11:]
    return len(hx)==32 and set(hx)<=HEX
FAM=[('permutation rules','permutation / selected order'),('lane rules','lane rules / route controls'),
     ('source-guided','source-guided / A'),('reflections','reflections cancel'),('literal containers','literal containers')]
good=[];bad=[];fam=Counter();orphan=[]
for p in sorted(OUT.glob('*.txt')):
    if p.name=='RECOVERED_IDS.txt': continue
    t=p.read_text(errors='replace')
    if not (ROOT/(p.stem+'.bin')).exists(): orphan.append(p.name); continue
    if ok(t):
        good.append(p.stem+'.bin')
        fam[next((v for k,v in FAM if k in t.splitlines()[0]),'other')]+=1
    else: bad.append(p.name)
(OUT/'RECOVERED_IDS.txt').write_text('\n'.join(good)+'\n')
gs=set(good)
census=json.load(open('/workspace/cypher/work/r10/census.json'))
def tag(r):
    tops=[p for p,_ in r['reach'] if len(p)<=4]
    first=r['reach'][0][0] if r['reach'] else ''
    if not r['reach']: return 'opaque'
    for k in ('WLN','WVC'):
        if any(p.startswith(k) for p,_ in r['reach']): return {'WLN':'WLN1','WVC':'WVC'}[k]
    if first.startswith('WNM') or first in('NA',) or any(p=='WNM' for p,_ in r['reach']): return 'WNM'
    if any(p=='WNC' for p,_ in r['reach']): return 'WNC'
    if any(p in('A','BA') for p,_ in r['reach']): return 'WRA1'
    if any(p in('BWNC',) for p,_ in r['reach']): return 'WNC'
    if any(p in('BWNM',) for p,_ in r['reach']): return 'WNM'
    return 'other'
before=Counter(tag(r) for r in census)
after=Counter(tag(r) for r in census if r['id'] not in gs)
res={'validated_count':len(good),'bad':bad,'orphans':orphan,'families':dict(fam),
     'unrecovered_by_tag_before_r10':dict(before),'unrecovered_by_tag_after':dict(after)}
print(json.dumps(res,indent=1))
json.dump(res,open('/workspace/cypher/work/r10/validate_out.json','w'),indent=1)
