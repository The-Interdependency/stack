#!/usr/bin/env python3
"""Complete single-C search via DP on shared corpus-window prefixes.

The Round 10/11 DFS (wln_coupled.solve) is correct but can exceed a few million
steps when both deque ends stay compatible.  This DP explores the same model
exactly, with O(T * 2^{m-1}) states, and checks message uniqueness by asking
whether any wildcard plaintext bit can take the opposite value on another
accepting window.

layouts_any is wln_coupled.layouts without the 'C must see >=3 lanes' filter,
so single-lane C schedules are included; they are almost always rejected by
the uniqueness check (same observation as Round 8's free L/R model).
"""
from __future__ import annotations
import sys
from collections import defaultdict
from pathlib import Path
sys.path[:0] = ['/workspace/cypher/work/r10', '/workspace/cypher/v2', '/workspace/cypher/src']
import wln_coupled as W

def layouts_any(sched, n_init, tcnt, rot, ar):
    p = dict(W.DUMMY, initial_lanes=n_init, thread_count=tcnt, lane_rotation=rot, inter_arity=ar)
    ctxs, final = W.tc.contexts(W.NB, sched, p)
    ci = [i for i, o in enumerate(sched) if o == 'C']
    if len(ci) != 1:
        return None
    c = ci[0]
    lens = W.tc.initial_lengths(W.NB, n_init)
    lanes, s = [], 0
    for n in lens:
        lanes.append(list(range(s, s + n)))
        s += n
    u = W.run_ops(lanes, sched[:c], ctxs[:c])
    post = [[(k, i) for i in range(len(l))] for k, l in enumerate(u)]
    v = W.run_ops(post, sched[c + 1:], ctxs[c + 1:])
    return u, v, final


def wire_z(wire_lanes, v, u):
    z = [[None] * len(l) for l in u]
    for fk, lane in enumerate(v):
        for j, (k, i) in enumerate(lane):
            z[k][i] = wire_lanes[fk][j]
    if any(x is None for row in z for x in row):
        raise ValueError('incomplete C-output coverage')
    return z


def _exists(z, u, force=None):
    """True iff some window prefix survives known-bit (and optional force) checks."""
    m = len(u)
    ns = [len(l) for l in u]
    T = max(ns[k] + k for k in range(m))
    KB = W.KB
    cur = {tuple(0 for _ in range(m))}
    for t in range(T):
        nxt = set()
        for los in cur:
            for wb in (0, 1):
                new = list(los)
                ok = True
                for k in range(m):
                    i = t - k
                    if not 0 <= i < ns[k]:
                        continue
                    lo = los[k]
                    hi = ns[k] - 1 - (i - lo)
                    if lo > hi:
                        ok = False
                        break
                    pos = hi if wb else lo
                    pbit = u[k][pos]
                    want = z[k][i]
                    kb = KB[pbit] if (force is None or pbit not in force) else force[pbit]
                    if kb is not None and kb != want:
                        ok = False
                        break
                    if not wb:
                        new[k] = lo + 1
                if ok:
                    nxt.add(tuple(new))
        if not nxt:
            return False
        cur = nxt
    return True


