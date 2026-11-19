# Round 20b: like portfolio.py but falls back to plain solve() when solve_limited is unsupported (relies on SIGKILL cap). r18/negpos4.py with the SAT solver as 6th arg (pysat name), truth mode only. Planted tests only.
import sys, time, json, threading
sys.path[:0] = ['/workspace/cypher/work/r13', '/workspace/cypher/work/r12', '/workspace/cypher/work/r10']
import wln_sat as S, wln_coupled as W
from test_multi_synth import plant
from pysat.solvers import Solver
mode, t, seed, tl, sched, sname = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), tuple(sys.argv[5]), sys.argv[6]
assert mode == 'truth'
msg, wl, p = plant(sched, t, seed)
bits = [(b >> (7-k)) & 1 for b in msg for k in range(8)]
t0 = time.time()
e, x, hexv = S.build(sched, 1, t, 0, 3, wl)
cl = e.cl + [[v if b else -v] for v, b in zip(x, bits)]
nv = max(abs(l) for c in cl for l in c)
sv = Solver(name=sname, bootstrap_with=cl)
tm = threading.Timer(tl, sv.interrupt); tm.start()
try:
    r = sv.solve_limited(expect_interrupt=True)
except NotImplementedError:
    r = sv.solve()
tm.cancel()
st = {True: 'sat_truth_admitted', False: 'UNSAT_truth_excluded', None: 'timeout'}[r]
print(json.dumps({'mode': mode, 't': t, 'seed': seed, 'sched': ''.join(sched), 'solver': sname, 'vars': nv, 'clauses': len(cl), 'status': st, 'secs': round(time.time()-t0, 1)}), flush=True)
