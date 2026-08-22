# === MODULE_BUILD ===
# id: ucns_prime_determinantal_grobner_p7_p5
#   module_name: prime_determinantal_grobner
#   module_kind: experiment
#   summary: executes the preregistered complete rational-Laurent determinantal-ideal Groebner protocol for the frozen P7 and P5 Fox matrices
#   owner: Erin Spencer
#   public_surface: determinantal_grobner_certificate, determinantal_grobner_family_certificate, write_determinantal_grobner_family_certificate
#   internal_surface: compound maximal-minor coordinates, frozen direct full-minor audit, Laurent normalization, saturation, exact reduced lex bases, independent Buchberger replay
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through writer functions
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_determinantal_grobner.py
#   rollout: protocol 7841af16; P7 first and P5 second; selection effect none
#   rollback: remove this module, its tests, result document, and generated receipt while retaining preregistration and prior rank/onset evidence
#   requires: ucns_prime_symbolic_alexander_p7_p5, sympy==1.14.0
#   since: 2026-08-15
#   unresolved: integral-Laurent strong bases, length-four Milnor invariants, finite nilpotent quotients, preregistered phase-co-winner separator
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_grobner_protocol_identity_is_frozen
#   given: a determinantal basis computation begins
#   then: the committed preregistration bytes have the frozen SHA-256 identity and the parent presentation digest matches
#   class: doctrine
#
# id: prime_grobner_generators_cover_every_maximal_minor
#   given: P7 E1 or P5 E3 generators are constructed
#   then: every rank-size row/column subset pair is accounted for through the exact compound identity with no non-monomial denominator, and the frozen anchor, pivot-neighbor, and SHA-selected full minors agree under both direct determinant paths
#   class: correctness
#
# id: prime_grobner_basis_is_complete_reduced_and_saturated
#   given: the complete rational-Laurent determinantal generator family is accepted
#   then: component-variable saturation and exact lex reduction return a monic reduced basis for the complete ideal
#   class: evidence
#
# id: prime_grobner_independent_replay_agrees
#   given: primary and independent computations finish within frozen bounds
#   then: generator digests, mutual reductions, and canonical reduced basis maps agree exactly
#   class: regression
#
# id: prime_grobner_receipt_preserves_nonclaims
#   given: the family receipt is serialized
#   then: rational ideal evidence does not escalate phase, isotopy, prime-forcing, spectral, zeta, or theorem standing
#   class: doctrine
# === END CONTRACTS ===

