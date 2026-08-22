# Frozen preregistration: exact Milnor and prime-character Alexander experiment

**Frozen before evaluating the phase functional or whole-link fingerprints.**

## Scope

The experiment has three ordered aims:

1. replace the five numerical P7 Milnor-zero conclusions with integer coefficients from a generic link diagram and a degree-two Magnus expansion of preferred longitudes;
2. evaluate a prime-sensitive phase selector that was fixed before its outcome was inspected;
3. issue a stronger whole-link discriminator through finite-field specializations of the multivariable Fox-Alexander matrix.

P7 is evaluated first. P5 is processed only afterward under the same protocol.

## Fixed generic projection

Each complete centerline component is translated in the projection plane by

\[
\delta_i=10^{-3}(a_i,b_i).
\]

For P7 the integer vectors are

```text
C  ( 0, 0)
R0 ( 1, 2)
R1 (-2, 1)
R2 ( 3,-1)
R3 (-1,-3)
R4 ( 2,-2)
R5 (-3, 3)
```

P5 uses the first five applicable labels. The perturbation is fixed independently of crossing signs and invariant values. Its maximum component displacement is below `0.00425`; the maximum relative displacement is below `0.00850`, smaller than the previously certified finite-width clearance `0.07`.

## Exact Milnor protocol

For each pairwise-zero P7 triple:

1. construct the generic double-crossing diagram of the translated centerlines;
2. order all undercrossings on each oriented component;
3. use the Wirtinger update

\[
m_{\mathrm{out}}=o^{\varepsilon}m_{\mathrm{in}}o^{-\varepsilon};
\]

4. construct the preferred longitude by prepending the over-arc factors in traversal order, which gives the reverse conjugator product;
5. apply the noncommutative Magnus expansion through total degree two;
6. report the coefficient of \(X_iX_j\) in the longitude of component \(k\).

The implementation must recover `+1` or `-1` for the closure of the Borromean braid `(sigma_1 sigma_2^-1)^3` before P7 values are accepted.

## Prime-character Fox-Alexander selector

For prime primitive `p`, use the finite field

```text
P7: F_29, whose multiplicative group contains order-7 characters
P5: F_11, whose multiplicative group contains order-5 characters
```

Let `g=2`, and let

\[
\zeta_p=g^{(q-1)/p}\in\mathbb F_q.
\]

For phase candidate `(omega,n)`, assign the component character

\[
t_C=\zeta_p^{\omega},
\qquad
t_{R_i}=\zeta_p^{in}.
\]

Evaluate the full Wirtinger Fox matrix at this character. Define

\[
\nu(\omega,n)=N_{\mathrm{generators}}-\operatorname{rank}A(\chi_{\omega,n})-1,
\]

where the final subtraction removes the universal Fox kernel direction.

## Phase-lift alignment energy

At every stored hypernode occurrence, compare the candidate phase \(\phi_{h,c}\) with its normalized finite-field lift residue \(r_{h,c}/p\). Define

\[
E(\omega,n)=\sum_{h,c}
\min\left(|\phi_{h,c}-r_{h,c}/p|,
1-|\phi_{h,c}-r_{h,c}/p|\right)^2.
\]

This is an exact rational number.

## Frozen selector

Among admissible candidates, select lexicographically by:

1. maximum minimum phase gap;
2. maximum Fox-Alexander excess nullity \(\nu\);
3. minimum exact phase-lift alignment energy \(E\);
4. minimum absolute center winding `|omega|`;
5. positive winding before negative winding;
6. smallest outer numerator `n`.

No criterion refers to the desired torus-knot degree, to `7`, or to the previously selected `T(2,7)` boundary.

## Whole-link fingerprint

For every distinct prime-character assignment induced by the declared search family, record:

- Fox matrix rank;
- excess nullity;
- rank/nullity histogram;
- ordered rank-vector SHA-256.

The complete fingerprint, rather than one favorable character, is the primary P7-versus-P5 whole-link comparison.

## Stopping and failure rules

- A nonintegral Magnus coefficient is a failure of diagram or longitude construction.
- Failure to recover Borromean `|mu|=1` blocks P7 Milnor claims.
- A selector tie is retained as a tie; no new criterion may be added after evaluation.
- Selection of a boundary degree other than `7` is accepted.
- Failure of the Fox profile to distinguish P7 and P5 is accepted.
- No result is promoted to a zeta-function theorem, arithmetic redefinition, or proof of the Riemann hypothesis.
