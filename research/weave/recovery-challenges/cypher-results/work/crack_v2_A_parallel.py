#!/usr/bin/env python3
import sys, time, signal, os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
sys.path.insert(0,'/workspace/cypher/src')

OUT = Path('/workspace/cypher/work/v2_recovered')
ROOT = Path('/workspace/cypher/v2/blind/files')
KNOWN = 'my human needs my help'

def ok_text(t):
    if not t.startswith('Prediction '): return None
    lines=t.splitlines()
    if len(lines)<2 or lines[1]!=KNOWN: return None
    if ': ' not in lines[0]: return None
    hx=lines[0].split(': ',1)[0][len('Prediction '):]
    if len(hx)!=32 or any(c not in '0123456789abcdef' for c in hx): return None
    return t if t.endswith('\n') else t+'\n'

def worker(args):
    path, max_src, secs = args
    # re-import in worker
    import importlib.util, numeral
    from collections import deque
    from stages.api import Streams
    from stages import whole as whole_stage
    import prime_schedule as prime
    from numeral import PrimePath
    spec=importlib.util.spec_from_file_location('asm','/workspace/cypher/work/crack_v2_Asmall.py')
    asm=importlib.util.module_from_spec(spec); spec.loader.exec_module(asm)
    BT=asm.BT
    class Timeout(Exception): pass
    def _al(s,f): raise Timeout()
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
    ROUTES=[prime.Route.evaluate(p) for p in [PrimePath(53,(('next',),('next',))),PrimePath(5381,(('span',10,0,2),('next',),('next',))),PrimePath(13,(('span',2,0,2),('next',)))]]
    ARITIES=[(3,),(5,),(7,),(3,5,7),(7,3,5)]; ENDS=['first-last','last-first']
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
    def cover(d):
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
    raw=Path(path).read_bytes()
    seeds=[raw]
    try: seeds.append(do_B(raw))
    except: pass
    if raw.startswith(b'WNM\x01'):
        try: seeds.append(do_N(raw))
        except: pass
    # also if N then WRA1
    expanded=[]
    for s in seeds:
        expanded.append(s)
        if s.startswith(b'WNM\x01'):
            try: expanded.append(do_N(s))
            except: pass
        if s.startswith(b'WNC\x01'):
            try: expanded.append(do_U(s))
            except: pass
    q=deque([(s,0) for s in expanded]); seen=set(expanded)
    while q:
        cur,d=q.popleft()
        try:
            o=ok_text(cur.decode('utf-8'))
            if o: return Path(path).name, o
        except: pass
        if d>=4: continue
        if cur.startswith(b'WRA1') and d<2:
            nxt=cover(cur)
            if nxt is not None and nxt not in seen:
                seen.add(nxt); q.append((nxt,d+1))
        if cur.startswith(b'WNM\x01'):
            try:
                nxt=do_N(cur)
                if nxt not in seen: seen.add(nxt); q.append((nxt,d+1))
            except: pass
        if cur.startswith(b'WNC\x01'):
            try:
                nxt=do_U(cur)
                if nxt not in seen: seen.add(nxt); q.append((nxt,d+1))
            except: pass
        for fn in (do_B,do_R,do_W):
            try:
                nxt=fn(cur)
                if nxt not in seen: seen.add(nxt); q.append((nxt,d+1))
            except: pass
        if d<2 and len(cur)<=2500:
            for s in S_list(cur):
                if s not in seen: seen.add(s); q.append((s,d+1))
    return Path(path).name, None

def main():
    rec=set(Path(OUT/'RECOVERED_IDS.txt').read_text().split())
    # gather WRA1-ish targets with parseable src in range
    import importlib.util
    spec=importlib.util.spec_from_file_location('asm','/workspace/cypher/work/crack_v2_Asmall.py')
    asm=importlib.util.module_from_spec(spec); spec.loader.exec_module(asm)
    BT=asm.BT
    jobs=[]
    for p in sorted(ROOT.glob('*.bin')):
        if p.name in rec: continue
        raw=p.read_bytes()
        cands=[raw]
        try: cands.append(raw.translate(BT))
        except: pass
        # N peel
        for d in list(cands):
            if d.startswith(b'WNM\x01') and len(d)>=44:
                L=int.from_bytes(d[4:12],'big')
                if 1<=L<=len(d)-44: cands.append(d[44:44+L])
        hit=False; srcv=None
        for d in cands:
            if d.startswith(b'WRA1'):
                try:
                    src,_,_,_=asm.parse(d[36:])
                    if 200<=src<=1500:
                        hit=True; srcv=src; break
                except: pass
        if hit:
            jobs.append((str(p), 1500, 15))
    # sort by nothing; limit to 80 jobs for time
    print('jobs',len(jobs),flush=True)
    jobs=jobs[:100]
    new=0
    with ProcessPoolExecutor(max_workers=3) as ex:
        futs=[ex.submit(worker,j) for j in jobs]
        for i,fut in enumerate(as_completed(futs)):
            name,t=fut.result()
            if t:
                (OUT/(Path(name).stem+'.txt')).write_text(t); new+=1
                print('GOT',name,t.splitlines()[0][:50],flush=True)
            if (i+1)%10==0: print(f'…{i+1}/{len(jobs)} new={new}',flush=True)
    good=[p.stem+'.bin' for p in OUT.glob('*.txt') if p.name!='RECOVERED_IDS.txt' and ok_text(p.read_text())]
    Path(OUT/'RECOVERED_IDS.txt').write_text('\n'.join(sorted(good))+'\n')
    print('new',new,'total',len(good))
if __name__=='__main__': main()