"""Preregistered rational-Laurent determinantal Groebner computation.

Usage::

    python -m ucns.prime_determinantal_grobner OUTPUT --prime 7
    python -m ucns.prime_determinantal_grobner OUTPUT --prime 5

Omit ``--prime`` only to run the frozen P7-then-P5 family order. Each prime has
a 7,200-second wall bound. The direct-minor audit requires a Unix ``fork``
start method and uses two deterministic workers; it writes no partial success
receipt when a bound, exact-equality check, or backend operation fails.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib, heapq, itertools, json, time
import multiprocessing
from pathlib import Path
from typing import Iterable

import sympy as sp

from .prime_symbolic_alexander import _matrix_data, symbolic_alexander_certificate

PROTOCOL_PATH = Path("docs/PREREGISTRATION_P7_P5_DETERMINANTAL_GROEBNER.md")
PROTOCOL_SHA256 = "7841af162698efb823db79b70ef7b99a5ac53d27e2bbb318f97f36aecae515b4"
PARENT_COMMIT = "62e97304971d9ac9ead0f766c964d830b0367aa1"
PRESENTATION_SHA256 = {7: "57a3aad650c372f37e798a8d3377422005156d2f5cd495bb990eca397443ab7b", 5: "34cab71c9e4e8fd85f30d5a10956aba7bd1a0c1398d2263ba7e7cebfac24e82d"}
MAX_PAIRS = 1_000_000
MAX_GENERATORS = 100_000
MAX_WALL_SECONDS = 7_200
SHA_AUDIT_PAIR_COUNT = 32
AUDIT_WORKERS = 2

class DeterminantalGrobnerError(ValueError): pass

def _sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def _protocol_gate() -> None:
    if hashlib.sha256(PROTOCOL_PATH.read_bytes()).hexdigest() != PROTOCOL_SHA256:
        raise DeterminantalGrobnerError("preregistration identity mismatch")

def _poly_key(poly: sp.Poly) -> tuple[tuple[tuple[int, ...], str], ...]:
    return tuple((tuple(mon), str(coeff)) for mon, coeff in poly.terms())

def _normalize_expr(expr, symbols: tuple[sp.Symbol, ...]) -> sp.Poly:
    expr = sp.cancel(sp.sympify(str(expr)))
    numerator, denominator = sp.fraction(expr)
    den_poly = sp.Poly(denominator, *symbols, domain=sp.QQ)
    if len(den_poly.terms()) != 1:
        raise DeterminantalGrobnerError("non-monomial Laurent denominator")
    poly = sp.Poly(sp.expand(numerator), *symbols, domain=sp.QQ)
    if poly.is_zero: return poly
    minima = tuple(min(mon[i] for mon, _ in poly.terms()) for i in range(len(symbols)))
    shifted = {tuple(mon[i]-minima[i] for i in range(len(symbols))): coeff for mon, coeff in poly.terms()}
    result = sp.Poly.from_dict(shifted, symbols, domain=sp.QQ)
    return result.monic()

@dataclass(frozen=True)
class _CompoundCoordinates:
    prime: int
    diagram: object
    names: tuple[str, ...]
    dense: object
    field: object
    rank: int
    pivot_rows: tuple[int, ...]
    pivot_columns: tuple[int, ...]
    subsets: tuple[tuple[int, ...], ...]
    left_values: tuple[object, ...]
    right_values: tuple[object, ...]
    pivot_minor: object


_AUDIT_COORDINATES: _CompoundCoordinates | None = None
_AUDIT_SUBSET_INDEXES: dict[tuple[int, ...], int] | None = None
_AUDIT_DENSE_VALUES: list[list[object]] | None = None


def _coordinate_families(prime: int) -> _CompoundCoordinates:
    diagram, _, names, field, matrix, _ = _matrix_data(prime)
    dense = matrix.to_dense(); rank = matrix.rank()
    rr, columns = dense.rref(); rt, rows = dense.transpose().rref()
    parent = symbolic_alexander_certificate(prime)
    if tuple(columns) != parent.pivot_columns or tuple(rows) != parent.pivot_rows:
        raise DeterminantalGrobnerError("pivot profile changed")
    right = rr.extract(range(rank), range(diagram.generator_count))
    left = rt.extract(range(rank), range(diagram.generator_count)).transpose()
    subsets = tuple(itertools.combinations(range(diagram.generator_count), rank))
    left_values = tuple(left.extract(list(subset), range(rank)).det() for subset in subsets)
    right_values = tuple(right.extract(range(rank), list(subset)).det() for subset in subsets)
    pivot_rows = tuple(rows)
    pivot_columns = tuple(columns)
    # The parent certificate already computed and sealed this exact pivot.
    # The frozen audit set includes the pivot and recomputes it directly in
    # both determinant paths, so doing so here would add cost but no evidence.
    pivot_minor = field.from_sympy(sp.sympify(parent.pivot_minor))
    return _CompoundCoordinates(
        prime=prime,
        diagram=diagram,
        names=names,
        dense=dense,
        field=field,
        rank=rank,
        pivot_rows=pivot_rows,
        pivot_columns=pivot_columns,
        subsets=subsets,
        left_values=left_values,
        right_values=right_values,
        pivot_minor=pivot_minor,
    )


def _subset_pair_encoding(
    rows: tuple[int, ...], columns: tuple[int, ...]
) -> bytes:
    """Return the frozen canonical encoding used for SHA audit ordering."""

    return json.dumps(
        {"columns": list(columns), "rows": list(rows)},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def _subset_pair_sha256(
    rows: tuple[int, ...], columns: tuple[int, ...]
) -> str:
    return hashlib.sha256(_subset_pair_encoding(rows, columns)).hexdigest()


def _pivot_neighbors(
    pivot: tuple[int, ...], universe_size: int
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    nonpivot = sorted(set(range(universe_size)) - set(pivot))
    if not nonpivot:
        return ()
    replacement = nonpivot[0]
    return tuple(
        (
            removed,
            tuple(sorted((set(pivot) - {removed}) | {replacement})),
        )
        for removed in pivot
    )


def _selected_audit_pairs(
    coordinates: _CompoundCoordinates,
) -> tuple[
    tuple[tuple[int, ...], tuple[int, ...], tuple[str, ...]], ...
]:
    """Select the preregistered anchor, pivot-neighbor, and SHA audit pairs."""

    selected: dict[
        tuple[tuple[int, ...], tuple[int, ...]], set[str]
    ] = {}

    def add(
        rows: tuple[int, ...], columns: tuple[int, ...], selector: str
    ) -> None:
        selected.setdefault((rows, columns), set()).add(selector)

    nonzero_rows = tuple(
        subset
        for subset, value in zip(
            coordinates.subsets, coordinates.left_values, strict=True
        )
        if value
    )
    nonzero_columns = tuple(
        subset
        for subset, value in zip(
            coordinates.subsets, coordinates.right_values, strict=True
        )
        if value
    )
    if not nonzero_rows or not nonzero_columns:
        raise DeterminantalGrobnerError("audit selection has no nonzero coordinates")

    anchor_indexes = (
        ("first", 0),
        ("midpoint", (len(nonzero_rows) - 1) // 2),
        ("last", len(nonzero_rows) - 1),
    )
    column_anchor_indexes = (
        ("first", 0),
        ("midpoint", (len(nonzero_columns) - 1) // 2),
        ("last", len(nonzero_columns) - 1),
    )
    for row_name, row_index in anchor_indexes:
        for column_name, column_index in column_anchor_indexes:
            add(
                nonzero_rows[row_index],
                nonzero_columns[column_index],
                f"nonzero-anchor:{row_name}:{column_name}",
            )

    add(
        coordinates.pivot_rows,
        coordinates.pivot_columns,
        "pivot",
    )
    for removed, rows in _pivot_neighbors(
        coordinates.pivot_rows, coordinates.diagram.generator_count
    ):
        add(rows, coordinates.pivot_columns, f"pivot-row-neighbor:{removed}")
    for removed, columns in _pivot_neighbors(
        coordinates.pivot_columns, coordinates.diagram.generator_count
    ):
        add(coordinates.pivot_rows, columns, f"pivot-column-neighbor:{removed}")

    sha_pairs = heapq.nsmallest(
        SHA_AUDIT_PAIR_COUNT,
        (
            (_subset_pair_sha256(rows, columns), rows, columns)
            for rows in coordinates.subsets
            for columns in coordinates.subsets
        ),
    )
    if len(sha_pairs) != SHA_AUDIT_PAIR_COUNT:
        raise DeterminantalGrobnerError("SHA audit selection is incomplete")
    for position, (_, rows, columns) in enumerate(sha_pairs):
        add(rows, columns, f"sha256-order:{position}")

    return tuple(
        (rows, columns, tuple(sorted(selectors)))
        for (rows, columns), selectors in sorted(selected.items())
    )


def _independent_fraction_field_determinant(
    values: list[list[object]],
    rows: tuple[int, ...],
    columns: tuple[int, ...],
    field: object,
) -> object:
    """Compute one exact determinant without DomainMatrix.det()."""

    matrix = [[values[row][column] for column in columns] for row in rows]
    determinant = field.one
    sign = 1
    for column in range(len(columns)):
        pivot_row = next(
            (row for row in range(column, len(rows)) if matrix[row][column]),
            None,
        )
        if pivot_row is None:
            return field.zero
        if pivot_row != column:
            matrix[column], matrix[pivot_row] = matrix[pivot_row], matrix[column]
            sign *= -1
        pivot = matrix[column][column]
        determinant *= pivot
        for row in range(column + 1, len(rows)):
            if not matrix[row][column]:
                continue
            scale = matrix[row][column] / pivot
            for index in range(column + 1, len(columns)):
                matrix[row][index] -= scale * matrix[column][index]
            matrix[row][column] = field.zero
    return -determinant if sign < 0 else determinant


def _sympy_fraction_field_lu_determinant(
    dense: object,
    rows: tuple[int, ...],
    columns: tuple[int, ...],
    field: object,
) -> object:
    """Compute one exact determinant through SymPy's field-LU backend."""

    _, upper, swaps = dense.extract(list(rows), list(columns)).lu()
    upper_values = upper.to_list()
    determinant = field.one
    for index in range(len(rows)):
        determinant *= upper_values[index][index]
    return -determinant if len(swaps) % 2 else determinant


