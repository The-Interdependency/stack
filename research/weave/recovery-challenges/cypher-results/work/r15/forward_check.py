#!/usr/bin/env python3
"""Round 15: forward re-encode check for a multi-C SAT candidate.
Solve, extract the shared corpus window W from the model, then run the PUBLIC
transport_cases.run forward on the candidate message with a synthetic corpus
equal to W (offset 0) and compare every output lane bit to the challenge file.
Passing shows the candidate is an exact preimage under that schedule/params;
it does not prove it equals the excluded original."""
import sys, json
sys.path[:0] = ['/workspace/cypher/work/r15', '/workspace/cypher/work/r13', '/workspace/cypher/work/r10']
import wln_sat2 as S, wln_coupled as W
from pysat.solvers import Cadical153
from pathlib import Path
f, s, n, t, rot, ar = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
wl = [list(l) for l in W.tc.decode_lanes(Path('/workspace/cypher/v2/blind/files', f).read_bytes()).lanes]
e, x, hexv = S.build(tuple(s), n, t, rot, ar, wl)
sv = Cadical153(bootstrap_with=e.cl); assert sv.solve()
m = set(l for l in sv.get_model() if l > 0)
bits = [1 if v in m else 0 for v in x]
msg = bytes(sum(bits[8*i+k] << (7-k) for k in range(8)) for i in range(len(bits)//8))
L = max(e.Wv) + 1
wb = [1 if e.Wv.get(i) in m else 0 for i in range(L)]
wb += [0] * (-len(wb) % 8) + [0] * 64
corpus = bytes(sum(wb[8*i+k] << (7-k) for k in range(8)) for i in range(len(wb)//8))
p = dict(W.DUMMY, initial_lanes=n, thread_count=t, lane_rotation=rot, inter_arity=ar,
         corpus_hex=corpus.hex(), corpus_bit_offset=0)
out = [list(l) for l in W.tc.decode_lanes(W.tc.run(msg, list(s), p)).lanes]
print(json.dumps({'file': f, 'sched': s, 't': t, 'lanes_equal': out == wl,
                  'window_bits': L, 'msg': msg.decode('latin1')}))