def _pack(bits):
    return bytes(sum(bits[8 * b + x] << (7 - x) for x in range(8)) for b in range(W.NB // 8))


def _force_char(bi, ch):
    """Bit force dict for TEMPLATE byte index bi = character ch, or None if it
    contradicts already-known template bits."""
    force = {}
    for s in range(8):
        idx = 8 * bi + s
        bit = (ch >> (7 - s)) & 1
        kb = W.KB[idx]
        if kb is not None:
            if kb != bit:
                return None
        else:
            force[idx] = bit
    return force


def _hex_search(z, u, force, start_bi, budget):
    """Search remaining hex bytes from start_bi. Return (msgs, budget)."""
    if budget[0] <= 0:
        return ['BUDGET'], budget
    if start_bi >= W.HEXHI:
        bits = [W.KB[i] if W.KB[i] is not None else force.get(i) for i in range(W.NB)]
        if None in bits:
            return [], budget
        return [_pack(bits)], budget
    # skip bytes already fully forced
    bi = start_bi
    valid = []
    for ch in W.HEXS:
        extra = _force_char(bi, ch)
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
        budget[0] -= 1
        if _exists(z, u, force=merged):
            valid.append((ch, merged))
    if not valid:
        return [], budget
    msgs = []
    for ch, merged in valid:
        more, budget = _hex_search(z, u, merged, bi + 1, budget)
        msgs.extend(more)
        if len(msgs) >= 2:
            return msgs[:2], budget
    return msgs, budget


def recover(z, u):
    """Return (status, msg_or_none).

    status is 'none', 'unique', or 'ambiguous'.  Accepting windows are filtered
    to those whose 32-byte id is hex (0-9a-f).
    """
    if not _exists(z, u):
        return 'none', None
    msgs, budget = _hex_search(z, u, {}, W.HEXLO, [20000])
    if 'BUDGET' in msgs:
        return 'ambiguous', None
    msgs = [m for m in msgs if all(c in W.HEXS for c in m[W.HEXLO:W.HEXHI])]
    if not msgs:
        return 'none', None
    uniq = set(msgs)
    if len(uniq) == 1:
        return 'unique', next(iter(uniq))
    return 'ambiguous', None


def candidates_1c():
    acc, _ = W.matrix.transport_schedules()
    out = []
    for s, n in acc:
        if s.count('C') != 1:
            continue
        for tcnt in ((3, 5, 7) if 'X' in s else (3,)):
            for rot in (range(7) if 'J' in s else (0,)):
                for ar in ((3, 5, 7) if 'I' in s else (3,)):
                    out.append((s, n, tcnt, rot, ar))
    return out


def precompute_layouts(cands):
    by_final = defaultdict(list)
    for c in cands:
        try:
            L = layouts_any(*c)
        except Exception:
            continue
        if not L:
            continue
        u, v, final = L
        by_final[tuple(final)].append((c, u, v))
    return by_final


def recover_file(wire_lanes, layouts):
    """Try every layout of matching shape. Return dict."""
    shape = tuple(map(len, wire_lanes))
    hits = []
    msgs = set()
    for c, u, v in layouts:
        try:
            z = wire_z(wire_lanes, v, u)
        except Exception:
            continue
        status, msg = recover(z, u)
        if status == 'none':
            continue
        rec = {
            'sched': ''.join(c[0]),
            'init': c[1], 't': c[2], 'rot': c[3], 'ar': c[4],
            'm': len(u), 'status': status,
            'msg': None if msg is None else msg.decode(),
        }
        hits.append(rec)
        if msg is not None and status == 'unique':
            msgs.add(msg)
        elif status == 'ambiguous':
            # do not add to unique set
            pass
    unique_msgs = {h['msg'] for h in hits if h['status'] == 'unique'}
    if len(unique_msgs) == 1 and not any(h['status'] == 'ambiguous' and h['msg'] != next(iter(unique_msgs)) for h in hits):
        # Accept only if every successful unique layout agrees, and any
        # ambiguous layout is ignored if we already have a unique one? Safer:
        # if ANY layout is unique and all unique layouts agree, AND there is
        # no ambiguous layout that produced a *different* reconstructed msg.
        # If there's an ambiguous layout, uniqueness across the model is not
        # guaranteed — treat as ambiguous unless the ambiguous traceback
        # equals the unique msg (other windows may still differ).
        # Conservative: require at least one unique and no ambiguous.
        pass
    verdict = 'none'
    chosen = None
    uniq = [h for h in hits if h['status'] == 'unique']
    ambi = [h for h in hits if h['status'] == 'ambiguous']
    umsgs = {h['msg'] for h in uniq}
    if len(umsgs) == 1 and not ambi:
        verdict = 'unique'
        chosen = next(iter(umsgs))
    elif len(umsgs) > 1:
        verdict = 'ambiguous'
    elif len(umsgs) == 1 and ambi:
        # unique under some params, ambiguous under others: not accepted
        verdict = 'mixed'
        chosen = next(iter(umsgs))
    elif not umsgs and ambi:
        verdict = 'ambiguous'
    return {'shape': shape, 'verdict': verdict, 'msg': chosen, 'hits': hits}


if __name__ == '__main__':
    import json, time
    files = sys.argv[1:]
    print('precomputing 1C layouts', flush=True)
    by = precompute_layouts(candidates_1c())
    print('shapes', {str(k): len(v) for k, v in by.items() if sum(k) == W.NB or True and len(v) and isinstance(k[0], int)}, flush=True)
    print('n shapes', len(by), 'total layouts', sum(len(v) for v in by.values()), flush=True)
    for f in files:
        data = Path(f).read_bytes()
        st = W.tc.decode_lanes(data)
        wl = [list(l) for l in st.lanes]
        shape = tuple(map(len, wl))
        t0 = time.time()
        res = recover_file(wl, by.get(shape, []))
        res['file'] = Path(f).name
        res['secs'] = round(time.time() - t0, 3)
        # shrink hit list in stdout
        print(json.dumps({k: res[k] for k in ('file', 'shape', 'verdict', 'msg', 'secs')} | {'nhits': len(res['hits'])}), flush=True)
