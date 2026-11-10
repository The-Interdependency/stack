#!/usr/bin/env python3
"""Synthetic fixtures via public transport_cases.run + random corpora.

These are not challenge files.  A solver must recover the planted message
and report it unique when the model pins the hex id.
"""
import os, random, sys, time
sys.path[:0] = ['/workspace/cypher/work/r12', '/workspace/cypher/work/r10']
import wln_dp as D
import wln_coupled as W

def plant(sched, n_init=1, t=3, rot=0, ar=3, seed=7):
    random.seed(seed)
    msg = W.PREFIX + bytes(random.choice(b'0123456789abcdef') for _ in range(32)) + W.TEMPLATE[W.HEXHI:]
    p = {
        'initial_lanes': n_init, 'thread_count': t, 'lane_rotation': rot, 'inter_arity': ar,
        'corpus_hex': random.randbytes(256).hex(), 'corpus_bit_offset': random.randrange(8192),
    }
    wire = W.tc.run(msg, list(sched), p)
    st = W.tc.decode_lanes(wire)
    wl = [list(l) for l in st.lanes]
    return msg, wl, p

def test_one(sched, n=1, t=3, rot=0, ar=3, seed=7, expect_unique=True):
    msg, wl, p = plant(sched, n, t, rot, ar, seed)
    L = D.layouts_any(sched, n, t, rot, ar)
    assert L, f'layout failed {sched}'
    u, v, final = L
    assert tuple(final) == tuple(map(len, wl))
    z = D.wire_z(wl, v, u)
    t0 = time.time()
    status, rec = D.recover(z, u)
    dt = time.time() - t0
    match = rec == msg if rec is not None else False
    print(f'1C {"".join(sched):10} seed={seed} m={len(u)} status={status:10} match={match} secs={dt:.3f}', flush=True)
    if expect_unique:
        assert status == 'unique' and match, (status, match, rec, msg)
    return status, match

def main():
    # The seed-7 XC case that exhausted 3M-step DFS in both solvers.
    test_one(('X', 'C'), t=3, seed=7)
    test_one(('X', 'C'), t=3, seed=1)
    test_one(('X', 'C'), t=5, seed=7)
    test_one(('X', 'C'), t=7, seed=3)
    # original coupled synthetic
    # single-lane C: model is underdetermined (Round 8). Must not claim unique.
    st, m = test_one(('C',), seed=7, expect_unique=False)
    print('  single-lane C expected non-unique/ambiguous:', st, flush=True)
    assert st in ('ambiguous', 'none') or (st == 'unique' and m)
    # compare DP vs DFS on a lucky seed where DFS finishes
    msg, wl, p = plant(('X', 'C'), t=3, seed=1)
    u, v, final = W.layouts(('X', 'C'), 1, 3, 0, 3)
    sols, steps = W.solve(wl, u, v, maxsol=3, budget=2_000_000)
    print('DFS seed1 nsol', len(sols), 'steps', steps, 'match', [x == msg for x in sols], flush=True)
    print('ALL 1C SYNTH TESTS PASSED', flush=True)

if __name__ == '__main__':
    main()
