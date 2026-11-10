#!/usr/bin/env python3
"""SAT recovery for exactly-one-C WLN1, with hex-charset constraints.

Window bits w[t] pick left/right ends of each live lane's deque (public corpus
route).  Known template bits forbid some picks; unknown hex bits are SAT vars
restricted to 0-9a-f.  Uniqueness: solve, then forbid that hex assignment.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path[:0] = ['/workspace/cypher/work/r12', '/workspace/cypher/work/r10', '/workspace/cypher/v2', '/workspace/cypher/src']
import wln_dp as D
import wln_coupled as W
from pysat.solvers import Glucose4

# valid hex bytes
HEXS = list(b'0123456789abcdef')


class Enc:
    def __init__(self):
        self.n = 0
        self.cs = []

    def var(self, k=1):
        start = self.n + 1
        self.n += k
        if k == 1:
            return start
        return list(range(start, start + k))

    def add(self, *xs):
        self.cs.append(list(xs))

    def iff(self, a, b):
        self.add(a, -b)
        self.add(-a, b)

    def ite(self, b, t, e):
        """o <=> (b ? t : e). t/e may be lits."""
        o = self.var()
        self.add(b, -o, e)
        self.add(b, o, -e)
        self.add(-b, -o, t)
        self.add(-b, o, -t)
        return o

    def bit_eq_const(self, bits, val):
        """lit <=> (bits == val)."""
        lits = []
        for i, b in enumerate(bits):
            lits.append(b if ((val >> i) & 1) else -b)
        return self.and_lits(lits)

    def and_lits(self, lits):
        if not lits:
            v = self.var(); self.add(v); return v
        if len(lits) == 1:
            return lits[0]
        o = self.var()
        self.add(*([-x for x in lits] + [o]))  # all => o?  wait AND: o => each; each=>o
        # o <=> AND(lits): (~l1|~l2|...|o) and (~o|l_i)
        for x in lits:
            self.add(-o, x)
        self.add(*([-x for x in lits] + [o]))
        return o

    def increment(self, bits, cin):
        """(sum_bits, cout) = bits + cin, same width (ignore overflow into extra)."""
        sums = []
        c = cin
        for b in bits:
            # s = b XOR c, c' = b AND c
            s = self.var()
            # s <=> b xor c: (s|b|~c)(s|~b|c)(~s|b|c)(~s|~b|~c)? 
            # xor: s <=> (b|c) & ~(b&c)
            self.add(-s, b, c)
            self.add(-s, -b, -c)
            self.add(s, -b, c)
            self.add(s, b, -c)
            c2 = self.var()
            # c2 <=> b & c
            self.add(-c2, b)
            self.add(-c2, c)
            self.add(c2, -b, -c)
            sums.append(s)
            c = c2
        return sums, c


def encode(z, u):
    E = Enc()
    m = len(u)
    ns = [len(l) for l in u]
    T = max(ns[k] + k for k in range(m))
    w = [E.var() for _ in range(T)]
    pt = [None] * W.NB
    for i, kb in enumerate(W.KB):
        if kb is None:
            pt[i] = E.var()
    # hex charset
    for bi in range(W.HEXLO, W.HEXHI):
        # 8 bits MSB first: indices 8*bi .. 8*bi+7 map to bit7..bit0
        blits = []
        for s in range(7, -1, -1):
            idx = 8 * bi + (7 - s)
            # idx = 8*bi + pos_in_byte_msb_first
            pass
        # bits list MSB first matching TEMPLATE packing
        byte_lits = []
        for s in range(8):
            idx = 8 * bi + s  # s=0 is bit7 (MSB)
            if W.KB[idx] is not None:
                byte_lits.append(None)  # constant
            else:
                byte_lits.append(pt[idx])
        # enumerate valid hex: at least one valid pattern
        options = []
        for ch in HEXS:
            lits = []
            ok = True
            for s in range(8):
                idx = 8 * bi + s
                bit = (ch >> (7 - s)) & 1
                kb = W.KB[idx]
                if kb is not None:
                    if kb != bit:
                        ok = False
                        break
                else:
                    lits.append(pt[idx] if bit else -pt[idx])
            if ok:
                options.append(E.and_lits(lits) if lits else None)
        options = [o for o in options if o is not None]
        # at least one valid (constants-only valid hex is implicit if options empty after filter...
        # if a pattern is all-constant and ok, lits=[] we treated as None and dropped — that
        # pattern is already satisfied. If ANY all-constant ok pattern exists, charset is free.
        raw_ok_const = False
        # recompute properly:
    # redo hex more clearly
    E.cs = [c for c in E.cs]  # keep w,pt vars; we'll add hex below after clearing accidental
    # Actually rebuild hex only:
    hex_clauses_start = len(E.cs)
    # We'll just add the OR-of-valid-patterns now, ignoring the partial loop above.
    # Remove unused options from the sloppy first loop by not adding OR yet.
    # The sloppy loop added and_lits vars but no OR — harmless extra vars.

    for bi in range(W.HEXLO, W.HEXHI):
        pats = []
        const_ok = False
        for ch in HEXS:
            lits = []
            ok = True
            for s in range(8):
                idx = 8 * bi + s
                bit = (ch >> (7 - s)) & 1
                kb = W.KB[idx]
                if kb is not None:
                    if kb != bit:
                        ok = False
                        break
                else:
                    lits.append(pt[idx] if bit else -pt[idx])
            if not ok:
                continue
            if not lits:
                const_ok = True
                break
            pats.append(E.and_lits(lits))
        if not const_ok:
            if not pats:
                E.add()  # UNSAT
            else:
                E.add(*pats)

    # prefix sums and pick constraints per lane
    width = 11
    # For each window offset that appears, we could share S — offsets are 0..m-1
    # S_off[i] = sum(w[off:off+i]) as `width` bits, LSB first
    S = {}  # (off, i) -> bits
    for off in range(m):
        zero = E.var(width)
        for b in zero:
            E.add(-b)
        S[(off, 0)] = zero
        max_i = max((ns[k] for k in range(m) if k == off), default=0)
        # each lane k uses offset k, i=0..ns[k]
        max_i = ns[off] if off < m else 0
        for i in range(max_i):
            prev = S[(off, i)]
            nxt, _cout = E.increment(prev, w[off + i])
            S[(off, i + 1)] = nxt

    for k in range(m):
        n = ns[k]
        off = k
        for i in range(n):
            wb = w[off + i]
            sbits = S[(off, i)]  # sum w[off:off+i]
            # P = wb ? n-1-S : i-S
            # compute i-S and (n-1)-S as bitvectors, then ITE
            def const_minus(const, bits):
                # const - bits, width bits, two's complement: const + ~bits + 1
                inv = [-b for b in bits]
                sums, c = Enc.increment(E, inv, 1) if False else (None, None)
                # add const bit by bit to ~bits + 1
                # first increment inv already = -bits
                neg, _ = E.increment(inv, 1 if True else 0)  # -bits = ~bits+1
                # now add const
                # add const to neg
                c = 0  # we'll do ripple with const bits as fixed
                out = []
                carry_lit = None
                for j in range(width):
                    cb = (const >> j) & 1
                    b = neg[j]
                    if carry_lit is None:
                        # first: just b + cb
                        if cb:
                            # s = ~b, c = b  (adding 1)
                            s = E.var(); E.iff(s, -b); out.append(s)
                            carry_lit = b
                        else:
                            out.append(b)
                            carry_lit = None
                            # represent 0 carry as... use next iteration carefully
                            # set carry_lit to a false var
                            z = E.var(); E.add(-z); carry_lit = z
                    else:
                        # s = b xor cb xor carry; c = maj
                        if cb:
                            # s = ~b xor carry = ~(b xor carry)?  b xor 1 xor c = ~b xor c
                            s = E.var()
                            # s <=> b xor 1 xor carry <=> ~b xor carry? wait b xor True = ~b; (~b) xor carry
                            # s <=> -b xor carry_lit
                            E.add(-s, -b, carry_lit)
                            E.add(-s, b, -carry_lit)
                            E.add(s, -b, -carry_lit)
                            E.add(s, b, carry_lit)
                            # c2 <=> (b & 1) | (b & carry) | (1 & carry) = b | carry
                            c2 = E.var()
                            E.add(-b, c2)
                            E.add(-carry_lit, c2)
                            E.add(-c2, b, carry_lit)
                            carry_lit = c2
                            out.append(s)
                        else:
                            # s = b xor 0 xor carry = b xor carry
                            s = E.var()
                            E.add(-s, b, carry_lit)
                            E.add(-s, -b, -carry_lit)
                            E.add(s, -b, carry_lit)
                            E.add(s, b, -carry_lit)
                            # c2 <=> b & carry
                            c2 = E.var()
                            E.add(-c2, b)
                            E.add(-c2, carry_lit)
                            E.add(c2, -b, -carry_lit)
                            carry_lit = c2
                            out.append(s)
                return out

            p0 = const_minus(i, sbits)
            p1 = const_minus(n - 1, sbits)
            P = [E.ite(wb, p1[j], p0[j]) for j in range(width)]
            want = z[k][i]
            for pos in range(n):
                eq = E.bit_eq_const(P, pos)
                pbit = u[k][pos]
                kb = W.KB[pbit]
                if kb is not None:
                    if kb != want:
                        E.add(-eq)  # cannot pick this pos
                    # else always fine
                else:
                    hv = pt[pbit]
                    # eq => (hv == want)
                    if want:
                        E.add(-eq, hv)
                    else:
                        E.add(-eq, -hv)
    return E, w, pt


def recover(z, u, check_unique=True):
    E, w, pt = encode(z, u)
    wild = [i for i, kb in enumerate(W.KB) if kb is None]
    with Glucose4(bootstrap_with=E.cs) as slv:
        if not slv.solve():
            return 'none', None
        model = set(slv.get_model())
        def msg_of(model):
            bits = []
            for i in range(W.NB):
                if W.KB[i] is not None:
                    bits.append(W.KB[i])
                else:
                    bits.append(1 if pt[i] in model else 0)
            return D._pack(bits)
        msg = msg_of(model)
        if not all(c in W.HEXS for c in msg[W.HEXLO:W.HEXHI]):
            return 'none', None
        if not check_unique:
            return 'sat', msg
        # forbid this hex assignment
        clause = []
        for i in wild:
            clause.append(-pt[i] if pt[i] in model else pt[i])
        slv.add_clause(clause)
        if slv.solve():
            msg2 = msg_of(set(slv.get_model()))
            return 'ambiguous', (msg, msg2)
        return 'unique', msg


if __name__ == '__main__':
    import os, random, time
    random.seed(7)
    msg = W.PREFIX + bytes(random.choice(b'0123456789abcdef') for _ in range(32)) + W.TEMPLATE[W.HEXHI:]
    p = {'initial_lanes': 1, 'thread_count': 3, 'lane_rotation': 0, 'inter_arity': 3,
         'corpus_hex': os.urandom(256).hex(), 'corpus_bit_offset': random.randrange(8192)}
    wire = W.tc.run(msg, ['X', 'C'], p)
    st = W.tc.decode_lanes(wire)
    wl = [list(l) for l in st.lanes]
    u, v, final = D.layouts_any(('X', 'C'), 1, 3, 0, 3)
    z = D.wire_z(wl, v, u)
    t0 = time.time()
    print('encoding...', flush=True)
    status, rec = recover(z, u)
    print('status', status, 'secs', round(time.time() - t0, 2), flush=True)
    if status == 'unique':
        print('match', rec == msg, rec[11:43], flush=True)
    elif status == 'ambiguous':
        print('m1', rec[0][11:43], 'match0', rec[0] == msg, 'm2', rec[1][11:43], flush=True)
