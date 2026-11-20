# Round 21: real XCCC files with kissat404 (pysat), schedule params from r15/xccc_args.txt.
# Planted prerequisite: r21 kport2 pos t=7 seed 3 recovered the planted message (first XCCC planted recovery).
# On SAT: extract message + corpus window, forward re-encode with PUBLIC transport_cases.run (as r15/forward_check.py), compare all lanes.
# 'none' here is NOT an elimination until kissat passes planted negatives at this t. No uniqueness check in this pass.
import sys, json, time
sys.path[:0] = ['/workspace/cypher/work/r15', '/workspace/cypher/work/r13', '/workspace/cypher/work/r10']
import wln_sat2 as S, wln_coupled as W
from pysat.solvers import Solver
from pathlib import Path
f, s, n, t, rot, ar = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
wl = [list(l) for l in W.tc.decode_lanes(Path('/workspace/cypher/v2/blind/files', f).read_bytes()).lanes]
m0 = time.monotonic()
b = S.build(tuple(s), n, t, rot, ar, wl)
if b is None:
    print(json.dumps({'file': f, 'status': 'shape'})); sys.exit()
e, x, hexv = b
sv = Solver(name='kissat404', bootstrap_with=e.cl)
r = sv.solve()
res = {'file': f, 'sched': s, 'n': n, 't': t, 'rot': rot, 'ar': ar, 'solver': 'kissat404', 'mono': round(time.monotonic()-m0, 1)}
if not r:
    res['status'] = 'none_UNCONFIRMED'
else:
    m = set(l for l in sv.get_model() if l > 0)
    bits = [1 if v in m else 0 for v in x]
    msg = bytes(sum(bits[8*i+k] << (7-k) for k in range(8)) for i in range(len(bits)//8))
    L = max(e.Wv) + 1
    wb = [1 if e.Wv.get(i) in m else 0 for i in range(L)]
    wb += [0] * (-len(wb) % 8) + [0] * 64
    corpus = bytes(sum(wb[8*i+k] << (7-k) for k in range(8)) for i in range(len(wb)//8))
    p = dict(W.DUMMY, initial_lanes=n, thread_count=t, lane_rotation=rot, inter_arity=ar, corpus_hex=corpus.hex(), corpus_bit_offset=0)
    out = [list(l) for l in W.tc.decode_lanes(W.tc.run(msg, list(s), p)).lanes]
    Path('/workspace/cypher/work/r21/cand').mkdir(exist_ok=True)
    Path('/workspace/cypher/work/r21/cand', f + '.' + s + '.msg').write_bytes(msg)
    res.update(status='sat', lanes_equal=(out == wl), window_bits=L, msg=msg.decode('latin1'))
print(json.dumps(res), flush=True)
