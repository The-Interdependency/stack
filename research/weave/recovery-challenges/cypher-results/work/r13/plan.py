import sys, json
sys.path[:0] = ['/workspace/cypher/work/r13','/workspace/cypher/work/r12','/workspace/cypher/work/r10']
import wln_coupled as W, run_1c as R
from collections import defaultdict
acc,_ = W.matrix.transport_schedules()
cands = []
for s,n in acc:
    if s.count('C') < 2: continue
    for t in ((3,5,7) if 'X' in s else (3,)):
        for rot in (range(7) if 'J' in s else (0,)):
            for ar in ((3,5,7) if 'I' in s else (3,)):
                p = dict(W.DUMMY, initial_lanes=n, thread_count=t, lane_rotation=rot, inter_arity=ar)
                lens = W.tc.initial_lengths(W.NB, n); ok = True
                try:
                    # lane count at each C
                    from itertools import accumulate
                    ctxs, final = W.tc.contexts(W.NB, list(s), p)
                    L = len(lens)
                    for op, c in zip(s, ctxs):
                        if op == 'C' and L < 3: ok = False
                        if op == 'X': L = t
                        if op == 'J': L = 1
                except Exception: continue
                if ok: cands.append(((''.join(s)), n, t, rot, ar, tuple(final)))
by = defaultdict(list)
for c in cands: by[c[5]].append(c[:5])
rem = R.remaining()
jobs = []
for f in rem:
    wl = [list(l) for l in W.tc.decode_lanes(f.read_bytes()).lanes]
    for c in by.get(tuple(map(len, wl)), []): jobs.append((f.name,) + c)
print(len(cands), len(rem), len(jobs))
from collections import Counter; print(Counter(j[1] for j in jobs).most_common(20))
json.dump(jobs, open('jobs.json','w'))
