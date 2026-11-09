import json,time,sys
sys.path.insert(0,'.')
from fastA import invert_A, asm
from pathlib import Path
rows=json.load(open('census.json'))
ROOT=Path('/workspace/cypher/v2/blind/files')
n=0;t0=time.time()
for r in rows:
    if r['reach'] and r['reach'][0][0]=='A':
        d=(ROOT/r['id']).read_bytes()
        t=time.time(); res=invert_A(d)
        pe=[asm.peel(x) for x in res]
        print(r['id'],r['reach'][0][1],len(res),[bool(x) for x in pe],round(time.time()-t,2),res[0][:12] if res else None,flush=True)
        n+=1
        if n>=15: break