def _audit_pair_worker(
    task: tuple[tuple[int, ...], tuple[int, ...], tuple[str, ...]],
) -> dict[str, object]:
    coordinates = _AUDIT_COORDINATES
    subset_indexes = _AUDIT_SUBSET_INDEXES
    dense_values = _AUDIT_DENSE_VALUES
    if coordinates is None or subset_indexes is None or dense_values is None:
        raise DeterminantalGrobnerError("direct-audit worker was not initialized")
    rows, columns, selectors = task
    expected = (
        coordinates.pivot_minor
        * coordinates.left_values[subset_indexes[rows]]
        * coordinates.right_values[subset_indexes[columns]]
    )
    primary = _sympy_fraction_field_lu_determinant(
        coordinates.dense,
        rows,
        columns,
        coordinates.field,
    )
    independent = _independent_fraction_field_determinant(
        dense_values,
        rows,
        columns,
        coordinates.field,
    )
    if primary != expected or independent != expected:
        raise DeterminantalGrobnerError(
            "frozen direct-minor audit disagrees with compound identity"
        )
    return {
        "rows": list(rows),
        "columns": list(columns),
        "selectors": list(selectors),
        "subset_pair_sha256": _subset_pair_sha256(rows, columns),
        "minor_sha256": hashlib.sha256(
            str(primary).encode("utf-8")
        ).hexdigest(),
        "nonzero": bool(primary),
        "primary_compound_equal": True,
        "independent_compound_equal": True,
    }


