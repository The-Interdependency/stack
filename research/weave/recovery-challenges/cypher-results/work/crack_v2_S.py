#!/usr/bin/env python3
"""Brute-force prime-route interleave (S) over the public matrix catalog; also W on larger files."""
from __future__ import annotations
import sys, json
from pathlib import Path
from collections import Counter
sys.path.insert(0, '/workspace/cypher/src')
import numeral, prime_schedule as prime
from stages.api import Streams
from stages import whole as whole_stage

ROOT = Path('/workspace/cypher/v2/blind/files')
OUT = Path('/workspace/cypher/work/v2_recovered')
KNOWN = 'my human needs my help'
BIT_REVERSE = bytes(int(f'{i:08b}'[::-1], 2) for i in range(256))

PATHS = [
    {'seed': 53, 'steps': [('next',), ('next',)]},
    {'seed': 5381, 'steps': [('span', 10, 0, 2), ('next',), ('next',)]},
    {'seed': 13, 'steps': [('span', 2, 0, 2), ('next',)]},
]
ARITIES = [(3,), (5,), (7,), (3,5,7), (7,3,5)]
ENDS = ['first-last', 'last-first']

def is_plain(b):
    try:
        t = b.decode('utf-8')
    except Exception:
        return None
    return t if KNOWN in t else None

def do_B(d): return d.translate(BIT_REVERSE)
def do_R(d):
    if len(d)%3: raise ValueError
    return b''.join(d[i:i+3][::-1] for i in range(0,len(d),3))
def do_W(d):
    bits = tuple((b>>s)&1 for b in d for s in range(7,-1,-1))
    inv = whole_stage.inverse(Streams((bits,)), None).lanes[0]
    out=bytearray()
    for i in range(0,len(inv),8):
        v=0
        for k in range(8): v=(v<<1)|inv[i+k]
        out.append(v)
    return bytes(out)

# precompute routes
_ROUTES = []
for p in PATHS:
    pp = numeral.PrimePath(p['seed'], tuple(p['steps']))
    _ROUTES.append(prime.Route.evaluate(pp))

def all_S_inverse(d):
    """Yield (label, bytes) for every catalog S inverse."""
    bl = len(d)*8
    for ri, route in enumerate(_ROUTES):
        for ar in ARITIES:
            if any(a > bl for a in ar): continue
            try:
                split = prime.plan(bl, route, ar)
            except Exception:
                continue
            for end in ENDS:
                try:
                    out = prime.interleave(d, split, inverse=True, end_order=end)
                except Exception:
                    continue
                yield f'S[p{ri}/a{ar}/{end}]', out

def peel_NU(d):
    cur=d; path=[]
    if cur.startswith(b'WNC\x01'):
        try:
            cur=numeral.decode(cur).restore().to_bytes(); path.append('U')
        except Exception: pass
    if cur.startswith(b'WNM\x01') and len(cur)>=44:
        L=int.from_bytes(cur[4:12],'big')
        if 1<=L<=len(cur)-44:
            cur=cur[44:44+L]; path.append('N')
    return cur, path

def crack(d):
    # try S alone and S after B/R/W peel sandwich
    cands = [('id', d)]
    for name,fn in [('B',do_B),('R',do_R)]:
        try: cands.append((name, fn(d)))
        except Exception: pass
    if len(d)<=8192:
        try: cands.append(('W', do_W(d)))
        except Exception: pass
    for pref, cur0 in cands:
        for sname, out in all_S_inverse(cur0):
            # after S, peel N/U and reflections
            peeled, extra = peel_NU(out)
            for label, blob in [(sname, out), (sname+'+peel', peeled)]:
                t = is_plain(blob)
                if t: return t, [pref, label] + extra
                for n2,f2 in [('B',do_B),('R',do_R)]:
                    try:
                        b2=f2(blob); t=is_plain(b2)
                        if t: return t, [pref, label, n2]
                        p2,e2=peel_NU(b2); t=is_plain(p2)
                        if t: return t, [pref, label, n2]+e2
                    except Exception: pass
    return None, None

def main():
    recovered=set(Path(OUT/'RECOVERED_IDS.txt').read_text().split()) if (OUT/'RECOVERED_IDS.txt').exists() else set()
    methods=Counter(); new=0
    files=sorted(ROOT.glob('*.bin'))
    for i,p in enumerate(files):
        if p.name in recovered: continue
        d=p.read_bytes()
        # skip huge for S brute (still ok but slower)
        if len(d)>20000: continue
        t,path=crack(d)
        if t:
            new+=1; recovered.add(p.name)
            methods['/'.join(path)]+=1
            (OUT/(p.stem+'.txt')).write_text(t)
            print('GOT', p.name, path, t[:60].replace('\n','|'))
        if (i+1)%300==0:
            print(f'… {i+1} new={new}', flush=True)
    # update summary
    ids=sorted(recovered)
    (OUT/'RECOVERED_IDS.txt').write_text('\n'.join(ids))
    print(json.dumps({'new_this_pass':new, 'total_recovered':len(ids), 'methods':methods.most_common(20)}, indent=2))

if __name__=='__main__':
    main()
