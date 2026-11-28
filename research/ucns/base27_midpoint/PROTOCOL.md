# Frozen experiment protocol — 2026-11-28

## Objective and standing

Reproduce the supplied integer-residue theorem and measure which extra geometric or arithmetic observations refine its finite equivalence classes. This is an isolated, noncanonical mathematical experiment, not a cipher or a security benchmark. Weave retains ownership of cryptographic research; UCNS owns geometric claims. A fixed-radius circle is not the native 157-gon or a Möbius metric.

## Scope and falsifiers (fixed before execution)

- Domain: canonical representative c in [0, 3^a), with 3^ceil((a−1)/2) dividing c; primary exponent a=9. Eligible residue means there is no modular obstruction; actual twin-prime realization is empirical. Direct cube gap is forward +2, not signed shortest arc. Exclude exceptional (3,5).
- For a=9, check all 19,683 residues by independent direct modular cubes against the divisibility condition and midpoint formula. All eligible midpoint fibers must contain exactly three distinct spokes; otherwise the theorem fails. Reproduce 46,818, 73,062, 178,038 as retrospective examples.
- Radius controls: constant exact radius; a common bearing-dependent radius; three exact radial layers explicitly labeling the input sector; a coarse two-layer label. Check refinement and retained-label reconstruction on the entire finite carrier. The sector label is an explicit trit, not derived private state. Corrupt labels must not reproduce the original residue (no tamper-detection claim).
- Independent moduli: evaluate an additional canonical midpoint residue and an additional transformed residue on moduli 2, 3, 81, 243, 157, 6561, 19683, 19685. Measure the output class sizes, not a secret search. Keep the canonical representative assumption separate from arbitrary integer lifts.
- Ordinals: sieve all primes through 60,000,000 (inclusive); one-based prime ranks; consecutive twin pairs above 3; retrospective interval upper prime <=30,000,000; held-out interval 30,000,000 < lower prime and upper prime <=60,000,000. Record any excluded crossing pair. Compare direct cubes for every pair. For eligible pairs measure output × input-family counts; observe lower ordinal modulo 3, 9 and 27, and ordinal difference. Measure distinct input residue labels per observed class. Full ordinals identify primes by definition and are not a private relation.
- Interlacing: use fully public mathematical sequences of two eligible residues with the second fixed at 81; compare observation tuple, a fixed coordinate swap, and one-coordinate omission. Also compare the first 81 eligible pairs (fixed-order toy sample) as label vectors. The fixed permutation must preserve the equivalence partition; omission may coarsen only. No bitstream encryption or key schedule.
- Recursion: iterate the bearing map c→3c mod 3^9, not prime cubing. Test depths 0 through 7 across all eligible input residues. Predict class count 3^max(5−d,0), class size 3^min(d,5). Saturation at depth 5 is a required negative control against unbounded growth.
- Scaling: a=5,7,9,11,13,15; enumerate eligible residues, evaluate direct forward bearing map, count classes and fibers, 9 repeats each. Record median wall time and platform details separately from deterministic evidence. No time-to-break or hardness metrics.
- Controls: identity observation, redundant duplicated labels, constant observation, fixed permutation, explicit sector label. Malformed state must be rejected. All exact checks run in standard-library unittest. Execute deterministic report twice and compare bytes; measured timing record is not expected to reproduce bit-for-bit.
- Evidence divisions: mathematical theorem, finite replay, empirical prime counts, application-security NOT TESTED. Do not transfer proof or status to any cipher or native Möbius construction.

Usage: run python -m unittest -v, python experiment.py --limit 60000000 --output evidence.json and python experiment.py --timing timing.json from this directory. All code is local, standard library, no external I/O beyond named output files. The complete run is estimated below 100 MiB sieve memory plus modest aggregate tables, with no dependency downloads.

hmmm: an independently necessary private mathematical relation, physical-metric radius, and actual cryptographic asymmetry are not established by these tests.