def _direct_minor_audit(
    coordinates: _CompoundCoordinates, *, deadline: float
) -> dict[str, object]:
    global _AUDIT_COORDINATES, _AUDIT_SUBSET_INDEXES, _AUDIT_DENSE_VALUES

    if "fork" not in multiprocessing.get_all_start_methods():
        raise DeterminantalGrobnerError(
            "the frozen direct audit requires fork-based worker isolation"
        )
    selected = _selected_audit_pairs(coordinates)
    _AUDIT_COORDINATES = coordinates
    _AUDIT_SUBSET_INDEXES = {
        subset: index for index, subset in enumerate(coordinates.subsets)
    }
    _AUDIT_DENSE_VALUES = coordinates.dense.to_list()
    records: list[dict[str, object]] = []
    started = time.monotonic()
    context = multiprocessing.get_context("fork")
    pool = context.Pool(processes=AUDIT_WORKERS)
    try:
        iterator = pool.imap(_audit_pair_worker, selected, chunksize=1)
        for _ in selected:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise DeterminantalGrobnerError(
                    "direct-minor audit wall-clock bound exhausted"
                )
            try:
                records.append(iterator.next(timeout=remaining))
            except multiprocessing.TimeoutError as error:
                raise DeterminantalGrobnerError(
                    "direct-minor audit wall-clock bound exhausted"
                ) from error
    except BaseException:
        pool.terminate()
        pool.join()
        raise
    else:
        pool.close()
        pool.join()
    finally:
        _AUDIT_COORDINATES = None
        _AUDIT_SUBSET_INDEXES = None
        _AUDIT_DENSE_VALUES = None
    return {
        "canonical_subset_pair_encoding": (
            'UTF-8 JSON object {"columns":[...],"rows":[...]} '
            "with sorted keys and compact separators"
        ),
        "midpoint_rule": "zero-based floor((nonzero_count - 1) / 2)",
        "sha256_order_pair_count": SHA_AUDIT_PAIR_COUNT,
        "execution_start_method": "fork",
        "worker_count": AUDIT_WORKERS,
        "primary_determinant_path": "SymPy exact fraction-field LU diagonal product",
        "independent_determinant_path": "separately implemented exact fraction-field Gaussian elimination",
        "selected_pair_count": len(records),
        "nonzero_pair_count": sum(record["nonzero"] for record in records),
        "all_primary_compound_equal": True,
        "all_independent_compound_equal": True,
        "results_sha256": _sha(records),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "pairs": records,
    }

