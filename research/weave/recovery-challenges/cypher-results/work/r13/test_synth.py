import sys, time
sys.path[:0] = ['/workspace/cypher/work/r13', '/workspace/cypher/work/r12', '/workspace/cypher/work/r10']
import wln_sat as S
from test_multi_synth import plant
for sched, t, seed in [(('X','C'),3,7), (('C','C'),3,7), (('X','C','C'),3,7), (('C','X','C'),3,7), (('C','C','C'),3,7), (('X','C','C'),5,1)]:
    msg, wl, p = plant(sched, t, seed)
    t0 = time.time()
    st, rec = S.solve(sched, 1, t, 0, 3, wl)
    print(''.join(sched), t, seed, st, rec == msg, f'{time.time()-t0:.1f}s', flush=True)
