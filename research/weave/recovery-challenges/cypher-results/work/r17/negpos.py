import sys, time, json, random
sys.path[:0] = ['/workspace/cypher/work/r13', '/workspace/cypher/work/r12', '/workspace/cypher/work/r10']
import wln_sat as S, wln_coupled as W
from test_multi_synth import plant
from pysat.solvers import Cadical153
mode, t, seed, tl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
msg, wl, p = plant(('X','C','C'), t, seed)
bits = [(b >> (7-k)) & 1 for b in msg for k in range(8)]
if mode.startswith('flip'):
    k = int(mode[4:]); rng = random.Random(1000+seed)
    flat = [(i, j) for i, l in enumerate(wl) for j in range(len(l))]
    for i, j in rng.sample(flat, k): wl[i][j] ^= 1
elif mode == 'rand':
    rng = random.Random(2000+seed); wl = [[rng.randrange(2) for _ in l] for l in wl]
t0 = time.time()
if mode == 'truth':
    e, x, hexv = S.build(('X','C','C'), 1, t, 0, 3, wl)
    cl = e.cl + [[v if b else -v] for v, b in zip(x, bits)]
    sv = Cadical153(bootstrap_with=cl)
    import threading
    tm = threading.Timer(tl, sv.interrupt); tm.start()
    r = sv.solve_limited(expect_interrupt=True); tm.cancel()
    st = {True: 'sat_truth_admitted', False: 'UNSAT_truth_excluded', None: 'timeout'}[r]; ok = None
else:
    st, rec = S.solve(('X','C','C'), 1, t, 0, 3, wl)
    ok = (rec == msg) if rec is not None else None
print(json.dumps({'mode': mode, 't': t, 'seed': seed, 'status': st, 'rec_eq_planted': ok, 'secs': round(time.time()-t0, 1)}), flush=True)
