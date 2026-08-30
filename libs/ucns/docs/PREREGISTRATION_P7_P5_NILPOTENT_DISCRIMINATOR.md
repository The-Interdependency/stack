# Frozen preregistration: smallest decisive nilpotent discriminator

**Status:** frozen before quotient construction

**Research order:** P7, P5, then phase-co-winner identity comparison

**Selection effect:** none

**Parent result:** PR #190, exact-zero frozen P7 length-four Milnor target

## 1. Smallest decisive quotient

Freeze the complete ordered core-link group

\[
G_L=\pi_1(S^3\setminus L)
\]

from the existing fixed, interval-certified Wirtinger diagram. The primary
object is the marked peripheral nilpotent quotient

\[
N_4(L)=G_L/\gamma_5(G_L),
\]

where `gamma_1(G)=G` and `gamma_(k+1)(G)=[gamma_k(G),G]`. Thus `N_4` has
nilpotency class at most four.

Class four is the first permitted class. Pairwise linking, exact length-three
Milnor values, and the frozen distinct-index length-four target already inspect
the information visible through weights one, two, and three. Increasing directly
to class five or changing the lower-central filtration after seeing class four
is forbidden.

The marking consists of the existing ordered component meridians and preferred
longitudes. P7 uses `(C,R0,R1,R2,R3,R4,R5)`; P5 uses
`(C,R0,R1,R2,R3)`. The first Wirtinger arc after the fixed basepoint is the
component meridian. Longitude traversal prepends signed over-arc factors, as in
the existing exact Magnus implementation. No Tietze move, generator reorder,
basepoint move, orientation reversal, or longitude conjugacy representative may
be selected after quotient output is inspected.

## 2. Frozen backend

Primary computation:

- Ubuntu Noble package `gap` version `4.12.1-2build2`;
- GAP package NQ version `2.5.11-1`;
- `NqEpimorphismNilpotentQuotient(G,4)` on the exact Wirtinger finite
  presentation;
- integral polycyclic output; no rationalization and no finite-prime
  specialization.

The receipt records the package versions, input presentation SHA-256, generator
and relator counts, the NQ epimorphism, lower-central factors through weight
four, torsion invariants, Hirsch number, and the collected coordinates of every
marked meridian and preferred longitude.

Independent replay:

- repository Python under the pinned project lock;
- exact integer noncommutative Magnus arithmetic through total degree four;
- substitute every fixed Wirtinger relator and require all coefficients through
  degree four to vanish after the declared quotient relations;
- replay every marked longitude word and compare its weight-filtered coordinates
  with the primary result.

The replay passes only if component order, relator order, all lower-central
factor invariants, and every marked element agree exactly. A digest match alone
is insufficient.

## 3. Canonical receipt

The canonical JSON representation uses UTF-8, sorted object keys, compact
separators, decimal integers, and newline termination. Ordered mathematical
lists remain ordered. Polycyclic generators retain NQ order. Signs are not
normalized up to inversion. The receipt includes both the raw deterministic NQ
transcript digest and the structured comparison fields.

Resource bounds are 900 seconds wall time and 8 GiB resident memory per family.
Any backend error, timeout, memory breach, non-integral conversion, inconsistent
collection, or primary/replay mismatch yields `unresolved`. Partial output may
be retained only as a failure receipt and cannot support `distinguish` or
`no-distinguish`.

## 4. P7/P5 comparison

Both complete core links are computed at the same class with the same pipeline.
The different weight-one ranks are recorded but cannot by themselves count as
the new discriminator; component count and pairwise linking are already known.

For each family, freeze the higher signature as:

1. ranks and torsion invariant factors of `gamma_k/gamma_(k+1)` for
   `k=2,3,4`;
2. the defect of each such rank from the Witt rank of the free nilpotent group
   on that family's meridians;
3. the lower-central depth and collected weight-two through weight-four
   coordinates of every preferred longitude, retained in component order;
4. the sorted multiset of longitude coordinate records as an additional
   label-forgetting check.

P7/P5 is `distinguish` only if these higher signatures differ in a field other
than the known number of components or weight-one rank. It is `no-distinguish`
only if the normalized higher signatures agree exactly. Incomparability caused
by unequal coordinate domains, rather than a declared invariant difference, is
`unresolved`.

## 5. Phase-co-winner comparison

Freeze the substantive co-winners already emitted by the phase selector:

- P7: `(center_winding, outer_numerator) = (3,4)` and `(9,4)`;
- P5: `(-3,1)` and `(9,1)`.

For each co-winner, bind the exact diagram, Wirtinger presentation, peripheral
marking, and phase-law record. A nilpotent quotient may distinguish co-winners
only if their bound group/peripheral inputs differ and their structured class-four
outputs differ. If co-winners bind byte-identical group/peripheral inputs, the
mandatory result is `no-distinguish`; phase annotations may not manufacture a
topological difference. Any ambiguous binding is `unresolved`.

## 6. Decision rule

Accept exactly one family result and one phase result from:

- `distinguish`: the frozen higher signature differs under the rule above;
- `no-distinguish`: the frozen comparable signatures agree exactly;
- `unresolved`: construction, resource, binding, or replay gates fail.

No outcome changes the quotient, class, component scope, ordering, backend,
normalization, or comparison fields. A P7/P5 distinction is not a phase-law
selection. A phase no-distinction is not evidence that the phase laws are
physically equivalent.

## 7. Nonclaims

This protocol does not establish ambient-isotopy classification, integral
Alexander torsion, phase selection, prime forcing, particle ontology, a spectral
operator, a zeta correspondence, or theorem status.
