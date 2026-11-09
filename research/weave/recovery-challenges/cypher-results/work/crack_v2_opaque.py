#!/usr/bin/env python3
"""Attack opaque IDs via W/S(/B) peels into known magics, then N/U/A/S deep peel."""
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
KNOWN_M = (b'WLN1', b'WNM\x01', b'WRA1', b'WNC\x01', b'WVC\x01', b'WAF\x01')
ROUTES = [prime.Route.evaluate(p) for p in [
    PrimePath(53, (('next',), ('next',))),
    PrimePath(5381, (('span', 10, 0, 2), ('next',), ('next',))),
    PrimePath(13, (('span', 2, 0, 2), ('next',))),
]]
ARITIES = [(3,), (5,), (7,), (3, 5, 7), (7, 3, 5)]
ENDS = ['first-last', 'last-first']

def ok_text(t: str):
    if not t.startswith('Prediction '): return None
    lines = t.splitlines()
    if len(lines) < 2 or lines[1] != KNOWN: return None
    if ': ' not in lines[0]: return None
    left, right = lines[0].split(': ', 1)
    hx = left[len('Prediction '):]
    if len(hx) != 32 or any(c not in '0123456789abcdef' for c in hx): return None
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
def do_U(d): return numeral.decode(d).restore().to_bytes()
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

def try_unaffix(d, max_src=2000):
    if not d.startswith(b'WRA1') or len(d) < 40: return None
    try:
        src, packet, counts, pos = asm.parse(d[36:])
    except Exception:
        return None
    if src > max_src: return None
    if len(packet.entries) == 1 and packet.entries[0].block.length // 8 == src:
        return packet.entries[0].block.to_bytes()
    try:
        return asm.try_cover(src, packet, counts, pos)
    except Exception:
        return None

def peel_once(d):
    """Yield one-step peels."""
    for fn in (do_B, do_R, do_W):
        try: yield fn(d)
        except Exception: pass
    if d.startswith(b'WNM\x01'):
        try: yield do_N(d)
        except Exception: pass
    if d.startswith(b'WNC\x01'):
        try: yield do_U(d)
        except Exception: pass
    if d.startswith(b'WRA1'):
        u = try_unaffix(d, max_src=1800)
        if u is not None: yield u
    if len(d) <= 3500:
        yield from S_list(d)

def crack(raw, deadline):
    q = deque([(raw, 0)])
    seen = {raw}
    while q:
        if time.time() > deadline: break
        cur, depth = q.popleft()
        try:
            t = cur.decode('utf-8')
            o = ok_text(t)
            if o: return o
        except Exception:
            pass
        if depth >= 5: continue
        for nxt in peel_once(cur):
            if nxt in seen or len(nxt) > 20000: continue
            seen.add(nxt)
            q.append((nxt, depth + 1))
    return None

def is_opaque(raw):
    if raw.startswith(KNOWN_M): return False
    try:
        if do_B(raw).startswith(KNOWN_M): return False
    except Exception:
        pass
    return True

def main():
    rec = set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    targets = [p for p in sorted(ROOT.glob('*.bin')) if p.name not in rec and is_opaque(p.read_bytes())]
    print('opaque targets', len(targets), flush=True)
    new = 0; meth = Counter()
    t0 = time.time()
    for i, p in enumerate(targets):
        raw = p.read_bytes()
        # quick reveal
        revealed = None
        for label, d in [('W', None)]:
            pass
        cands = [raw]
        try: cands.append(do_W(raw)); 
        except Exception: pass
        try: cands.append(do_B(raw))
        except Exception: pass
        if len(raw) <= 4000:
            cands.extend(S_list(raw)[:30])  # cap
        # only pursue if some cand hits known magic or short
        pursue = any(c.startswith(KNOWN_M) or len(c) < 200 for c in cands)
        if not pursue and len(raw) > 5000:
            continue
        t = crack(raw, deadline=time.time()+30)
        if t:
            (OUT/(p.stem+'.txt')).write_text(t)
            new += 1
            print('GOT', p.name, t.splitlines()[0][:55], flush=True)
        if (i+1) % 50 == 0:
            print(f'…{i+1}/{len(targets)} new={new} {time.time()-t0:.0f}s', flush=True)
        if time.time()-t0 > 900:
            print('time stop'); break
    # refresh ids
    good=[]
    for p in OUT.glob('*.txt'):
        if p.name=='RECOVERED_IDS.txt': continue
        t=p.read_text()
        if ok_text(t): good.append(p.stem+'.bin')
    Path(OUT/'RECOVERED_IDS.txt').write_text('\n'.join(sorted(good))+'\n')
    print('new', new, 'total', len(good))

if __name__ == '__main__':
    main()
