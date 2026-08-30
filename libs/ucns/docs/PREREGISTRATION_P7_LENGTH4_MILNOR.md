# Frozen preregistration: minimal P7 length-four Milnor experiment

**Status:** preregistered before evaluation  
**Research order:** P7 first  
**Selection effect:** none  
**Parent artifact:** PR #183, `agent/p7-exact-milnor-alexander`  
**Parent head at freeze:** `35e432f4348987977411ccd47d33136be4fe30a6`  
**Source basis:** `Intersecting Möbius Strips and Quantum Geometry`  
**Source boundary:** one-turn opposite-side traversal, two-turn return, and the proposed seven-loop incrementally phase-shifted three-dimensional braid

## 1. Why this is the minimal decisive action

The current P7 core linking matrix has exactly one four-component sublink whose six pairwise linking numbers all vanish:

```text
Q = (R0, R1, R4, R5)
```

Its four three-component restrictions are exactly the already certified zero-Milnor triples:

```text
(R0,R1,R4)
(R0,R1,R5)
(R0,R4,R5)
(R1,R4,R5)
```

Therefore every lower-order obstruction required for an integer length-four Milnor invariant is absent in the frozen diagram. The first still-open irreducible linking question is whether the four components carry nonzero length-four information despite all pairwise and triple readouts vanishing.

No other four-component P7 sublink has all six pairwise linking numbers zero. The target is selected by the pre-existing linking matrix, not by inspecting a length-four result.

## 2. Frozen ordered target

Use the canonical carrier order inherited from the P7 family:

```text
R0 < R1 < R2 < R3 < R4 < R5
```

The primary ordered invariant is

\[
\bar\mu_{R0,R1,R4,R5},
\]

implemented as the coefficient of

\[
X_{R0}X_{R1}X_{R4}
\]

in the degree-three noncommutative Magnus expansion of the preferred longitude of `R5`, after extracting the four-component sublink `Q` from the fixed generic P7 diagram.

The implementation must also record:

- the reverse-word coefficient `X_R4 X_R1 X_R0` in the longitude of `R5`;
- the degree-one and degree-two longitude coefficients as zero gates;
- all cyclic rotations of the ordered quadruple;
- the orientation and commutator conventions used.

The primary conclusion is based only on the canonical ordered invariant. Additional permutations are consistency evidence, not alternate targets.

## 3. Required algebraic gate

Before evaluating P7, extend the exact Magnus engine from total degree two to total degree three and verify the free-group identity

\[
w=[[x_1,x_2],x_3],
\qquad
[a,b]=aba^{-1}b^{-1}.
\]

Under

\[
M(x_i)=1+X_i,
\qquad
M(x_i^{-1})=1-X_i+X_i^2-X_i^3+O(4),
\]

the gate must return

```text
coefficient X1 X2 X3 = +1
coefficient X2 X1 X3 = -1
coefficient X3 X1 X2 = -1
coefficient X3 X2 X1 = +1
```

and zero for every degree below three. Failure blocks all P7 length-four claims.

## 4. Geometric and lower-order gates

The experiment must use the exact fixed generic diagram already frozen in PR #183. It may not choose a new projection after seeing the target coefficient.

Before accepting a length-four result, the extracted sublink must reproduce:

```text
six pairwise linking numbers: 0
four length-three Milnor invariants: 0
preferred-longitude degree one: 0
preferred-longitude degree two: 0 for the required lower-order words
```

The current crossing-combinatorics standing remains computer-assisted. This experiment does not promote the diagram to proof-assistant or outward-interval certification.

## 5. Frozen outcomes

### Outcome A: nonzero

If

\[
\bar\mu_{R0,R1,R4,R5}\ne0,
\]

record the exact integer and conclude only:

> The frozen P7 realization contains detected irreducible four-component linking not visible in its pairwise linking matrix or length-three Milnor invariants.

This would justify immediate escalation to the maximal whole-link program.

### Outcome B: zero

If

\[
\bar\mu_{R0,R1,R4,R5}=0,
\]

record exact zero and conclude only:

> The unique algebraically split four-component P7 sublink has no detected length-four Milnor invariant under the frozen convention.

The next discriminator would then be the symbolic multivariable Alexander module, higher nilpotent quotients, repeated-index Milnor invariants, or invariants of the complete core-boundary link.

### Outcome C: undefined or inconsistent

If lower-order gates fail, longitude extraction is ambiguous, or convention checks disagree, report the invariant as unresolved. Do not repair the target or choose a different quadruple after evaluation.

## 6. Minimal versus maximal action

| Dimension | Minimal decisive action | Maximal coherent action |
|---|---|---|
| Primary question | Is there irreducible four-way P7 linking? | What is the strongest presently computable whole-link classification? |
| Geometric scope | One frozen four-component sublink | Every P7/P5 component and phase co-winner |
| Diagram certification | Reuse current fixed generic diagram | Outward-interval certify every crossing sign, order, and separation |
| Group calculation | Degree-three Magnus expansion | Symbolic multivariable Fox matrix, elementary ideals, nilpotent quotients |
| Milnor scope | One canonical length-four invariant plus convention checks | All admissible length-four invariants, indeterminacies, and selected higher lengths |
| Phase comparison | Not required | Compare all substantive P7 and P5 co-winners under a frozen selector |
| Result size | One exact integer or an obstruction | A complete pre-spectral topology packet |
| Main advantage | Fastest result capable of changing the theory | Closes nearly every known topology boundary at once |
| Main risk | May return zero and leave the whole-link question open | Several independent failure surfaces can obscure the first informative result |

## 7. Decision rule

Run the minimal experiment first.

- A nonzero result triggers the maximal program immediately.
- A zero result redirects the maximal program toward Alexander ideals and nilpotent quotients rather than further ordinary Milnor searches.
- An unresolved result triggers crossing-combinatorics certification before any broader computation.

This ordering distinguishes the **minimum action capable of changing the theory** from the **maximum action capable of closing the full research layer**.

## 8. Explicit nonclaims

This preregistration does not claim:

- that the length-four invariant is nonzero;
- that P7 is uniquely characterized by a Milnor invariant;
- proof-assistant certification of the generic diagram;
- a complete ambient-isotopy classification;
- an arithmetic redefinition of primality;
- an electron ontology or Pauli-exclusion derivation;
- a spectral operator, zeta-zero correspondence, or proof of the Riemann hypothesis.
