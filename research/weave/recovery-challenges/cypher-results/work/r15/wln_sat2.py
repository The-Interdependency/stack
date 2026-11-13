#!/usr/bin/env python3
"""Round 13: CNF encoding of multi-C WLN1 transport (public transport_cases).

Every C stage uses corpus offsets (offset+lane) for its lanes, so ALL C stages
read one shared window W (relative to the unknown offset). Unknowns: W bits and
the 192 free hex-id plaintext bits. X/J/I/W are public permutations, pushed
through the public forward code with SAT variable ids as labels. Each C lane is
a deque route encoded with one-hot left-count variables. Cyclic corpus wrap is
ignored (a relaxation: can only add solutions, never remove the true one).
Hex chars constrained to 0-9a-f. Uniqueness via a blocking clause on hex bits.
"""
import sys, time
sys.path[:0] = ['/workspace/cypher/work/r10', '/workspace/cypher/v2', '/workspace/cypher/src']
import wln_coupled as W
from stages.api import Streams
from pysat.solvers import Cadical153

class Enc:
    def __init__(s):
        s.n = 0; s.cl = []
    def new(s):
        s.n += 1; return s.n

def build(sched, n_init, tcnt, rot, ar, wire_lanes):
    p = dict(W.DUMMY, initial_lanes=n_init, thread_count=tcnt, lane_rotation=rot, inter_arity=ar)
    ctxs, final = W.tc.contexts(W.NB, list(sched), p)
    if tuple(final) != tuple(map(len, wire_lanes)):
        return None
    e = Enc()
    x = [e.new() for _ in range(W.NB)]
    for i, kb in enumerate(W.KB):
        if kb is not None:
            e.cl.append([x[i] if kb else -x[i]])
    # hex chars 0-9a-f
    for bi in range(W.HEXLO, W.HEXHI):
        bv = x[8 * bi:8 * bi + 8]
        allowed = set(b'0123456789abcdef')
        for v in range(256):
            if v & 0x80 or not v & 0x20 or v in allowed:
                continue
            e.cl.append([-bv[s] if (v >> (7 - s)) & 1 else bv[s] for s in range(8)])
    lens = W.tc.initial_lengths(W.NB, n_init)
    lanes, s0 = [], 0
    for n in lens:
        lanes.append(x[s0:s0 + n]); s0 += n
    Wv = {}
    def wbit(i):
        if i not in Wv:
            Wv[i] = e.new()
        return Wv[i]
    for op, ctx in zip(sched, ctxs):
        if op != 'C':
            lanes = W.run_ops(lanes, [op], [ctx]); continue
        out = []
        for k, inp in enumerate(lanes):
            n = len(inp)
            y = [e.new() for _ in range(n)]
            c = [[e.new() for _ in range(t + 1)] for t in range(n)]
            e.cl.append([c[0][0]])
            for t in range(n):
                r = wbit(k + t)
                e.cl.append(c[t])  # some count holds
                for j in range(t + 1):
                    cj = c[t][j]
                    a, b = inp[j], inp[n - 1 - (t - j)]
                    e.cl += [[-cj, r, -y[t], a], [-cj, r, y[t], -a],
                             [-cj, -r, -y[t], b], [-cj, -r, y[t], -b]]
                    if t + 1 < n:
                        e.cl += [[-cj, -r, c[t + 1][j]], [-cj, r, c[t + 1][j + 1]]]
                if t + 1 < n:
                    for j in range(t + 2):
                        cj = c[t + 1][j]
                        e.cl.append([-cj, r] + ([c[t][j - 1]] if j >= 1 else []))
                        e.cl.append([-cj, -r] + ([c[t][j]] if j <= t else []))
            out.append(y)
        lanes = out
    for lv, wl in zip(lanes, wire_lanes):
        for v, b in zip(lv, wl):
            e.cl.append([v if b else -v])
    hexv = x[8 * W.HEXLO:8 * W.HEXHI]
    e.Wv = Wv
    return e, x, hexv

def solve(sched, n_init, tcnt, rot, ar, wire_lanes, tlimit=None):
    b = build(sched, n_init, tcnt, rot, ar, wire_lanes)
    if b is None:
        return 'shape', None
    e, x, hexv = b
    S = Cadical153(bootstrap_with=e.cl)
    def go():
        if tlimit is None:
            return S.solve()
        import threading
        tm = threading.Timer(tlimit, S.interrupt); tm.start()
        r = S.solve_limited(expect_interrupt=True); tm.cancel(); S.clear_interrupt()
        return r
    r = go()
    if r is None:
        return 'timeout', None
    if not r:
        return 'none', None
    m = set(l for l in S.get_model() if l > 0)
    bits = [1 if v in m else 0 for v in x]
    msg = W._pack(bits) if hasattr(W, '_pack') else bytes(sum(bits[8*i+k] << (7-k) for k in range(8)) for i in range(W.NB // 8))
    S.add_clause([-v if v in m else v for v in hexv])
    r = go()
    if r is None:
        return 'timeout2', msg
    if r:
        return 'ambiguous', msg
    return 'unique', msg