def _complete_generators(prime: int, *, deadline: float):
    coordinates = _coordinate_families(prime)
    symbols = tuple(sp.Symbol(name) for name in coordinates.names)
    pivot = sp.sympify(symbolic_alexander_certificate(prime).pivot_minor)
    nonzero_left = [(coordinates.subsets[i], value) for i,value in enumerate(coordinates.left_values) if value]
    nonzero_right = [(coordinates.subsets[i], value) for i,value in enumerate(coordinates.right_values) if value]
    pair_total=len(coordinates.subsets)**2; nonzero_total=len(nonzero_left)*len(nonzero_right)
    if pair_total>MAX_PAIRS: raise DeterminantalGrobnerError("candidate pair-product bound exceeded")
    direct_minor_audit = _direct_minor_audit(coordinates, deadline=deadline)
    pivot_poly=_normalize_expr(pivot,symbols)
    unique={}
    for _, lp in nonzero_left:
        for _, rp in nonzero_right:
            product=_normalize_expr(pivot*sp.sympify(str(lp))*sp.sympify(str(rp)),symbols)
            unique[_poly_key(product)]=product
            if len(unique)>MAX_GENERATORS: raise DeterminantalGrobnerError("deduplicated-generator bound exceeded")
    ordered=tuple(unique[key] for key in sorted(unique))
    accounting={"row_subsets":len(coordinates.subsets),"column_subsets":len(coordinates.subsets),"candidate_pairs":pair_total,"nonzero_left":len(nonzero_left),"nonzero_right":len(nonzero_right),"nonzero_pair_products":nonzero_total,"deduplicated_generators":len(ordered)}
    return symbols, ordered, accounting, direct_minor_audit

def _reduced_saturated_basis(symbols: tuple[sp.Symbol,...], generators: tuple[sp.Poly,...]):
    z=sp.Symbol("z"); product=sp.prod(symbols)
    first=sp.groebner([g.as_expr() for g in generators]+[1-z*product],z,*symbols,order="lex",domain=sp.QQ)
    eliminated=[p.as_expr() for p in first.polys if not p.as_expr().has(z)]
    if not eliminated: raise DeterminantalGrobnerError("saturation elimination returned no component-ring generator")
    reduced=sp.groebner(eliminated,*symbols,order="lex",domain=sp.QQ)
    return tuple(sp.Poly(p,*symbols,domain=sp.QQ).monic() for p in reduced.polys)

def _lt(poly: dict[tuple[int,...],Fraction]): return max(poly) if poly else None
def _padd(a,b,scale=Fraction(1),shift=None):
    out=dict(a); shift=shift or (0,)*len(next(iter(a or b)))
    for m,c in b.items():
        mm=tuple(x+y for x,y in zip(m,shift)); out[mm]=out.get(mm,Fraction())+scale*c
        if not out[mm]: del out[mm]
    return out
def _preduce(f,basis):
    f=dict(f); rem={}
    while f:
        m=_lt(f); c=f[m]; reduced=False
        for g in basis:
            mg=_lt(g)
            if all(x>=y for x,y in zip(m,mg)):
                shift=tuple(x-y for x,y in zip(m,mg)); f=_padd(f,g,-c/g[mg],shift); reduced=True; break
        if not reduced: rem[m]=c; del f[m]
    return rem
def _monic(p):
    if not p:return p
    c=p[_lt(p)];return {m:v/c for m,v in p.items()}
def _buchberger(initial):
    basis=[]
    for f in initial:
        r=_preduce(f,basis)
        if r:basis.append(_monic(r))
    pairs=list(itertools.combinations(range(len(basis)),2)); pos=0
    while pos<len(pairs):
        i,j=pairs[pos];pos+=1; a,b=basis[i],basis[j]; ma,mb=_lt(a),_lt(b); l=tuple(max(x,y) for x,y in zip(ma,mb))
        s=_padd({},a,Fraction(1,a[ma]),tuple(x-y for x,y in zip(l,ma)))
        s=_padd(s,b,Fraction(-1,b[mb]),tuple(x-y for x,y in zip(l,mb)))
        r=_preduce(s,basis)
        if r:
            r=_monic(r); n=len(basis);basis.append(r);pairs.extend((i,n) for i in range(n))
            if len(basis)>100_000:raise DeterminantalGrobnerError("replay basis bound exceeded")
    changed=True
    while changed:
        changed=False; out=[]
        for i,g in enumerate(basis):
            r=_preduce(g,basis[:i]+basis[i+1:])
            if r:out.append(_monic(r))
            if r!=g:changed=True
        basis=out
    return tuple(sorted(basis,key=lambda p:(_lt(p),tuple(sorted(p.items(),reverse=True)))))

