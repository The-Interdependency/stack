#!/usr/bin/env python3
"""Multi-C existence check + hex search (public transport_cases model).

Extends wln_multiC's waiter tracing with:
  - optional forced plaintext bits (hex digits under test)
  - local unit propagation (skip a window bit that immediately contradicts)
  - stop at the first accepting window (existence, not enumeration)
  - timeout returns 'unknown' rather than 'no' so we do not reject a
    valid hex digit because the search ran out of budget

Synthetic tests must pass before this is applied to challenge files.
"""
from __future__ import annotations
import sys
sys.path[:0] = ['/workspace/cypher/work/r12', '/workspace/cypher/work/r10']
import wln_dp as D
import wln_multiC as M
import wln_coupled as W


def exists_1c(z, u, force=None, budget=None):
    return D._exists(z, u, force=force)


def exists_multi(stages, final_lab, wire, force=None, budget=3_000_000):
    """Return True, False, or None (unknown/timeout)."""
    KB = list(W.KB)
    if force:
        for i, b in force.items():
            KB[i] = b
    q = len(stages)
    if q == 1:
        # Build z,u from stages/final_lab — caller should use exists_1c.
        pass
    R = [[[None] * n for n in st['sizes']] for st in stages]
    lo = [[0] * len(st['sizes']) for st in stages]
    hi = [[n - 1 for n in st['sizes']] for st in stages]
    waiters = {}
    T = max(k + n for st in stages for k, n in enumerate(st['sizes']))

    def trace(lab):
        while True:
            a, k, i = lab
            p = R[a][k][i]
            if p is None:
                return ('wait', lab)
            kind, tab = stages[a]['src']
            v = tab[k][p]
            if kind == 'pt':
                return ('pt', v)
            lab = v

    assign = {}

    def check(lab, want, undo):
        r = trace(lab)
        if r[0] == 'wait':
            waiters.setdefault(r[1], []).append((lab, want))
            undo.append(('w', r[1]))
            return True
        idx = r[1]
        kb = KB[idx]
        if kb is None:
            if idx in assign:
                return assign[idx] == want
            assign[idx] = want
            undo.append(('a', idx))
            return True
        return kb == want

    def rollback(undo):
        for kind, x in reversed(undo):
            if kind == 'a':
                del assign[x]
            elif kind == 'w':
                waiters[x].pop()
            elif kind == 'r':
                a, k, i, wb = x
                R[a][k][i] = None
                if wb:
                    hi[a][k] += 1
                else:
                    lo[a][k] -= 1
            elif kind == 'W':
                waiters[x[0]] = x[1]

    root = []
    for f, lane in enumerate(final_lab):
        for j, lab in enumerate(lane):
            if not check(lab, wire[f][j], root):
                return False

    steps = [0]
    found = [False]

    def apply(t, wb):
        undo = []
        for a, st in enumerate(stages):
            m = len(st['sizes'])
            for k in range(m):
                i = t - k
                if not 0 <= i < st['sizes'][k]:
                    continue
                pos = hi[a][k] if wb else lo[a][k]
                if lo[a][k] > hi[a][k]:
                    rollback(undo)
                    return None
                R[a][k][i] = pos
                if wb:
                    hi[a][k] -= 1
                else:
                    lo[a][k] += 1
                undo.append(('r', (a, k, i, wb)))
                key = (a, k, i)
                ws = waiters.get(key)
                if ws:
                    waiters[key] = []
                    undo.append(('W', (key, ws)))
                    for lab, want in ws:
                        if not check(lab, want, undo):
                            rollback(undo)
                            return None
        return undo

    def rec(t):
        if found[0]:
            return
        steps[0] += 1
        if steps[0] > budget:
            return
        if t == T:
            found[0] = True
            return
        options = []
        for wb in (0, 1):
            undo = apply(t, wb)
            if undo is not None:
                options.append((wb, undo))
                rollback(undo)
        # try unique option first; if both work, try 0 then 1
        if len(options) == 1:
            wb, _ = options[0]
            undo = apply(t, wb)
            rec(t + 1)
            rollback(undo)
        elif len(options) == 2:
            for wb, _ in options:
                if found[0] or steps[0] > budget:
                    return
                undo = apply(t, wb)
                rec(t + 1)
                rollback(undo)

    rec(0)
    if found[0]:
        return True
    if steps[0] > budget:
        return None
    return False


def recover_hex(stages, final_lab, wire, budget=3_000_000):
    ex = exists_multi(stages, final_lab, wire, None, budget)
    if ex is False:
        return 'none', None
    if ex is None:
        return 'timeout', None

    def search(force, bi, left):
        if left[0] <= 0:
            return ['BUDGET']
        if bi >= W.HEXHI:
            bits = [W.KB[i] if W.KB[i] is not None else force.get(i) for i in range(W.NB)]
            if None in bits:
                return []
            return [D._pack(bits)]
        msgs = []
        for ch in W.HEXS:
            extra = D._force_char(bi, ch)
            if extra is None:
                continue
            merged = dict(force)
            clash = False
            for k, v in extra.items():
                if k in merged and merged[k] != v:
                    clash = True
                    break
                merged[k] = v
            if clash:
                continue
            left[0] -= 1
            r = exists_multi(stages, final_lab, wire, merged, budget)
            if r is None:
                return ['BUDGET']
            if r is False:
                continue
            more = search(merged, bi + 1, left)
            if more == ['BUDGET']:
                return more
            msgs.extend(more)
            if len(msgs) >= 2:
                return msgs[:2]
        return msgs

    msgs = search({}, W.HEXLO, [8000])
    if msgs == ['BUDGET']:
        return 'timeout', None
    msgs = [m for m in msgs if all(c in W.HEXS for c in m[W.HEXLO:W.HEXHI])]
    if not msgs:
        return 'none', None
    if len(set(msgs)) == 1:
        return 'unique', msgs[0]
    return 'ambiguous', None
