#!/usr/bin/env python3
import random, sys, time
sys.path[:0] = ['/workspace/cypher/work/r12', '/workspace/cypher/work/r10']
import wln_multi as X
import wln_multiC as M
import wln_coupled as W

def plant(sched, t=3, seed=7):
    random.seed(seed)
    msg = W.PREFIX + bytes(random.choice(b'0123456789abcdef') for _ in range(32)) + W.TEMPLATE[W.HEXHI:]
    p = {'initial_lanes': 1, 'thread_count': t, 'lane_rotation': 0, 'inter_arity': 3,
         'corpus_hex': random.randbytes(256).hex(), 'corpus_bit_offset': random.randrange(8192)}
    wire = W.tc.run(msg, list(sched), p)
    st = W.tc.decode_lanes(wire)
    wl = [list(l) for l in st.lanes]
    return msg, wl, p

def test(sched, t=3, seed=7, budget=3_000_000):
    msg, wl, p = plant(sched, t, seed)
    built = M.build(sched, 1, t, 0, 3)
    assert built, sched
    stages, fl, final = built
    t0 = time.time()
    ex = X.exists_multi(stages, fl, wl, None, budget)
    dt = time.time() - t0
    print(f'exists {"".join(sched):8} t={t} seed={seed} -> {ex} secs={dt:.3f}', flush=True)
    t0 = time.time()
    status, rec = X.recover_hex(stages, fl, wl, budget)
    dt = time.time() - t0
    match = rec == msg if rec is not None else False
    print(f'recover {"".join(sched):8} status={status:10} match={match} secs={dt:.3f}', flush=True)
    return ex, status, match

def main():
    # 1-C XC seed 7: exists should be True via waiter+unitprop or we can skip
    # Multi-C plants
    cases = [
        (('C', 'C'), 3, 7),
        (('C', 'C', 'C'), 3, 7),
        (('X', 'C', 'C'), 3, 7),
        (('C', 'X', 'C'), 3, 7),
        (('X', 'C'), 3, 7),
    ]
    for s, t, seed in cases:
        test(s, t, seed)
    print('DONE', flush=True)

if __name__ == '__main__':
    main()
