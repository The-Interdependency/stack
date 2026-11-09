#!/usr/bin/env python3
import sys, time, signal
from pathlib import Path
from collections import deque
sys.path.insert(0,'/workspace/cypher/src')
import importlib.util, numeral, prime_schedule as prime
from numeral import PrimePath
from stages.api import Streams
from stages import whole as whole_stage
spec=importlib.util.spec_from_file_location('asm','/workspace/cypher/work/crack_v2_Asmall.py')
asm=importlib.util.module_from_spec(spec); spec.loader.exec_module(asm)
OUT=Path('/workspace/cypher/work/v2_recovered'); ROOT=Path('/workspace/cypher/v2/blind/files')
KNOWN='my human needs my help'; BT=asm.BT
KNOWN_M=(b'WLN1',b'WNM\x01',b'WRA1',b'WNC\x01',b'WVC\x01')
ROUTES=[prime.Route.evaluate(p) for p in [PrimePath(53,(('next',),('next',))),PrimePath(5381,(('span',10,0,2),('next',),('next',))),PrimePath(13,(('span',2,0,2),('next',)))]]
ARITIES=[(3,),(5,),(7,),(3,5,7),(7,3,5)]; ENDS=['first-last','last-first']
class Timeout(Exception): pass
def _al(s,f): raise Timeout()

def ok_text(t):
    if not t.startswith('Prediction '): return None
    lines=t.splitlines()
    if len(lines)<2 or lines[1]!=KNOWN: return None
    if ': ' not in lines[0]: return None
    hx=lines[0].split(': ',1)[0][len('Prediction '):]
    if len(hx)!=32 or any(c not in '0123456789abcdef' for c in hx): return None
    return t if t.endswith('\n') else t+'\n'
def do_B(d): return d.translate(BT)
def do_R(d):
    if len(d)%3: raise ValueError
    return b''.join(d[i:i+3][::-1] for i in range(0,len(d),3))
def do_W(d):
    bits=tuple((b>>s)&1 for b in d for s in range(7,-1,-1))
    inv=whole_stage.inverse(Streams((bits,)),None).lanes[0]
    return bytes(sum(inv[i+k]<<(7-k) for k in range(8)) for i in range(0,len(inv),8))
def do_N(d):
    L=int.from_bytes(d[4:12],'big')
    if not 1<=L<=len(d)-44: raise ValueError
    return d[44:44+L]
def do_U(d): return numeral.decode(d).restore().to_bytes()
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
def cover(d,secs=5,max_src=600):
    if not d.startswith(b'WRA1'): return None
    try: src,packet,counts,pos=asm.parse(d[36:])
    except: return None
    if src>max_src: return None
    if len(packet.entries)==1 and packet.entries[0].block.length//8==src:
        return packet.entries[0].block.to_bytes()
    signal.signal(signal.SIGALRM,_al); signal.alarm(secs)
    try: return asm.try_cover(src,packet,counts,pos)
    except: return None
    finally: signal.alarm(0)

def crack(raw):
    # first reveal
    seeds=[raw]
    try: seeds.append(do_W(raw))
    except: pass
    try: seeds.append(do_B(raw))
    except: pass
    if len(raw)<=3000:
        seeds.extend(S_list(raw))
    # keep only those that hit magic or decode as text
    useful=[]
    for s in seeds:
        if s.startswith(KNOWN_M) or (len(s)<300 and b'Prediction' in s):
            useful.append(s)
    if not useful: return None
    q=deque([(u,0) for u in useful]); seen=set(useful)
    while q:
        cur,d=q.popleft()
        try:
            o=ok_text(cur.decode('utf-8'))
            if o: return o
        except: pass
        if d>=5: continue
        nxts=[]
        if cur.startswith(b'WNM\x01'):
            try: nxts.append(do_N(cur))
            except: pass
        if cur.startswith(b'WNC\x01'):
            try: nxts.append(do_U(cur))
            except: pass
        if cur.startswith(b'WRA1') and d<2:
            c=cover(cur)
            if c: nxts.append(c)
        for fn in (do_B,do_R,do_W):
            try: nxts.append(fn(cur))
            except: pass
        if d<2 and len(cur)<=2500:
            nxts.extend(S_list(cur))
        for nxt in nxts:
            if nxt in seen or len(nxt)>15000: continue
            seen.add(nxt); q.append((nxt,d+1))
    return None

def main():
    rec=set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    targets=[]
    for p in sorted(ROOT.glob('*.bin')):
        if p.name in rec: continue
        raw=p.read_bytes()
        if raw.startswith(KNOWN_M) or do_B(raw).startswith(KNOWN_M): continue
        targets.append(p)
    print('opaque',len(targets),flush=True)
    new=0; t0=time.time()
    for i,p in enumerate(targets):
        t=crack(p.read_bytes())
        if t:
            (OUT/(p.stem+'.txt')).write_text(t); new+=1
            print('GOT',p.name,t.splitlines()[0][:55],flush=True)
        if (i+1)%40==0: print(f'…{i+1} new={new} {time.time()-t0:.0f}s',flush=True)
        if time.time()-t0>600: break
    good=[p.stem+'.bin' for p in OUT.glob('*.txt') if p.name!='RECOVERED_IDS.txt' and ok_text(p.read_text())]
    Path(OUT/'RECOVERED_IDS.txt').write_text('\n'.join(sorted(good))+'\n')
    print('new',new,'total',len(good))
if __name__=='__main__': main()
