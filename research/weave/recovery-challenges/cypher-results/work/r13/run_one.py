import sys, json, time
sys.path[:0] = ['/workspace/cypher/work/r13','/workspace/cypher/work/r10']
import wln_sat as S, wln_coupled as W
from pathlib import Path
f, s, n, t, rot, ar = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
wl = [list(l) for l in W.tc.decode_lanes(Path('/workspace/cypher/v2/blind/files', f).read_bytes()).lanes]
t0 = time.time()
st, msg = S.solve(tuple(s), n, t, rot, ar, wl)
print(json.dumps({'file': f, 'sched': s, 'n': n, 't': t, 'rot': rot, 'ar': ar, 'status': st,
    'msg': msg.decode('latin1') if msg else None, 'secs': round(time.time()-t0, 1)}), flush=True)
