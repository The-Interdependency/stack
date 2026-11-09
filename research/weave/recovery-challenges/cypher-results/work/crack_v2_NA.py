#!/usr/bin/env python3
"""Peel N/U/B/R to expose WRA1, then space-cover + post-peel. Also nested N/U."""
from __future__ import annotations
import sys, time
from pathlib import Path
from collections import deque, Counter
sys.path.insert(0, '/workspace/cypher/src')
import importlib.util, numeral, prime_schedule as prime
from numeral import PrimePath
from stages.api import Streams
from stages import whole as whole_stage

spec = importlib.util.spec_from_file_location('asm', '/workspace/cypher/work/crack_v2_Asmall.py')
asm = importlib.util.module_from_spec(spec); spec.loader.exec_module(asm)

OUT = Path('/workspace/cypher/work/v2_recovered')
ROOT = Path('/workspace/cypher/v2/blind/files')
KNOWN = 'my human needs my help'
BT = asm.BT
ROUTES = [prime.Route.evaluate(p) for p in [
    PrimePath(53, (('next',), ('next',))),
    PrimePath(5381, (('span', 10, 0, 2), ('next',), ('next',))),
    PrimePath(13, (('span', 2, 0, 2), ('next',))),
]]
ARITIES = [(3,), (5,), (7,), (3, 5, 7), (7, 3, 5)]
ENDS = ['first-last', 'last-first']

def ok(b: bytes):
    try:
        t = b.decode('utf-8')
    except Exception:
        return None
    if not t.startswith('Prediction '):
        return None
    lines = t.splitlines()
    if len(lines) < 2 or lines[1] != KNOWN:
        return None
    if ': ' not in lines[0]:
        return None
    left, right = lines[0].split(': ', 1)
    hx = left[len('Prediction '):]
    if len(hx) != 32 or any(c not in '0123456789abcdef' for c in hx):
        return None
    return t if t.endswith('\n') else t + '\n'

def do_B(d): return d.translate(BT)
def do_R(d):
    if len(d) % 3: raise ValueError
    return b''.join(d[i:i+3][::-1] for i in range(0, len(d), 3))
def do_W(d):
    bits = tuple((b >> s) & 1 for b in d for s in range(7, -1, -1))
    inv = whole_stage.inverse(Streams((bits,)), None).lanes[0]
    return bytes(sum(inv[i+k] << (7-k) for k in range(8)) for i in range(0, len(inv), 8))
def do_N(d):
    L = int.from_bytes(d[4:12], 'big')
    if not 1 <= L <= len(d) - 44: raise ValueError
    return d[44:44+L]
def do_U(d):
    return numeral.decode(d).restore().to_bytes()
def S_list(d):
    out = []; bl = len(d) * 8
    for route in ROUTES:
        for ar in ARITIES:
            if any(a > bl for a in ar): continue
            try: split = prime.plan(bl, route, ar)
            except Exception: continue
            for end in ENDS:
                try: out.append(prime.interleave(d, split, inverse=True, end_order=end))
                except Exception: continue
    return out

def try_unaffix(d, max_src=2500):
    if not d.startswith(b'WRA1') or len(d) < 40:
        return None
    try:
        src, packet, counts, pos = asm.parse(d[36:])
    except Exception:
        return None
    if src > max_src:
        return None
    # single entry shortcut
    if len(packet.entries) == 1 and packet.entries[0].block.length // 8 == src:
        return packet.entries[0].block.to_bytes()
    try:
        return asm.try_cover(src, packet, counts, pos)
    except Exception:
        return None

def deep_peel(seed, max_a=2, max_src=2500, deadline=None):
    q = deque([(seed, 0, 0)])  # bytes, depth, a_count
    seen = {seed}
    while q:
        if deadline and time.time() > deadline:
            break
        cur, d, ac = q.popleft()
        t = ok(cur)
        if t:
            return t
        if d >= 6:
            continue
        # WRA1 unaffix
        if ac < max_a and cur.startswith(b'WRA1'):
            nxt = try_unaffix(cur, max_src=max_src)
            if nxt is not None and nxt not in seen:
                seen.add(nxt); q.append((nxt, d+1, ac+1))
        if cur.startswith(b'WNM\x01'):
            try:
                nxt = do_N(cur)
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt, d+1, ac))
            except Exception:
                pass
        if cur.startswith(b'WNC\x01'):
            try:
                nxt = do_U(cur)
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt, d+1, ac))
            except Exception:
                pass
        for fn in (do_B, do_R):
            try:
                nxt = fn(cur)
                if nxt not in seen and len(nxt) <= 12000:
                    seen.add(nxt); q.append((nxt, d+1, ac))
            except Exception:
                pass
        if d < 3 and len(cur) <= 4096:
            try:
                nxt = do_W(cur)
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt, d+1, ac))
            except Exception:
                pass
        if d < 2 and len(cur) <= 3000:
            for s in S_list(cur):
                if s not in seen:
                    seen.add(s); q.append((s, d+1, ac))
    return None

def main():
    rec = set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    # prioritize: outer WNM/WNC or B→those, and raw WRA1 with src<=2500
    targets = []
    for p in sorted(ROOT.glob('*.bin')):
        if p.name in rec: continue
        raw = p.read_bytes()
        score = 0
        if raw.startswith(b'WNM\x01'): score = 3
        elif raw.startswith(b'WNC\x01'): score = 2
        elif raw.startswith(b'WRA1'): score = 1
        else:
            try:
                if do_B(raw).startswith((b'WNM\x01', b'WNC\x01', b'WRA1')): score = 2
            except Exception: pass
        if score:
            targets.append((score, p))
    targets.sort(key=lambda x: -x[0])
    print('targets', len(targets), flush=True)
    new = 0; meth = Counter()
    t0 = time.time()
    for i, (score, p) in enumerate(targets):
        # per-file budget
        deadline = time.time() + 45
        t = deep_peel(p.read_bytes(), max_a=2, max_src=2500, deadline=deadline)
        if t:
            (OUT/(p.stem+'.txt')).write_text(t)
            new += 1; meth[score] += 1
            print('GOT', p.name, 'score', score, t.splitlines()[0][:60], flush=True)
        if (i+1) % 20 == 0:
            print(f'…{i+1}/{len(targets)} new={new} elapsed={time.time()-t0:.0f}s', flush=True)
        # stop if too long overall (~25 min local)
        if time.time() - t0 > 1500:
            print('time budget stop', flush=True); break
    ids = sorted(x.stem+'.bin' for x in OUT.glob('*.txt') if x.name != 'RECOVERED_IDS.txt')
    # validate
    good = []
    for bid in ids:
        tt = (OUT/(bid[:-4]+'.txt')).read_text()
        if ok(tt.encode() if False else tt.encode('utf-8') if isinstance(tt,str) else tt):
            # ok() expects bytes-like via decode path — use text
            lines = tt.splitlines()
            if tt.startswith('Prediction ') and len(lines)>=2 and lines[1]==KNOWN:
                good.append(bid)
    Path(OUT/'RECOVERED_IDS.txt').write_text('\n'.join(sorted(set(good)))+'\n')
    print('new', new, 'total', len(good), 'meth', meth)
    print('elapsed', round(time.time()-t0,1))

if __name__ == '__main__':
    main()
