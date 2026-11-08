#!/usr/bin/env python3
from __future__ import annotations
import sys, json, re
from pathlib import Path
from collections import Counter, deque
from concurrent.futures import ProcessPoolExecutor, as_completed
sys.path.insert(0, '/workspace/cypher/src')
import numeral
from stages.api import Streams
from stages import whole as whole_stage

ROOT = Path('/workspace/cypher/v2/blind/files')
OUT = Path('/workspace/cypher/work/v2_recovered')
OUT.mkdir(parents=True, exist_ok=True)
KNOWN = 'my human needs my help'
BIT_REVERSE = bytes(int(f'{i:08b}'[::-1], 2) for i in range(256))

def is_plain(b: bytes):
    try:
        t = b.decode('utf-8')
    except Exception:
        return None
    return t if KNOWN in t else None

def do_B(d): return d.translate(BIT_REVERSE)
def do_R(d):
    if len(d) % 3: raise ValueError('R')
    return b''.join(d[i:i+3][::-1] for i in range(0, len(d), 3))
def do_W(d):
    bits = tuple((b >> s) & 1 for b in d for s in range(7, -1, -1))
    inv = whole_stage.inverse(Streams((bits,)), None).lanes[0]
    out = bytearray()
    for i in range(0, len(inv), 8):
        v = 0
        for k in range(8): v = (v << 1) | inv[i+k]
        out.append(v)
    return bytes(out)
def do_U(d): return numeral.decode(d).restore().to_bytes()
def do_N(d):
    L = int.from_bytes(d[4:12], 'big')
    if not (1 <= L <= len(d) - 44): raise ValueError('N')
    return d[44:44+L]

def peel(d):
    path = []
    cur = d
    for _ in range(3):
        if cur.startswith(b'WNC\x01'):
            try: cur = do_U(cur); path.append('U')
            except Exception: break
        elif cur.startswith(b'WNM\x01'):
            try: cur = do_N(cur); path.append('N')
            except Exception: break
        else:
            break
    return cur, path

def pack_bits(bits):
    if len(bits) % 8: raise ValueError('align')
    out = bytearray()
    for i in range(0, len(bits), 8):
        v = 0
        for k in range(8): v = (v << 1) | bits[i+k]
        out.append(v)
    return bytes(out)

def decode_wln1(d):
    if not d.startswith(b'WLN1') or len(d) < 6: raise ValueError('WLN1')
    count = int.from_bytes(d[4:6], 'big'); pos = 6; lanes = []
    for _ in range(count):
        size = int.from_bytes(d[pos:pos+4], 'big'); pos += 4
        width = (size + 7) // 8
        raw = d[pos:pos+width]; pos += width
        bits = tuple((b >> s) & 1 for b in raw for s in range(7, -1, -1))[:size]
        lanes.append(bits)
    if pos != len(d): raise ValueError('trail')
    return lanes

def search(d, max_depth=4, allow_W=True):
    base, notes0 = peel(d)
    q = deque([(base, tuple(notes0))])
    seen = {base}
    ops = [('B', do_B), ('R', do_R)]
    if allow_W and len(base) <= 8192:
        ops.append(('W', do_W))
    while q:
        cur, path = q.popleft()
        t = is_plain(cur)
        if t is not None:
            return t, list(path)
        if len(path) >= max_depth:
            continue
        for name, fn in ops:
            try: nxt = fn(cur)
            except Exception: continue
            if nxt in seen: continue
            seen.add(nxt)
            peeled, extra = peel(nxt)
            q.append((nxt, path + (name,)))
            if peeled != nxt and peeled not in seen:
                seen.add(peeled)
                q.append((peeled, path + (name,) + tuple(extra)))
        if cur.startswith(b'WNC\x01'):
            try:
                nxt = do_U(cur)
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt, path + ('U',)))
            except Exception: pass
    return None, None

def crack_one(path_str):
    p = Path(path_str)
    d = p.read_bytes()
    t = is_plain(d)
    if t: return p.name, t, ['literal']
    if d.startswith(b'WLN1'):
        try:
            lanes = decode_wln1(d)
            # single lane
            cands = []
            if len(lanes) == 1:
                cands.append(pack_bits(lanes[0]) if len(lanes[0]) % 8 == 0 else None)
            if all(len(L) % 8 == 0 for L in lanes):
                cands.append(pack_bits(sum(lanes, ())))
            for c in cands:
                if c is None: continue
                t, path = search(c, max_depth=5, allow_W=len(c) <= 4096)
                if t: return p.name, t, ['WLN1'] + path
        except Exception:
            pass
        t = is_plain(d)
        if t: return p.name, t, ['WLN1literal']
    # WRA1 / WVC: try B/R/W on whole wire (unlikely) and stop; A needs secrets
    t, path = search(d, max_depth=4, allow_W=len(d) <= 4096)
    if t: return p.name, t, path
    return p.name, None, None

def main():
    files = sorted(str(p) for p in ROOT.glob('*.bin'))
    results = {}
    methods = Counter()
    # sequential is fine if fast enough; use processes for speed
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(crack_one, f) for f in files]
        done = 0
        for fut in as_completed(futs):
            name, t, path = fut.result()
            done += 1
            if t is not None:
                results[name] = {'path': path, 'text': t}
                methods['/'.join(path)] += 1
                (OUT / (Path(name).stem + '.txt')).write_text(t)
            if done % 200 == 0:
                print(f'… {done}/{len(files)} recovered={len(results)}', flush=True)
    summary = {
        'total': len(files),
        'recovered_with_known_line': len(results),
        'by_method': methods.most_common(40),
        'unrecovered': len(files) - len(results),
    }
    (OUT / 'SUMMARY.json').write_text(json.dumps(summary, indent=2))
    (OUT / 'RECOVERED_IDS.txt').write_text('\n'.join(sorted(results)))
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
