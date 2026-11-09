#!/usr/bin/env python3
import sys, time, signal
from pathlib import Path
from collections import Counter
sys.path.insert(0, '/workspace/cypher/src')
import importlib.util, numeral
spec = importlib.util.spec_from_file_location('asm', '/workspace/cypher/work/crack_v2_Asmall.py')
asm = importlib.util.module_from_spec(spec); spec.loader.exec_module(asm)

OUT = Path('/workspace/cypher/work/v2_recovered')
ROOT = Path('/workspace/cypher/v2/blind/files')
KNOWN = 'my human needs my help'
BT = asm.BT

class Timeout(Exception): pass
def _alarm(s, f): raise Timeout()

def ok_text(t):
    if not t.startswith('Prediction '): return None
    lines = t.splitlines()
    if len(lines)<2 or lines[1]!=KNOWN: return None
    if ': ' not in lines[0]: return None
    hx = lines[0].split(': ',1)[0][len('Prediction '):]
    if len(hx)!=32 or any(c not in '0123456789abcdef' for c in hx): return None
    return t if t.endswith('\n') else t+'\n'

def do_B(d): return d.translate(BT)
def do_N(d):
    L=int.from_bytes(d[4:12],'big')
    if not 1<=L<=len(d)-44: raise ValueError
    return d[44:44+L]
def do_U(d): return numeral.decode(d).restore().to_bytes()

def cover_timed(d, max_src=900, secs=8):
    if not d.startswith(b'WRA1') or len(d)<40: return None
    try:
        src, packet, counts, pos = asm.parse(d[36:])
    except Exception:
        return None
    if src > max_src: return None
    if len(packet.entries)==1 and packet.entries[0].block.length//8==src:
        return packet.entries[0].block.to_bytes()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(secs)
    try:
        return asm.try_cover(src, packet, counts, pos)
    except Timeout:
        return None
    except Exception:
        return None
    finally:
        signal.alarm(0)

def post_peel(msg):
    from collections import deque
    from stages.api import Streams
    from stages import whole as whole_stage
    import prime_schedule as prime
    from numeral import PrimePath
    ROUTES=[prime.Route.evaluate(p) for p in [
        PrimePath(53,(('next',),('next',))),
        PrimePath(5381,(('span',10,0,2),('next',),('next',))),
        PrimePath(13,(('span',2,0,2),('next',))),
    ]]
    ARITIES=[(3,),(5,),(7,),(3,5,7),(7,3,5)]; ENDS=['first-last','last-first']
    def do_W(d):
        bits=tuple((b>>s)&1 for b in d for s in range(7,-1,-1))
        inv=whole_stage.inverse(Streams((bits,)),None).lanes[0]
        return bytes(sum(inv[i+k]<<(7-k) for k in range(8)) for i in range(0,len(inv),8))
    def do_R(d):
        if len(d)%3: raise ValueError
        return b''.join(d[i:i+3][::-1] for i in range(0,len(d),3))
    def S_list(d):
        out=[]; bl=len(d)*8
        for route in ROUTES:
            for ar in ARITIES:
                if any(a>bl for a in ar): continue
                try: split=prime.plan(bl,route,ar)
                except: continue
                for end in ENDS:
                    try: out.append(prime.interleave(d,split,inverse=True,end_order=end))
                    except: continue
        return out
    q=deque([(msg,0)]); seen={msg}
    while q:
        cur,d=q.popleft()
        try:
            o=ok_text(cur.decode('utf-8'))
            if o: return o
        except Exception: pass
        if d>=4: continue
        if cur.startswith(b'WNC\x01'):
            try:
                nxt=do_U(cur)
                if nxt not in seen: seen.add(nxt); q.append((nxt,d+1))
            except: pass
        if cur.startswith(b'WNM\x01'):
            try:
                nxt=do_N(cur)
                if nxt not in seen: seen.add(nxt); q.append((nxt,d+1))
            except: pass
        if cur.startswith(b'WRA1') and d<2:
            nxt=cover_timed(cur, max_src=900, secs=6)
            if nxt is not None and nxt not in seen: seen.add(nxt); q.append((nxt,d+1))
        for fn in (do_B, do_R, do_W):
            try:
                nxt=fn(cur)
                if nxt not in seen: seen.add(nxt); q.append((nxt,d+1))
            except: pass
        if d<2 and len(cur)<=2500:
            for s in S_list(cur):
                if s not in seen: seen.add(s); q.append((s,d+1))
    return None

def main():
    rec=set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    # Build worklist: N/U peel to WRA1 with src<=900, plus raw WRA1 src<=900, plus W/S opaque reveals
    work=[]
    for p in sorted(ROOT.glob('*.bin')):
        if p.name in rec: continue
        raw=p.read_bytes()
        variants=[('raw',raw)]
        try: variants.append(('B',do_B(raw)))
        except: pass
        for lab,d in variants:
            body=None; tag=None
            if d.startswith(b'WNM\x01'):
                try: body=do_N(d); tag='N'
                except: pass
            elif d.startswith(b'WNC\x01'):
                try: body=do_U(d); tag='U'
                except: pass
            elif d.startswith(b'WRA1'):
                body=d; tag='A'
            if body is None: continue
            if body.startswith(b'WRA1'):
                try:
                    src,packet,counts,pos=asm.parse(body[36:])
                except: continue
                if src<=900:
                    work.append((p, body if tag=='A' else d, src, f'{lab}/{tag}/src{src}'))
            elif tag in ('N','U') and len(body)<500:
                work.append((p, d, 0, f'{lab}/{tag}/short'))
    # dedupe by path keeping smallest src
    best={}
    for p,seed,src,note in work:
        if p.name not in best or src < best[p.name][2] or (best[p.name][2]==0 and src>0):
            best[p.name]=(p,seed,src,note)
    items=sorted(best.values(), key=lambda x: (x[2] if x[2] else 9999))
    print('work', len(items), flush=True)
    new=0; t0=time.time()
    for i,(p,seed,src,note) in enumerate(items):
        # Prefer starting from seed that is already inner if N-peeled
        if seed.startswith(b'WNM\x01'):
            try: seed2=do_N(seed)
            except: seed2=seed
        elif seed.startswith(b'WNC\x01'):
            try: seed2=do_U(seed)
            except: seed2=seed
        else:
            seed2=seed
        t=post_peel(seed2)
        if not t and seed2 is not seed:
            t=post_peel(seed)
        if t:
            (OUT/(p.stem+'.txt')).write_text(t)
            new+=1
            print('GOT', p.name, note, t.splitlines()[0][:50], flush=True)
        if (i+1)%15==0:
            print(f'…{i+1}/{len(items)} new={new} {time.time()-t0:.0f}s', flush=True)
        if time.time()-t0>700: print('stop'); break
    good=[]
    for p in OUT.glob('*.txt'):
        if p.name=='RECOVERED_IDS.txt': continue
        tt=p.read_text()
        if ok_text(tt): good.append(p.stem+'.bin')
    Path(OUT/'RECOVERED_IDS.txt').write_text('\n'.join(sorted(good))+'\n')
    print('new',new,'total',len(good))

if __name__=='__main__':
    main()
