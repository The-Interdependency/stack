#!/usr/bin/env python3
"""C-bearing WLN1: known 141-byte template + contiguous-deque DP (remaining always [lo,hi])."""
from __future__ import annotations
import sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, '/workspace/cypher/src')
sys.path.insert(0, '/workspace/cypher/v2')
from stages import split, join, inter, whole
from stages.api import Streams, PublicContext
import matrix

OUT = Path('/workspace/cypher/work/v2_recovered')
ROOT = Path('/workspace/cypher/v2/blind/files')
KNOWN_LINE = 'my human needs my help'
PRED = 'I expect recovery after the lane rules and route controls are disclosed.'
PREFIX = b'Prediction '
HEX_START = len(PREFIX)  # 11
HEX_END = HEX_START + 32  # 43
MSG_LEN = 141
HEX_CHARS = set(b'0123456789abcdef')
TEMPLATE = PREFIX + b'0' * 32 + (': ' + PRED + '\n' + KNOWN_LINE + '\n').encode()
assert len(TEMPLATE) == MSG_LEN
NBITS = MSG_LEN * 8
HEX_BIT_LO = HEX_START * 8
HEX_BIT_HI = HEX_END * 8  # exclusive

def bits_of(data: bytes):
    return [(b >> s) & 1 for b in data for s in range(7, -1, -1)]

KNOWN_BITS = bits_of(TEMPLATE)
KNOWN_MASK = [not (HEX_BIT_LO <= i < HEX_BIT_HI) for i in range(NBITS)]

