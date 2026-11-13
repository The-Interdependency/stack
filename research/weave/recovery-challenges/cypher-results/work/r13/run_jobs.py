import sys, json, time
sys.path[:0] = ['/workspace/cypher/work/r13','/workspace/cypher/work/r10']
import wln_sat as S, wln_coupled as W
from pathlib import Path
jobs = json.load(open(sys.argv[1])); tl = float(sys.argv[2]); out = open(sys.argv[3], 'a')
for f, s, n, t, rot, ar in jobs:
    wl = [list(l) for l in W.tc.decode_lanes(Path('/workspace/cypher/v2/blind/files', f).read_bytes()).lanes]
    t0 = time.time()
    st, msg = S.solve(tuple(s), n, t, rot, ar, wl, tlimit=tl)
    out.write(json.dumps({'file': f, 'sched': s, 'n': n, 't': t, 'rot': rot, 'ar': ar, 'status': st,
        'msg': msg.decode('latin1') if msg else None, 'secs': round(time.time()-t0, 1)}) + '\n'); out.flush()
