"""Finite residue and prime census research. See PROTOCOL.md and README.md.

Usage: python experiment.py --limit 60000000 --output evidence.json
       python experiment.py --timing timing.json
No cipher, secret-key recovery tool, network access, or security assertion.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from math import isqrt
from pathlib import Path
import platform
from statistics import median
from time import perf_counter_ns

M = 3**9
STEP = 81
SECTOR = M // 3
SPLIT = 30_000_000


def eligible(exponent: int) -> range:
    if type(exponent) is not int or exponent < 1:
        raise ValueError('positive integer exponent required')
    return range(0, 3**exponent, 3**(exponent//2))


def pair_cubes(c: int, modulus: int = M) -> tuple[int, int]:
    if type(c) is not int or type(modulus) is not int or modulus <= 1:
        raise ValueError('integer midpoint and modulus > 1 required')
    return pow(c - 1, 3, modulus), pow(c + 1, 3, modulus)


def bearing(c: int, modulus: int = M) -> int:
    return 3*c % modulus


def exact_sector(c: int) -> int:
    if type(c) is not int or c not in eligible(9):
        raise ValueError('eligible canonical midpoint required')
    return c // SECTOR


def retained_label_roundtrip(y: int, sector: int) -> int:
    """Decode an explicitly retained sector label; purely positional arithmetic."""
    if type(y) is not int or y < 0 or y >= M or y % (STEP*3):
        raise ValueError('eligible output bearing required')
    if type(sector) is not int or not 0 <= sector < 3:
        raise ValueError('sector must be 0, 1, or 2')
    return y//3 + sector*SECTOR


def partition(items, observation):
    """Group mathematical objects by their declared finite observation."""
    groups = defaultdict(list)
    for item in items:
        groups[observation(item)].append(item)
    return tuple(tuple(group) for group in groups.values())


def summarize(groups) -> dict:
    sizes = Counter(map(len, groups))
    return {'classes': len(groups), 'size_histogram': dict(sorted(sizes.items())),
            'colliding_classes': sum(v for k, v in sizes.items() if k > 1),
            'max_size': max(sizes, default=0), 'objects': sum(k*v for k,v in sizes.items())}


def same_partition(first, second) -> bool:
    return {frozenset(g) for g in first} == {frozenset(g) for g in second}


def refines(first, second) -> bool:
    """True if first is a refinement of second."""
    labels = {item: i for i, g in enumerate(second) for item in g}
    return all(len({labels[item] for item in g}) <= 1 for g in first)


def geometry_report() -> dict:
    domain = eligible(9)
    mismatch = []
    for c in range(M):
        a,b = pair_cubes(c)
        direct = (b-a) % M == 2
        predicted = c % STEP == 0
        if direct != predicted or (direct and (a,b) != ((3*c-1)%M,(3*c+1)%M)):
            mismatch.append(c)
    base = partition(domain, bearing)
    radius = {
        'bearing_only': summarize(base),
        'constant_radius': summarize(partition(domain, lambda c:(bearing(c),Fraction(1)))),
        'bearing_dependent_radius': summarize(partition(domain, lambda c:(bearing(c),1+Fraction(bearing(c),M)))),
        'two_explicit_radial_layers': summarize(partition(domain, lambda c:(bearing(c),1+Fraction(exact_sector(c)//2,3)))),
        'three_explicit_radial_layers': summarize(partition(domain, lambda c:(bearing(c),1+Fraction(exact_sector(c),3)))),
        'bearing_repeated': summarize(partition(domain, lambda c:(bearing(c),bearing(c)))),
        'identity_control': summarize(partition(domain,lambda c:c)),
        'constant_control': summarize(partition(domain,lambda c:0)),
    }
    retained_ok = sum(retained_label_roundtrip(bearing(c),exact_sector(c)) == c for c in domain)
    wrong_labels_equal = sum(retained_label_roundtrip(bearing(c),j)==c for c in domain for j in range(3) if j!=exact_sector(c))
    mods = {}
    for m in (2,3,81,243,157,6561,19683,19685):
        mods[str(m)] = {
            'canonical_midpoint_observation': summarize(partition(domain,lambda c:(bearing(c),c%m))),
            'transformed_midpoint_observation': summarize(partition(domain,lambda c:(bearing(c),bearing(c,m)))),
        }
    depth = {str(d):summarize(partition(domain,lambda c:pow(3,d,M)*c % M)) for d in range(8)}
    pairs = tuple((c,81) for c in domain)
    vector = partition(pairs,lambda p:(bearing(p[0]),bearing(p[1])))
    swapped = partition(pairs,lambda p:(bearing(p[1]),bearing(p[0])))
    omitted = partition(pairs,lambda p:bearing(p[1]))
    sample = tuple(domain)[:81]
    independent = tuple((c,d) for c in domain for d in domain)
    iv = partition(independent,lambda p:(bearing(p[0]),bearing(p[1])))
    iv_swap = partition(independent,lambda p:(bearing(p[1]),bearing(p[0])))
    iv_omit = partition(independent,lambda p:bearing(p[1]))
    return {'modulus':M,'eligible_step':STEP,'eligible_residues':len(domain),
            'exhaustive_direct_cube_checks':M,'cube_mismatch_count':len(mismatch),
            'first_cube_mismatch':mismatch[0] if mismatch else None,
            'worked_examples':[{'midpoint':c,'input_spoke':c%M,'cubes':pair_cubes(c),'output_spoke':bearing(c)} for c in (46818,73062,178038)],
            'radius_and_controls':radius,'retained_label':{'correct':retained_ok,'total':len(domain),'wrong_labels':len(domain)*2,'wrong_labels_equal_original':wrong_labels_equal},
            'moduli':mods,'recursion':depth,
            'interlacing_control':{'two_coordinate_vector':summarize(vector),'fixed_swap':summarize(swapped),'omit_first_coordinate':summarize(omitted),'swap_preserves_partition':same_partition(vector,swapped),'omission_only_coarsens':refines(vector,omitted),'first_81_eligible_residues_forward_labels': [bearing(c) for c in sample],
            'independent_product':{'two_coordinate_vector':summarize(iv),'fixed_swap':summarize(iv_swap),'omit_first_coordinate':summarize(iv_omit),'swap_preserves_partition':same_partition(iv,iv_swap),'omission_only_coarsens':refines(iv,iv_omit)}}}


def odd_sieve(limit: int) -> bytearray:
    """flags[i] records primality of odd number 2*i+1, through limit inclusive."""
    if type(limit) is not int or limit < 5:
        raise ValueError('integer limit >= 5 required')
    flags = bytearray(b'\x01')*((limit+1)//2)
    flags[0] = 0
    for p in range(3,isqrt(limit)+1,2):
        if flags[p//2]:
            start = p*p//2
            count = (len(flags)-1-start)//p+1
            flags[start::p] = b'\x00'*count
    return flags


def twin_records(limit: int):
    """Emit (midpoint, lower prime ordinal) for consecutive twin pairs above 3."""
    flags = odd_sieve(limit)
    i = flags.find(b'\x01',1)
    ordinal, previous = 1, 2
    while i != -1:
        p = 2*i+1
        ordinal += 1
        if p-previous == 2 and previous > 3:
            yield (p-1,ordinal-1)
        previous = p
        i = flags.find(b'\x01',i+1)


class Census:
    """Aggregate empirical frequencies, without inferring unobserved prime values."""
    def __init__(self):
        self.twin_count = self.eligible_count = self.direct_mismatches = 0
        self.first_mismatch = None
        self.original, self.input, self.output = set(),set(),set()
        self.last = [None]*3
        self.counts = defaultdict(lambda:[0,0,0])
        self.ordinal_labels = {q:defaultdict(set) for q in (3,9,27)}
        self.ordinal_differences = Counter()
        self.eligible_pairs = []

    def add(self,c,rank):
        self.twin_count += 1
        r = c % M
        if r not in self.original:
            self.original.add(r)
            self.last[0] = c+1
        a,b = pair_cubes(c)
        direct = (b-a)%M == 2
        formula = c%STEP == 0
        if direct != formula or (direct and (a,b)!=((3*c-1)%M,(3*c+1)%M)):
            self.direct_mismatches += 1
            if self.first_mismatch is None:
                self.first_mismatch=c
        if not formula:
            return
        self.eligible_count += 1
        y=bearing(c)
        if r not in self.input:
            self.input.add(r)
            self.last[1]=c+1
        if y not in self.output:
            self.output.add(y)
            self.last[2]=c+1
        self.counts[y][exact_sector(r)] += 1
        for q in self.ordinal_labels:
            self.ordinal_labels[q][(y,rank%q)].add(r)
        # Twin primes above 3 are consecutive. Rank difference = 1.
        self.ordinal_differences[1] += 1
        if len(self.eligible_pairs) < 81:
            self.eligible_pairs.append((r,y))

    def report(self):
        rows = [{'output_spoke':y,'family_counts':self.counts[y], 'total':sum(self.counts[y])} for y in sorted(self.counts)]
        pairs = tuple(self.eligible_pairs)
        original_vector = tuple((r,y) for r,y in pairs)
        swapped_vector = tuple((y,r) for r,y in pairs)
        return {'twin_pairs':self.twin_count,'eligible_pairs':self.eligible_count,
                'direct_cube_mismatches':self.direct_mismatches,'first_direct_mismatch':self.first_mismatch,
                'spokes':{'original':len(self.original),'eligible_input':len(self.input),'output':len(self.output)},
                'upper_prime_last_new_spoke':dict(zip(('original','eligible_input','output'),self.last)),
                'all_output_families':rows,
                'ordinal_label_count_unit':'distinct (output spoke, lower ordinal residue, input midpoint residue) incidences',
                'ordinal_labels': {str(q):summarize(groups.values()) for q,groups in self.ordinal_labels.items()},
                'ordinal_difference_counts':dict(self.ordinal_differences),
                'fixed_public_label_vector_control':{'first_pairs':original_vector,'coordinate_swap_roundtrip':tuple((r,y) for y,r in swapped_vector)==original_vector},
                'family_count_range':[min((v for r in rows for v in r['family_counts']),default=0),max((v for r in rows for v in r['family_counts']),default=0)],
                'output_count_range':[min((r['total'] for r in rows),default=0),max((r['total'] for r in rows),default=0)]}


def census_report(limit):
    prior,next_period=Census(),Census()
    crossing=[]
    for c,rank in twin_records(limit):
        if c+1<=SPLIT:
            prior.add(c,rank)
        elif c-1>SPLIT:
            next_period.add(c,rank)
        else:
            a,b=pair_cubes(c)
            gap=(b-a)%M
            crossing.append({'primes':[c-1,c+1],'lower_ordinal':rank,'cubes':[a,b],'forward_gap':gap,'formula_agrees':(gap==2)==(c%STEP==0) and (gap!=2 or (a,b)==((3*c-1)%M,(3*c+1)%M))})
    return {'limit_inclusive':limit,'split':SPLIT,'excluded_crossing_pairs':len(crossing),'crossing_witnesses':crossing,
            'first_interval':prior.report(),'next_interval':next_period.report()}


def scaling_report():
    rows=[]
    for a in (5,7,9,11,13,15):
        domain=eligible(a); modulus=3**a
        runs=[]
        for _ in range(9):
            start=perf_counter_ns()
            groups=partition(domain,lambda c:bearing(c,modulus))
            summary=summarize(groups)
            runs.append(perf_counter_ns()-start)
        rows.append({'exponent':a,'modulus':modulus,**summary,'median_ns':int(median(runs)), 'nine_runs_ns':runs})
    return {'method':'elapsed wall-clock forward bearing + partition summary (not inversion)', 'python':platform.python_version(),'platform':platform.platform(),'processor':platform.processor(),'rows':rows}


def deterministic_report(limit):
    return {'schema':'base27-mathematical-replay/1','protocol_sha256':sha256(Path(__file__).with_name('PROTOCOL.md').read_bytes()).hexdigest(),
            'addendum_sha256':sha256(Path(__file__).with_name('PROTOCOL_ADDENDUM.md').read_bytes()).hexdigest(),
            'implementation_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'geometry':geometry_report(),'prime_census':census_report(limit),
            'standing':'local mathematical evidence only','cryptographic_security':'NOT_TESTED'}


def write_json(path,data):
    with Path(path).open('x',encoding='utf-8') as f:
        f.write(json.dumps(data,indent=2,sort_keys=True)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int,default=60_000_000)
    parser.add_argument('--output')
    parser.add_argument('--timing')
    args=parser.parse_args()
    if bool(args.output)==bool(args.timing):
        parser.error('specify exactly one of --output or --timing')
    if args.output:
        write_json(args.output,deterministic_report(args.limit))
    else:
        write_json(args.timing,scaling_report())

if __name__=='__main__':
    main()
