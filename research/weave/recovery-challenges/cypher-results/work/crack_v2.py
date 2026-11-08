#!/usr/bin/env python3
"""Recover v2 blind-pack cases without private corpora/schedules/answers.

Allowed inversions (no secret params):
  B bit-reverse, R 3-byte reverse, W whole-stream last/first,
  U WNC numeral restore, N WNM message extract (+ then B/R/W),
  combinations of B/R/W up to depth 3, and compositions visible by magic.
"""
from __future__ import annotations
import sys, json, re
from pathlib import Path
from collections import Counter, defaultdict
sys.path.insert(0, '/workspace/cypher/src')
import numeral
from stages.api import Streams
from stages import whole as whole_stage

ROOT = Path('/workspace/cypher/v2/blind/files')
OUT = Path('/workspace/cypher/work/v2_recovered')
OUT.mkdir(parents=True, exist_ok=True)
KNOWN = 'my human needs my help'
BIT_REVERSE = bytes(int(f'{i:08b}'[::-1], 2) for i in range(256))
PRED = re.compile(r'^Prediction [0-9a-f]{32}: ')

def is_plain(b: bytes):
    try:
        t = b.decode('utf-8')
    except Exception:
        return None
    if KNOWN not in t:
        return None
    # prefer messages that look like the documented shape
    return t

def do_B(d): return d.translate(BIT_REVERSE)
def do_R(d):
    if len(d) % 3: raise ValueError('R len')
    return b''.join(d[i:i+3][::-1] for i in range(0, len(d), 3))
def do_W(d):
    bits = tuple((b >> s) & 1 for b in d for s in range(7, -1, -1))
    inv = whole_stage.inverse(Streams((bits,)), None).lanes[0]
    if len(inv) % 8: raise ValueError('W align')
    out = bytearray()
    for i in range(0, len(inv), 8):
        v = 0
        for k in range(8): v = (v << 1) | inv[i+k]
        out.append(v)
    return bytes(out)
def do_U(d):
    return numeral.decode(d).restore().to_bytes()
def do_N_extract(d):
    if not d.startswith(b'WNM\x01') or len(d) < 44: raise ValueError('WNM')
    L = int.from_bytes(d[4:12], 'big')
    if L > len(d) - 44 or L < 1: raise ValueError('len')
    return d[44:44+L]

OPS = [('B', do_B), ('R', do_R), ('W', do_W)]

def peel_magic(d):
    """Strip known framing that yields an inner payload without secrets."""
    notes = []
    cur = d
    # WRA1: root(32) + WAF wire — unaffix needs secrets; skip
    if cur.startswith(b'WNC\x01'):
        try:
            cur = do_U(cur); notes.append('U')
        except Exception as e:
            notes.append(f'U_fail:{e}')
            return cur, notes
    if cur.startswith(b'WNM\x01'):
        try:
            cur = do_N_extract(cur); notes.append('N')
        except Exception as e:
            notes.append(f'N_fail:{e}')
    return cur, notes

def search(d, max_depth=4):
    """BFS over B/R/W (+ initial magic peels)."""
    from collections import deque
    base, notes0 = peel_magic(d)
    q = deque([(base, notes0)])
    seen = {base}
    # also try peels after each op
    while q:
        cur, path = q.popleft()
        t = is_plain(cur)
        if t is not None:
            return t, path
        if len(path) >= max_depth:
            continue
        for name, fn in OPS:
            try:
                nxt = fn(cur)
            except Exception:
                continue
            if nxt in seen: continue
            seen.add(nxt)
            # maybe new framing appeared
            peeled, extra = peel_magic(nxt)
            if peeled != nxt and peeled not in seen:
                seen.add(peeled)
                q.append((peeled, path + [name] + extra))
            q.append((nxt, path + [name]))
        # also try U if looks like WNC
        if cur.startswith(b'WNC\x01'):
            try:
                nxt = do_U(cur)
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, path + ['U']))
            except Exception:
                pass
    return None, None

def try_wln1(d):
    """Decode transparent lanes; if single lane, treat as bit stream and try W/B."""
    if not d.startswith(b'WLN1') or len(d) < 6: return None, None
    count = int.from_bytes(d[4:6], 'big'); pos = 6
    lanes = []
    try:
        for _ in range(count):
            size = int.from_bytes(d[pos:pos+4], 'big'); pos += 4
            width = (size + 7) // 8
            raw = d[pos:pos+width]; pos += width
            bits = tuple((b >> s) & 1 for b in raw for s in range(7, -1, -1))[:size]
            lanes.append(bits)
        if pos != len(d): return None, None
    except Exception:
        return None, None
    # single joined lane: pack and search
    if len(lanes) == 1 and len(lanes[0]) % 8 == 0:
        packed = bytearray()
        bits = lanes[0]
        for i in range(0, len(bits), 8):
            v = 0
            for k in range(8): v = (v << 1) | bits[i+k]
            packed.append(v)
        t, path = search(bytes(packed), max_depth=5)
        if t: return t, ['WLN1'] + (path or [])
    # multi-lane: try concatenating in order (naive join) then search
    if all(len(L) % 8 == 0 for L in lanes):
        bits = sum(lanes, ())
        packed = bytearray()
        for i in range(0, len(bits), 8):
            v = 0
            for k in range(8): v = (v << 1) | bits[i+k]
            packed.append(v)
        t, path = search(bytes(packed), max_depth=4)
        if t: return t, ['WLN1cat'] + (path or [])
    # literal leakage inside WLN1
    t = is_plain(d)
    if t: return t, ['WLN1literal']
    return None, None

def main():
    results = {}
    by_method = Counter()
    files = sorted(ROOT.glob('*.bin'))
    for i, p in enumerate(files):
        d = p.read_bytes()
        t = path = None
        # literal
        t = is_plain(d)
        if t: path = ['literal']
        if t is None and d.startswith(b'WLN1'):
            t, path = try_wln1(d)
        if t is None:
            t, path = search(d, max_depth=5)
        if t is not None:
            results[p.name] = {'path': path, 'n': len(t.encode('utf-8')), 'text': t}
            by_method['/'.join(path)] += 1
            (OUT / (p.stem + '.txt')).write_text(t)
        if (i+1) % 200 == 0:
            print(f'… {i+1}/{len(files)} recovered={len(results)}', flush=True)
    summary = {
        'total': len(files),
        'recovered_with_known_line': len(results),
        'by_method': by_method.most_common(),
        'unrecovered': len(files) - len(results),
    }
    (OUT / 'SUMMARY.json').write_text(json.dumps(summary, indent=2))
    # also write id list
    (OUT / 'RECOVERED_IDS.txt').write_text('\n'.join(sorted(results)))
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