def pack_bits(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        v = 0
        for k in range(8):
            v = (v << 1) | bits[i + k]
        out.append(v)
    return bytes(out)

def ok_text(raw: bytes):
    if len(raw) != MSG_LEN or not raw.startswith(PREFIX):
        return None
    if raw[HEX_END:] != TEMPLATE[HEX_END:]:
        return None
    if any(raw[i] not in HEX_CHARS for i in range(HEX_START, HEX_END)):
        return None
    try:
        t = raw.decode('utf-8')
    except Exception:
        return None
    lines = t.splitlines()
    if len(lines) < 2 or lines[1] != KNOWN_LINE:
        return None
    if ': ' not in lines[0]:
        return None
    left, right = lines[0].split(': ', 1)
    if not left.startswith('Prediction '):
        return None
    hx = left[len('Prediction '):]
    if len(hx) != 32 or any(c not in '0123456789abcdef' for c in hx):
        return None
    if right != PRED:
        return None
    return t + ('\n' if not t.endswith('\n') else '')

def recover_c(wire):
    """wire[j] = msg[o[j]] for deque route o. Remaining always contiguous [lo,hi]."""
    n = len(wire)
    msg = [None] * n
    for i in range(n):
        if i < len(KNOWN_MASK) and KNOWN_MASK[i] and n == NBITS:
            msg[i] = KNOWN_BITS[i]
        elif n != NBITS and False:
            pass

    # General lane: if n != NBITS, known_mask only if caller seeded msg
    # Local helpers use msg as seeded

    def hex_byte_ok(idx):
        """If idx's byte fully assigned and in hex region, validate."""
        if n != NBITS:
            return True
        bi = idx // 8
        if not (HEX_START <= bi < HEX_END):
            return True
        base = bi * 8
        if any(msg[base + t] is None for t in range(8)):
            return True
        v = 0
        for t in range(8):
            v = (v << 1) | msg[base + t]
        return v in HEX_CHARS

    # DP for region entirely inside hex bits: state (lo, hi) with hi inclusive
    # When remaining ⊆ [HEX_BIT_LO, HEX_BIT_HI)
    from functools import lru_cache

    def assign_ok(idx, w):
        if msg[idx] is not None:
            return msg[idx] == w, False
        return True, True

    # Recursive with memo on (j, lo) for failure only when no writes to hex? 
    # Use explicit DFS; when [lo,hi] inside hex, call hex_dp.

    def hex_dp_fill(j, lo, hi):
        """Fill msg[lo..hi] from wire[j:] via deque; return True if hex valid.
        All positions lo..hi are in hex bit range; msg there currently None.
        """
        rem = hi - lo + 1
        assert rem == n - j
        # DP backward: can_complete[lo][hi] after assigning — actually forward DFS with memo (lo,hi,j) 
        # but j determined by rem: j = n - (hi-lo+1)
        @lru_cache(maxsize=None)
        def can(lo, hi):
            if lo > hi:
                return True
            jj = n - (hi - lo + 1)
            w = wire[jj]
            # take left
            msg[lo] = w
            ok_l = hex_byte_ok(lo) and can(lo + 1, hi)
            msg[lo] = None
            if ok_l:
                return True
            if lo == hi:
                return False
            msg[hi] = w
            ok_r = hex_byte_ok(hi) and can(lo, hi - 1)
            msg[hi] = None
            return ok_r

        # can() only checks; need to reconstruct one solution
        def build(lo, hi):
            if lo > hi:
                return True
            jj = n - (hi - lo + 1)
            w = wire[jj]
            msg[lo] = w
            if hex_byte_ok(lo) and (lo == hi or can(lo + 1, hi)) and build(lo + 1, hi):
                return True
            msg[lo] = None
            if lo == hi:
                return False
            msg[hi] = w
            if hex_byte_ok(hi) and can(lo, hi - 1) and build(lo, hi - 1):
                return True
            msg[hi] = None
            return False

        if not can(lo, hi):
            return False
        return build(lo, hi)

    def dfs(j, lo, hi):
        if j == n:
            return True
        # If remaining fully in hex region (and n==NBITS), switch to hex DP
        if n == NBITS and lo >= HEX_BIT_LO and hi < HEX_BIT_HI:
            return hex_dp_fill(j, lo, hi)
        w = wire[j]
        # try left
        ok, need_write = assign_ok(lo, w)
        if ok:
            old = msg[lo]
            if need_write:
                msg[lo] = w
            if hex_byte_ok(lo) and dfs(j + 1, lo + 1, hi):
                return True
            if need_write:
                msg[lo] = old
        if lo == hi:
            return False
        # try right
        ok, need_write = assign_ok(hi, w)
        if ok:
            old = msg[hi]
            if need_write:
                msg[hi] = w
            if hex_byte_ok(hi) and dfs(j + 1, lo, hi - 1):
                return True
            if need_write:
                msg[hi] = old
        return False

    if not dfs(0, 0, n - 1):
        return None
    if any(b is None for b in msg):
        return None
    return msg

def recover_c_seeded(wire, known_bits, known_mask):
    """Lane-sized recover with provided known mask (for multi-lane chunks)."""
    n = len(wire)
    msg = [known_bits[i] if known_mask[i] else None for i in range(n)]

    def hex_byte_ok(idx):
        return True  # chunk-local; validate at concat

    def assign_ok(idx, w):
        if msg[idx] is not None:
            return msg[idx] == w, False
        return True, True

    from functools import lru_cache
    # For partial lanes, hex may be split — use plain DFS with memo failure on (j,lo,hi) 
    # only when no None writes pending... keep simple DFS; lane sizes for initial>1 are ~376 bits
    fail = set()

    def dfs(j, lo, hi):
        if j == n:
            return True
        key = (j, lo, hi)
        if key in fail:
            return False
        w = wire[j]
        progressed = False
        for side, idx, nlo, nhi in ((0, lo, lo + 1, hi), (1, hi, lo, hi - 1)):
            if side == 1 and lo == hi:
                continue
            ok, need_write = assign_ok(idx, w)
            if not ok:
                continue
            old = msg[idx]
            if need_write:
                msg[idx] = w
            if dfs(j + 1, nlo, nhi):
                return True
            if need_write:
                msg[idx] = old
            progressed = True
        fail.add(key)
        return False

    if not dfs(0, 0, n - 1) or any(b is None for b in msg):
        return None
    return msg

# --- transport helpers ---
MODS = {'X': split, 'J': join, 'I': inter, 'W': whole}

def decode_lanes(data):
    if data[:4] != b'WLN1' or len(data) < 6:
        raise ValueError('WLN1')
    count = int.from_bytes(data[4:6], 'big')
    pos = 6
    lanes = []
    for _ in range(count):
        size = int.from_bytes(data[pos:pos + 4], 'big'); pos += 4
        width = (size + 7) // 8
        raw = data[pos:pos + width]; pos += width
        full = [(b >> s) & 1 for b in raw for s in range(7, -1, -1)]
        if any(full[size:]):
            raise ValueError('pad')
        lanes.append(tuple(full[:size]))
    if pos != len(data):
        raise ValueError('trail')
    return Streams(tuple(lanes))

def initial_lengths(size, count):
    q, r = divmod(size, count)
    return tuple(q + (i < r) for i in range(count))

def inv_ops(state, ops, size, initial, tc, lr, ia):
    if not ops:
        return state
    lengths = initial_lengths(size, initial)
    # We need lengths at the START of this ops sequence — caller must pass matching state.
    # Rebuild plans by simulating from a synthetic start: infer start lengths from final + inverse.
    # Simpler: simulate forward from given initial through ONLY these ops — but then start lengths
    # must be the lengths before ops. Pass start_lengths explicitly.
    raise NotImplementedError

def inv_ops_from(state, ops, start_lengths, size, tc, lr, ia):
    lengths = start_lengths
    plans = []
    for op in ops:
        params = {}
        if op == 'X':
            owners = split.cyclic_route(size, tc)
            params['split'] = (tc, owners)
            lengths = tuple(owners.count(i) for i in range(tc))
        elif op == 'J':
            r = lr % len(lengths)
            order = tuple(range(r, len(lengths))) + tuple(range(r))
            params['join'] = (lengths, order)
            lengths = (sum(lengths),)
        elif op == 'I':
            params['inter'] = tuple(inter.balanced_schedule(n, (ia,)) for n in lengths)
        elif op == 'W':
            if len(lengths) != 1:
                raise ValueError('W')
        else:
            raise ValueError(op)
        plans.append(PublicContext(None, parameters=params))
    if tuple(map(len, state.lanes)) != lengths:
        raise ValueError('final shape')
    for op, ctx in reversed(list(zip(ops, plans))):
        state = MODS[op].inverse(state, ctx)
    return state

def split_c(sched):
    idxs = [i for i, op in enumerate(sched) if op == 'C']
    return sched[:idxs[0]], sched[idxs[0]:idxs[-1] + 1], sched[idxs[-1] + 1:]

def traj_lengths(sched, size, initial, tc, lr):
    lengths = initial_lengths(size, initial)
    out = [lengths]
    for op in sched:
        if op == 'X':
            owners = split.cyclic_route(size, tc)
            lengths = tuple(owners.count(i) for i in range(tc))
        elif op == 'J':
            lengths = (sum(lengths),)
        out.append(lengths)
    return out  # out[i] = lengths BEFORE sched[i]; out[-1] = after all

def try_one(st0, sched, initial):
    pre, mid, suf = split_c(sched)
    if not all(x == 'C' for x in mid) or len(mid) != 1:
        return None
    size = sum(map(len, st0.lanes))
    if size != NBITS:
        return None
    tcs = [3, 5, 7] if 'X' in sched else [0]
    lrs = list(range(7)) if 'J' in sched else [0]
    ias = [3, 5, 7] if 'I' in sched else [0]
    for tc in tcs:
        for lr in lrs:
            for ia in ias:
                try:
                    traj = traj_lengths(sched, size, initial, tc, lr)
                    if traj[-1] != tuple(map(len, st0.lanes)):
                        continue
                    st = st0
                    if suf:
                        # lengths before suffix = traj[len(pre)+len(mid)]
                        start_len = traj[len(pre) + len(mid)]
                        # inv_ops_from expects start_lengths = lengths at beginning of forward suf
                        # and state at end. Rebuild: simulate suf forward plans from start_len
                        lengths = start_len
                        plans = []
                        for op in suf:
                            params = {}
                            if op == 'X':
                                owners = split.cyclic_route(size, tc)
                                params['split'] = (tc, owners)
                                lengths = tuple(owners.count(i) for i in range(tc))
                            elif op == 'J':
                                r = lr % len(lengths)
                                order = tuple(range(r, len(lengths))) + tuple(range(r))
                                params['join'] = (lengths, order)
                                lengths = (sum(lengths),)
                            elif op == 'I':
                                params['inter'] = tuple(inter.balanced_schedule(n, (ia,)) for n in lengths)
                            elif op == 'W':
                                if len(lengths) != 1:
                                    raise ValueError('W')
                            plans.append((op, PublicContext(None, parameters=params)))
                        if tuple(map(len, st.lanes)) != lengths:
                            continue
                        for op, ctx in reversed(plans):
                            st = MODS[op].inverse(st, ctx)
                    # st = after C, before suf; lengths = after pre (C preserves)
                    after_pre = traj[len(pre)]
                    if tuple(map(len, st.lanes)) != after_pre:
                        continue
                    if pre:
                        # C(prefix(msg)) — skip (no known bits on prefix output)
                        continue
                    # empty pre: recover C on each lane / single lane
                    if len(st.lanes) == 1:
                        got = recover_c(list(st.lanes[0]))
                        if got is None:
                            continue
                        raw = pack_bits(got)
                        t = ok_text(raw)
                        if t:
                            return t
                    else:
                        # multi-lane split of message then per-lane C
                        start = 0
                        chunks = []
                        good = True
                        for L in st.lanes:
                            ln = len(L)
                            kb = KNOWN_BITS[start:start + ln]
                            km = KNOWN_MASK[start:start + ln]
                            got = recover_c_seeded(list(L), kb, km)
                            if got is None:
                                good = False
                                break
                            chunks.append(got)
                            start += ln
                        if not good:
                            continue
                        flat = [b for ch in chunks for b in ch]
                        raw = pack_bits(flat)
                        t = ok_text(raw)
                        if t:
                            return t
                except Exception:
                    continue
    return None

def main():
    # unit check
    import secrets
    from collections import deque as dq

    def route(size, material, offset=0):
        remaining = dq(range(size))
        out = []
        for i in range(size):
            p = (offset + i) % (8 * len(material))
            right = (material[p // 8] >> (7 - p % 8)) & 1
            out.append(remaining.pop() if right else remaining.popleft())
        return tuple(out)

    msg = PREFIX + secrets.token_hex(16).encode() + (': ' + PRED + '\n' + KNOWN_LINE + '\n').encode()
    mb = bits_of(msg)
    o = route(len(mb), secrets.token_bytes(256), 99)
    wire = [mb[i] for i in o]
    got = recover_c(wire)
    raw = pack_bits(got) if got else None
    print('UNIT', raw == msg, flush=True)
    if raw != msg:
        return

    rec = set(Path(OUT / 'RECOVERED_IDS.txt').read_text().split())
    acc, _ = matrix.transport_schedules()
    scheds = []
    for s, n in acc:
        if 'C' not in s:
            continue
        pre, mid, suf = split_c(tuple(s))
        if all(x == 'C' for x in mid) and len(mid) == 1 and pre == ():
            scheds.append((tuple(s), n))
    print('schedules', len(scheds), flush=True)
    targets = [p for p in sorted(ROOT.glob('*.bin')) if p.name not in rec and p.read_bytes()[:4] == b'WLN1']
    print('targets', len(targets), flush=True)
    new = 0
    meth = Counter()
    for i, p in enumerate(targets):
        st0 = decode_lanes(p.read_bytes())
        hit = None
        used = None
        for sched, initial in scheds:
            t = try_one(st0, sched, initial)
            if t:
                hit = t if t.endswith('\n') else t + '\n'
                used = '/'.join(sched) + f'|i{initial}'
                break
        if hit:
            (OUT / (p.stem + '.txt')).write_text(hit)
            new += 1
            meth[used] += 1
            print('GOT', p.name, used, flush=True)
        if (i + 1) % 25 == 0:
            print(f'…{i+1}/{len(targets)} new={new}', flush=True)
    ids = sorted(x.stem + '.bin' for x in OUT.glob('*.txt') if x.name != 'RECOVERED_IDS.txt')
    Path(OUT / 'RECOVERED_IDS.txt').write_text('\n'.join(ids) + '\n')
    print('new', new, 'total', len(ids))
    print(meth.most_common(30))

if __name__ == '__main__':
    main()