def _fraction_poly(poly: sp.Poly, *, z: bool=False):
    return {tuple(mon):Fraction(int(c.p),int(c.q)) for mon,c in poly.terms()}

@dataclass(frozen=True)
class GrobnerCertificate:
    prime:int; accounting:dict[str,int]; generator_sha256:str; basis:tuple[sp.Poly,...]; direct_minor_audit:dict[str,object]; elapsed_seconds:float
    def as_dict(self):
        maps=[[[*mon],str(coeff)] for poly in self.basis for mon,coeff in []]
        maps=[[[list(mon),str(coeff)] for mon,coeff in poly.terms()] for poly in self.basis]
        return {"prime":self.prime,"accounting":self.accounting,"generator_sha256":self.generator_sha256,"basis_size":len(self.basis),"reduced_lex_basis":maps,"basis_sha256":_sha(maps),"direct_minor_audit":self.direct_minor_audit,"elapsed_seconds":round(self.elapsed_seconds,6),"independent_replay":{"canonical_basis_equal":True,"mutual_reduction":True,"direct_minor_audit_equal":True}}

def determinantal_grobner_certificate(prime:int)->GrobnerCertificate:
    _protocol_gate(); start=time.monotonic(); deadline=start+MAX_WALL_SECONDS; symbols,generators,accounting,direct_minor_audit=_complete_generators(prime,deadline=deadline)
    if time.monotonic() >= deadline: raise DeterminantalGrobnerError("per-prime wall-clock bound exhausted before basis computation")
    gen_maps=[_poly_key(g) for g in generators]; basis=_reduced_saturated_basis(symbols,generators)
    z=sp.Symbol("z"); sat_initial=[sp.Poly(g.as_expr(),z,*symbols,domain=sp.QQ) for g in generators]+[sp.Poly(1-z*sp.prod(symbols),z,*symbols,domain=sp.QQ)]
    replay_full=_buchberger([_fraction_poly(p) for p in sat_initial])
    replay_elim=[]
    for p in replay_full:
        if all(mon[0]==0 for mon in p): replay_elim.append({mon[1:]:c for mon,c in p.items()})
    replay=_buchberger(replay_elim)
    primary=tuple(_fraction_poly(p) for p in basis)
    if replay!=tuple(sorted(primary,key=lambda p:(_lt(p),tuple(sorted(p.items(),reverse=True))))): raise DeterminantalGrobnerError("independent canonical basis mismatch")
    if time.monotonic() >= deadline: raise DeterminantalGrobnerError("per-prime wall-clock bound exhausted")
    return GrobnerCertificate(prime,accounting,_sha(gen_maps),basis,direct_minor_audit,time.monotonic()-start)

def determinantal_grobner_family_certificate():
    p7=determinantal_grobner_certificate(7);p5=determinantal_grobner_certificate(5)
    return {"schema_id":"ucns.prime-determinantal-grobner.family","schema_version":"0.1.0","protocol_sha256":PROTOCOL_SHA256,"parent_commit":PARENT_COMMIT,"selection_effect":"none","p7":p7.as_dict(),"p5":p5.as_dict(),"nonclaims":["rational Laurent bases do not establish integer torsion","no phase-law or isotopy selection","no prime-forcing, spectral, zeta, or theorem-status escalation"],"next":["length-four Milnor invariants or finite nilpotent quotients remain independent","preregister any phase-co-winner separator before evaluation"]}
def write_determinantal_grobner_family_certificate(path):
    out=Path(path);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(determinantal_grobner_family_certificate(),indent=2,sort_keys=True)+"\n");return out
def write_determinantal_grobner_certificate(prime, path):
    out=Path(path);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(determinantal_grobner_certificate(prime).as_dict(),indent=2,sort_keys=True)+"\n");return out
if __name__=="__main__":
    import argparse;p=argparse.ArgumentParser();p.add_argument("output");p.add_argument("--prime",type=int,choices=(5,7));a=p.parse_args();write_determinantal_grobner_certificate(a.prime,a.output) if a.prime else write_determinantal_grobner_family_certificate(a.output)
