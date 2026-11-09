#!/usr/bin/env python3
"""Round 10: event-driven coupled solver for C-bearing WLN1 with 1..3 C stages.

All C applications in one case read the same corpus window: a single-lane C
uses w[i]; an m-lane C uses w[k+i] for lane k (transport_cases.contexts).  We
DFS over window bits w[t]; each C stage-lane keeps a deque interval, so
r[stage][lane][i] becomes known at t=k+i.  Every final wire bit is traced
backwards through the public X/J/I/W permutations and the C routes; when the
trace completes it must match the 141-byte public template (hex id bits are
wildcards, bound on first use).  A candidate is accepted ONLY if the DFS
finishes exhaustively (within budget) with exactly one distinct message.
"""
import sys, json, time
from pathlib import Path
sys.path.insert(0,'/workspace/cypher/work/r10')
import wln_coupled as W   # reuses public-module imports, template, label tracking
tc=W.tc; NB=W.NB; KB=W.KB
sys.setrecursionlimit(1000000)

def build(sched, n_init, tcnt, rot, ar):
    p=dict(W.DUMMY, initial_lanes=n_init, thread_count=tcnt, lane_rotation=rot, inter_arity=ar)
    ctxs,final=tc.contexts(NB, sched, p)
    cpos=[i for i,o in enumerate(sched) if o=='C']
    if not cpos: return None
    lens=tc.initial_lengths(NB,n_init); lanes=[]; s=0
    for n in lens: lanes.append(list(range(s,s+n))); s+=n
    seg0=W.run_ops(lanes, sched[:cpos[0]], ctxs[:cpos[0]])    # C1 input: plaintext idx
    stages=[]   # per C stage: lane sizes, and 'src' = for each input pos (k,p) its origin
    prev_in=seg0; src=('pt',seg0)
    for a,c in enumerate(cpos):
        sizes=[len(l) for l in prev_in]
        stages.append({'sizes':sizes,'src':src})
        nxt=cpos[a+1] if a+1<len(cpos) else len(sched)
        lab=[[(a,k,i) for i in range(n)] for k,n in enumerate(sizes)]
        out=W.run_ops(lab, sched[c+1:nxt], ctxs[c+1:nxt])
        prev_in=out; src=('c',out)
    final_lab=prev_in   # final wire position -> (stage,k,i) label of last C output
    return stages, final_lab, tuple(final)

def solve(wire, stages, final_lab, maxsol=2, budget=3_000_000):
    q=len(stages)
    R=[[[None]*n for n in st['sizes']] for st in stages]
    lo=[[0]*len(st['sizes']) for st in stages]
    hi=[[n-1 for n in st['sizes']] for st in stages]
    waiters={}  # (a,k,i) -> list of (want_bit)
    assign={}
    T=max(k+n for st in stages for k,n in enumerate(st['sizes']))
    jobs=[]
    for f,lane in enumerate(final_lab):
        for j,lab in enumerate(lane): jobs.append((lab, wire[f][j]))
    def trace(lab):
        # lab=(a,k,i) output label of stage a; return ('pt',idx) or ('wait',key)
        while True:
            a,k,i=lab
            p=R[a][k][i]
            if p is None: return ('wait',lab)
            kind,tab=stages[a]['src']
            v=tab[k][p]
            if kind=='pt': return ('pt',v)
            lab=v
    sols=set(); steps=[0]; exhausted=[False]
    def check(lab,want,undo):
        r=trace(lab)
        if r[0]=='wait':
            waiters.setdefault(r[1],[]).append((lab,want)); undo.append(('w',r[1])); return True
        idx=r[1]; kb=KB[idx]
        if kb is None:
            if idx in assign: return assign[idx]==want
            assign[idx]=want; undo.append(('a',idx)); return True
        return kb==want
    def rollback(undo):
        for kind,x in reversed(undo):
            if kind=='a': del assign[x]
            elif kind=='w': waiters[x].pop()
            elif kind=='r': a,k,i,wb=x; R[a][k][i]=None; (hi[a].__setitem__(k,hi[a][k]+1) if wb else lo[a].__setitem__(k,lo[a][k]-1))
            elif kind=='W': waiters[x[0]]=x[1]
    root=[]
    for lab,want in jobs:
        if not check(lab,want,root): return [],0,True
    def rec(t):
        steps[0]+=1
        if steps[0]>budget: exhausted[0]=True; return
        if len(sols)>=maxsol: return
        if t==T:
            bits=[KB[i] if KB[i] is not None else assign.get(i) for i in range(NB)]
            if None in bits: return
            msg=bytes(sum(bits[8*b+x]<<(7-x) for x in range(8)) for b in range(NB//8))
            if all(c in W.HEXS for c in msg[W.HEXLO:W.HEXHI]): sols.add(msg)
            return
        for wb in (0,1):
            undo=[]; ok=True
            for a,st in enumerate(stages):
                m=len(st['sizes'])
                for k in range(m):
                    i=t-k if m>1 else t
                    if not 0<=i<st['sizes'][k]: continue
                    pos=hi[a][k] if wb else lo[a][k]
                    R[a][k][i]=pos
                    if wb: hi[a][k]-=1
                    else: lo[a][k]+=1
                    undo.append(('r',(a,k,i,wb)))
                    key=(a,k,i)
                    ws=waiters.get(key)
                    if ws:
                        waiters[key]=[]; undo.append(('W',(key,ws)))
                        for lab,want in ws:
                            if not check(lab,want,undo): ok=False; break
                    if not ok: break
                if not ok: break
            if ok: rec(t+1)
            rollback(undo)
            if len(sols)>=maxsol or exhausted[0]: return
    rec(0)
    return sorted(sols), steps[0], exhausted[0]

def candidates():
    acc,_=W.matrix.transport_schedules()
    for s,n in acc:
        if 'C' not in s: continue
        for tcnt in ((3,5,7) if 'X' in s else (3,)):
            for rot in (range(7) if 'J' in s else (0,)):
                for ar in ((3,5,7) if 'I' in s else (3,)):
                    yield (s,n,tcnt,rot,ar)

def main():
    budget=int(sys.argv[1]); files=sys.argv[2:]
    built=[]
    for c in candidates():
        try: b=build(*c)
        except Exception: continue
        if b: built.append((c,b))
    print('param sets',len(built),flush=True)
    for f in files:
        st=tc.decode_lanes(Path(f).read_bytes()); wl=[list(l) for l in st.lanes]; shape=tuple(map(len,wl))
        res=[]; t0=time.time()
        for c,(stages,final_lab,final) in built:
            if final!=shape: continue
            sols,steps,exh=solve(wl,stages,final_lab,budget=budget)
            if sols or exh: res.append({'sched':''.join(c[0]),'init':c[1],'t':c[2],'rot':c[3],'ar':c[4],'nsol':len(sols),'exhausted':exh,'steps':steps,'sols':[x.decode() for x in sols]})
        print(json.dumps({'file':Path(f).name,'shape':shape,'res':res,'secs':round(time.time()-t0,1)}),flush=True)
if __name__=='__main__': main()
