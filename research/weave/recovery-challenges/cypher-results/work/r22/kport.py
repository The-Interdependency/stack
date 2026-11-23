# Round 21: kissat404 (pysat) planted XCCC tests. Based on r20/portfolio2.py + r18/negpos4.py modes.
# Modes: truth (truth admission), rand (random-wire negative), pos (full planted recovery + uniqueness check).
# Records wall, monotonic and process CPU seconds separately (r18-r20 wall figures included box pauses).
import sys, time, json, random, resource
sys.path[:0] = ['/workspace/cypher/work/r13', '/workspace/cypher/work/r12', '/workspace/cypher/work/r10']
import wln_sat as S, wln_coupled as W
from test_multi_synth import plant
from pysat.solvers import Solver
mode, t, seed, sched, sname = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), tuple(sys.argv[4]), sys.argv[5]
msg, wl, p = plant(sched, t, seed)
bits = [(b >> (7-k)) & 1 for b in msg for k in range(8)]
if mode == 'rand':
    rng = random.Random(2000+seed); wl = [[rng.randrange(2) for _ in l] for l in wl]
w0, m0 = time.time(), time.monotonic()
e, x, hexv = S.build(sched, 1, t, 0, 3, wl)
cl = list(e.cl)
if mode == 'truth':
    cl += [[v if b else -v] for v, b in zip(x, bits)]
sv = Solver(name=sname, bootstrap_with=cl)
r = sv.solve(); ok = None; st = None
if mode == 'truth':
    st = {True: 'sat_truth_admitted', False: 'UNSAT_truth_excluded'}[r]
elif not r:
    st = 'none'
else:
    m = set(l for l in sv.get_model() if l > 0)
    rb = [1 if v in m else 0 for v in x]
    rec = bytes(sum(rb[8*i+k] << (7-k) for k in range(8)) for i in range(len(rb)//8))
    ok = (rec == msg)
    sv.add_clause([-v if v in m else v for v in hexv])
    st = 'ambiguous' if sv.solve() else 'unique'
ru = resource.getrusage(resource.RUSAGE_SELF)
print(json.dumps({'mode': mode, 't': t, 'seed': seed, 'sched': ''.join(sched), 'solver': sname, 'clauses': len(cl), 'status': st, 'rec_eq_planted': ok,
  'wall': round(time.time()-w0, 1), 'mono': round(time.monotonic()-m0, 1), 'cpu': round(ru.ru_utime+ru.ru_stime, 1)}), flush=True)
