#!/usr/bin/env python3
# Round 10 census: classify unrecovered v2 files after cheap public peels (B, N-extract, U-restore)
import sys, json, importlib.util
from pathlib import Path
from collections import Counter
sys.path.insert(0,'/workspace/cypher/src')
spec=importlib.util.spec_from_file_location('asm','/workspace/cypher/work/crack_v2_Asmall.py')
asm=importlib.util.module_from_spec(spec); spec.loader.exec_module(asm)
ROOT=Path('/workspace/cypher/v2/blind/files'); OUT=Path('/workspace/cypher/work/v2_recovered')
rec=set(OUT.joinpath('RECOVERED_IDS.txt').read_text().split())
def peels(d):
    res=[]
    if d.startswith(b'WNM\x01'):
        try: res.append(asm.do_B(d) if False else None)
        except: pass
        L=int.from_bytes(d[4:12],'big')
        if 1<=L<=len(d)-44: res.append(d[44:44+L])
    if d.startswith(b'WNC\x01'):
        try: res.append(asm.decode_numeral(d).restore().to_bytes())
        except: pass
    return [x for x in res if x]
rows=[]
for p in sorted(ROOT.glob('*.bin')):
    if p.name in rec: continue
    raw=p.read_bytes()
    chain=[]; frontier=[(raw,'')]; seen=set(); was=[]
    while frontier:
        d,path=frontier.pop()
        if d in seen or len(path)>8: continue
        seen.add(d)
        tag=d[:4]
        if tag.startswith(b'WRA1'):
            try: src=asm.parse(d[36:])[0]
            except Exception: src=-1
            was.append((path+'A',src))
        elif tag in (b'WNM\x01',b'WNC\x01') or tag.startswith(b'WLN1') or tag.startswith(b'WVC'):
            was.append((path+tag[:3].decode(errors='replace'),None))
        for n in peels(d): frontier.append((n,path+('N' if tag==b'WNM\x01' else 'U')))
        if path=='' : frontier.append((asm.do_B(d),'B'))
    rows.append({'id':p.name,'len':len(raw),'reach':was})
json.dump(rows,open('census.json','w'))
c=Counter()
srcs=[]
for r in rows:
    a=[s for pth,s in r['reach'] if pth.endswith('A')]
    if a: srcs.append(max(a))
    c[tuple(sorted(set(pth for pth,_ in r['reach'])))[:3]]+=1
print(len(rows))
for k,v in c.most_common(30): print(v,k)
import statistics
srcs.sort(); print('WRA1-reachable',len(srcs), 'src quantiles', [srcs[int(len(srcs)*q)] for q in (0,.25,.5,.75,.99)] if srcs else None)
print('src<=2500',sum(1 for s in srcs if 0<s<=2500),'<=4000',sum(1 for s in srcs if 0<s<=4000))
