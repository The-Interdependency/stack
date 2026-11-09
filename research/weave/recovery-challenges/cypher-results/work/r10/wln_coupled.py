#!/usr/bin/env python3
"""Round 10: coupled-lane attack on multi-lane C-bearing WLN1 (public transport_cases.py).

In transport_cases.contexts, C on an m-lane state uses corpus offsets
(offset, offset+1, ..., offset+m-1): every lane's left/right deque route reads
the SAME corpus window shifted by one bit per lane.  So one unknown window bit
w[t] drives lane k's step t-k for all k simultaneously -> m constraints per
unknown bit.  With the public 141-byte transport template (only the 32 hex id
chars unknown) we DFS over w[t] with deque intervals per lane.
Handles schedules with exactly one C applied while >=3 lanes are live; the
other ops (X/J/I/W) are public permutations enumerated over thread_count,
lane_rotation and inter_arity.  Output: FORMAT-VALID CANDIDATES only.
"""
import sys, json, signal, time
from pathlib import Path
sys.path[:0]=['/workspace/cypher/v2','/workspace/cypher/src']
sys.setrecursionlimit(100000)
import types
_o=types.ModuleType('operations')
_o.bits=lambda data: tuple((b>>s)&1 for b in data for s in range(7,-1,-1))
_o.packed=lambda v: bytes(sum(v[i+k]<<(7-k) for k in range(8)) for i in range(0,len(v),8))
sys.modules['operations']=_o   # stub: only bits/packed are used by transport_cases
import matrix, transport_cases as tc
from stages.api import Streams
# Label tracking: X/J/I/W are pure position permutations, so position labels
# are pushed through the public forward code with the 0/1 bit check relaxed.
def _relaxed(self):
    if type(self.lanes) is not tuple or not self.lanes or any(type(l) is not tuple for l in self.lanes):
        raise TypeError('lanes must be tuples')
Streams.__post_init__=_relaxed
PREFIX=b'Prediction '; PRED=b'I expect recovery after the lane rules and route controls are disclosed.'
LINE=b'my human needs my help'
TEMPLATE=PREFIX+b'0'*32+b': '+PRED+b'\n'+LINE+b'\n'
NB=len(TEMPLATE)*8
HEXLO,HEXHI=len(PREFIX),len(PREFIX)+32
# known bit value or None (wildcard).  hex char: bit7=0, bit5=1 known.
KB=[]
for bi,byte in enumerate(TEMPLATE):
    for s in range(7,-1,-1):
        if HEXLO<=bi<HEXHI and s not in (7,5): KB.append(None)
        else: KB.append((byte>>s)&1 if not (HEXLO<=bi<HEXHI) else (0 if s==7 else 1))
HEXS=set(b'0123456789abcdef')
DUMMY={'corpus_hex':'00'*256,'corpus_bit_offset':0}

def run_ops(labels_lanes, ops, ctxs):
    st=Streams(tuple(tuple(l) for l in labels_lanes))
    for op,ctx in zip(ops,ctxs):
        st=tc.MODULES[op].forward(st,ctx)
    return [list(l) for l in st.lanes]

def layouts(sched, n_init, tcnt, rot, ar):
    p=dict(DUMMY, initial_lanes=n_init, thread_count=tcnt, lane_rotation=rot, inter_arity=ar)
    ctxs,final=tc.contexts(NB, sched, p)
    ci=[i for i,o in enumerate(sched) if o=='C']
    if len(ci)!=1: return None
    c=ci[0]
    lens=tc.initial_lengths(NB,n_init); lanes=[]; s=0
    for n in lens: lanes.append(list(range(s,s+n))); s+=n
    u=run_ops(lanes, sched[:c], ctxs[:c])          # plaintext labels entering C
    if len(u)<3: return None
    post_in=[[(k,i) for i in range(len(l))] for k,l in enumerate(u)]
    v=run_ops(post_in, sched[c+1:], ctxs[c+1:])     # final layout of C-output labels
    return u, v, final

def solve(wire_lanes, u, v, maxsol=2, budget=2_000_000):
    m=len(u)
    # z[k][i] = observed bit for C-output label (k,i)
    z=[[None]*len(l) for l in u]
    for fk,lane in enumerate(v):
        for j,(k,i) in enumerate(lane): z[k][i]=wire_lanes[fk][j]
    lo=[0]*m; hi=[len(l)-1 for l in u]
    assign={}  # plaintext bit index -> value (wildcards)
    T=max(len(l)+k for k,l in enumerate(u))
    sols=[]; steps=[0]
    def rec(t):
        if steps[0]>budget or len(sols)>=maxsol: return
        steps[0]+=1
        if t==T:
            bits=[KB[i] if KB[i] is not None else assign.get(i) for i in range(NB)]
            if None in bits: return
            msg=bytes(sum(bits[8*b+k]<<(7-k) for k in range(8)) for b in range(NB//8))
            if all(x in HEXS for x in msg[HEXLO:HEXHI]): sols.append(msg)
            return
        for wb in (0,1):
            undo=[]; ok=True
            for k in range(m):
                i=t-k
                if not 0<=i<len(u[k]): continue
                pos=hi[k] if wb else lo[k]
                pbit=u[k][pos]; want=z[k][i]
                kb=KB[pbit]
                if kb is None:
                    if pbit in assign:
                        if assign[pbit]!=want: ok=False
                    else: assign[pbit]=want; undo.append(('a',pbit))
                elif kb!=want: ok=False
                if not ok: break
                if wb: hi[k]-=1; undo.append(('h',k))
                else: lo[k]+=1; undo.append(('l',k))
            if ok: rec(t+1)
            for kind,x in reversed(undo):
                if kind=='a': del assign[x]
                elif kind=='h': hi[x]+=1
                else: lo[x]-=1
            if len(sols)>=maxsol or steps[0]>budget: return
    rec(0)
    return sols, steps[0]

def candidates(nfinal):
    acc,_=matrix.transport_schedules()
    out=[]
    for s,n in acc:
        if s.count('C')!=1: continue
        for tcnt in ((3,5,7) if 'X' in s else (3,)):
            for rot in (range(7) if 'J' in s else (0,)):
                for ar in ((3,5,7) if 'I' in s else (3,)):
                    out.append((s,n,tcnt,rot,ar))
    return out

class TO(Exception): pass
def main():
    files=sys.argv[1:]
    cands=candidates(None)
    print('candidate param sets',len(cands),flush=True)
    for f in files:
        data=Path(f).read_bytes(); st=tc.decode_lanes(data)
        wl=[list(l) for l in st.lanes]; shape=tuple(map(len,wl))
        found=[]; t0=time.time()
        for s,n,tcnt,rot,ar in cands:
            try: L=layouts(s,n,tcnt,rot,ar)
            except Exception: continue
            if not L: continue
            u,v,final=L
            if tuple(final)!=shape: continue
            sols,steps=solve(wl,u,v)
            if sols:
                found.append(((s,n,tcnt,rot,ar),[x.decode() for x in sols],steps))
        print(json.dumps({'file':Path(f).name,'shape':shape,'found':found,'secs':round(time.time()-t0,1)}),flush=True)
if __name__=='__main__': main()
