# Base-27 midpoint projection — finite-state research receipt

**GPT generated; context, prompt Erin Spencer.** 2026-11-28.

Standing: **SURVIVED_LOCALLY** for the declared integer-residue identities and finite geometry. **FALSIFIED** for the hypotheses that a constant radius, redundant radius, fixed coordinate permutation, or indefinitely repeated bearing projection alone provides an independent recovery constraint. **UNRESOLVED** for any actual cryptographic trapdoor. No security profile is implemented or certified.

## CHANGED

Executed an isolated standard-library experiment on the supplied twin-prime cubing transform, with exact finite geometry, two 30-million-number prime windows, explicit retained-label reconstruction, extra-observation controls, ordinal census, interlacing/permutation controls, recursion, forward scaling and falsifiers. The research artifact is standalone rather than a change to existing UCNS/Weave code. Source graph and current authorities are pinned in `sources.json`.

## PROOF: exact arithmetic

Let M=3^9=19,683 and let c be the midpoint of a twin-prime pair above 3. Then 6 divides c, so its canonical residue lies among the 6,561 multiples of 3. The special pair (3,5) is deliberately excluded.

Cubing each endpoint gives a forward difference 6c²+2. The forward modular difference equals 2 iff 3^9 | 6c², which is equivalent to 1+2v₃(c)≥9, or 81 | c (including c=0 in the residue domain). Then c³ and 3c² both vanish modulo M, so the cubes reduce to 3c−1 and 3c+1. The finite eligible domain D=81Z/M has 243 elements and the midpoint map is T(c)=3c mod M. Its image is 243Z/M with 81 elements. The three elements of each fiber differ by 6,561 canonical positions. For y in the image, these are y/3 + j·6,561, for j in {0,1,2}.

This is a complete finite-map explanation, independent of secret information. It identifies the three mathematically compatible spokes, not which integer prime pair actually occurred. The original unbounded pair is not recovered by reconstructing its residue. No assumption about infinite twin primes is needed to establish that all spokes occurred in the bounded census.

All 19,683 residues pass independent direct-cube checks; the three supplied example midpoints have residues 7,452; 14,013; 891, and all land at 2,672 and 2,674. The underlying angular geometry is a 19,683-position generic circle, not the historical 157-position Public Gonol or the native Möbius state.

## Five candidate distinctions

The results below report partitions of fully specified mathematical objects, not attacks on the Weave implementation.

### Radius

| Observation | Classes | Largest class |
|---|---:|---:|
| Bearing only |81|3|
| Bearing + constant exact radius |81|3|
| Bearing + radius determined by bearing |81|3|
| Bearing + two explicit radial layers |162|2|
| Bearing + three explicit radial layers |243|1|
| Identity control |243|1|

An explicitly retained sector label reconstructs all 243 of 243 original residues. All 486 wrong-sector choices produce a different residue, so the label affects the return; this is not tamper detection. The three-layer control simply records the sector trit in a radial coordinate. The two-layer control leaves a pair ambiguous at every output spoke. A known physical radius without an independently varying observable does not identify the sector. No physical metric/embedded band claim is made.

### Additional modulus

The domain is the canonical input residue, not unbounded c. Each fiber has successive differences 6,561; for an additional transformed residue those differences are 19,683. If the additional modulus divides the difference, it cannot refine the fiber; if it divides twice the difference but not the difference, the first and third elements still agree. These identities explain the observed class sizes. This tests public observations, not secret key relations.

| Additional modulus | Input observation classes | Input max size | Transformed observation classes | Transformed max size |
|---|---:|---:|---:|---:|
|2|162|2|162|2|
|3, 81, 243, 6,561 (each)|81|3|81|3|
|157|243|1|243|1|
|19,683|243|1|81|3|
|19,685|243|1|243|1|

Additional public observations can distinguish the finite residues; they do not establish private recovery. For unbounded integer lifts, finite congruences still leave a new period of possible integer values. Nothing here proves recovery of arbitrary integers or prime identities.

### Prime ordinals

One-based lower-prime ordinal is computed by traversing all primes in the sieve. The two primes of any above-three twin pair are consecutive primes: their ordinal difference is always 1, and adds no distinction. The exact lower-prime ordinal uniquely names the integer prime by definition, rather than supplying an independent geometric secret. It is not a function of midpoint residue alone.

For smaller ordinal residues, an observed class is (output spoke, lower-prime ordinal mod q); its size is the count of distinct midpoint residues actually observed in that class. In the next interval:

| Ordinal modulus | Observed classes | Classes with >1 distinct midpoint residue | Max |
|---|---:|---:|---:|
|3|243|243|3|
|9|728|702|3|
|27|1,964|1,110|3|

Even the finer label leaves ambiguous observed classes. First-window figures and complete histograms are in `evidence.json`. Finite data sparsity must not be mistaken for a one-to-one law or confidentiality.

### Interlacing

On the full independent product D×D, 59,049 mathematical input pairs produce 6,561 distinct two-coordinate observations, with nine pairs per class. A fixed coordinate swap preserves the *entire partition*; omission leaves 81 classes of 729 pairs. The same invariance holds for the fixed-second-coordinate control. Merely reordering a tuple does not create information; retaining independent relations can change what is visible, but that would be a new declared observation. This is not the active Weave bitstream or its multi-arity, corpus-dependent construction. Do not promote this falsification of a permutation-only hypothesis to a verdict about Weave.

### Recursion

For depth d≥0, the map is T^d(c)=3^d c mod M. On D the number of image spokes is 3^max(5−d,0); each class size is 3^min(d,5). All depths 0–7 were tested:

| Depth | Distinct spokes | Inputs per spoke |
|---:|---:|---:|
|0|243|1|
|1|81|3|
|2|27|9|
|3|9|27|
|4|3|81|
|5–7|1|243|

There is saturation at five ternary digits, not an indefinitely growing search space. These are repeated midpoint-bearing projections, not another census of cubed primes.

## Prime census and brightness

| Window | Twin pairs | Retaining forward gap 2 | Ordinary / eligible / transformed spokes |
|---|---:|---:|---|
| Upper prime ≤30,000,000 |152,890|5,646|6,561 / 243 / 81|
| 30,000,000 < lower prime; upper ≤60,000,000 |127,666|4,721|6,561 / 243 / 81|

All direct modular cube checks agree, including the separate boundary-crossing pair (29,999,999, 30,000,001), which is excluded from both strict windows and is not gap preserving (forward modular gap 11,234). Total above-three twin-pair checks through 60 million: 280,557 including that pair.

Every eligible family contributes to every output spoke in both windows. In the second window, per-family counts range from 8 to 30; per-spoke totals range from 42 to 70. At spoke 5,589, relative imbalance is largest: (10,30,23), a 3:1 maximum/minimum ratio. Brightest spokes are 11,178 and 11,907, tied at 70, with family counts (25,26,19) and (25,22,23), respectively. At 2,673 the counts change from (22,20,23) to (15,23,18). Family totals over all spokes are (1,872,1,915,1,859) and (1,546,1,567,1,608). These are descriptive counts only; no stable family preference, prime distribution theorem, π/φ pattern, or entropy is inferred.

`brightness.csv` contains all 81 rows; `brightness.png` is the stacked chart. Both are regenerated from exact data by `plot_census.py`.

## Forward scaling (measured)

Median wall-clock time for forward residue mapping and partition summary, nine repeats each, measured in this environment. The timings are not adversarial runtime or asymptotic security evidence. `timing.json` preserves all nine runs.

| Modulus | Eligible residues | Classes | Median milliseconds |
|---:|---:|---:|---:|
|3^5|27|9|0.0086|
|3^7|81|27|0.0171|
|3^9|243|81|0.0429|
|3^11|729|243|0.1733|
|3^13|2,187|729|0.4895|
|3^15|6,561|2,187|1.9026|

## Current source and ownership graph

- [skill-lib, b3bcb5f](https://github.com/The-Interdependency/skill-lib/tree/b3bcb5f51c19dd9f5e61a38a4d7cb72af178c9cc): research/evidence and authority discipline.
- [UCNS, ee8addc](https://github.com/The-Interdependency/ucns/tree/ee8addc0af36f02b64b42cb355734cb72a126ea5): geometry and mathematical representation; finite modular circle candidate; complete native Möbius lift remains unresolved. Stack's pinned UCNS base is separately `1975fe70cf4e0826a8020c2da3047569e277af64`.
- [Stack, 3d02974](https://github.com/The-Interdependency/stack/tree/3d0297430956f6fae22b3330063a42db27ddbfe6): research forge; restored Möbius coordinate-domain candidate and distinct π digit-block workspace. The base-27 theorem was supplied in the conversation; searches did not find a corresponding implementation in current sources.
- [Weave, Stack research](https://github.com/The-Interdependency/stack/tree/3d0297430956f6fae22b3330063a42db27ddbfe6/research/weave): cryptographic architecture, intended private/public relation, native sequence cycle and Cypher challenges. No independently accessible Weave repository was found. Existing published cycle evidence and previous polynomial falsification retain their original scope. A new mathematical finding transfers neither proof standing nor security standing to the native cycle. No source pin, canon, current cipher or challenge record was modified.

## Review and reproduction

Unpack the ZIP. Core requires only Python 3.12+ standard library. The packaged outputs are already executed. To rerun without overwriting the evidence, use a new directory or distinct names:

```sh
python -m unittest -v
python experiment.py --limit 60000000 --output review-evidence.json
cmp review-evidence.json evidence.json
python experiment.py --timing review-timing.json
python verify_evidence.py
```

`verify_evidence.py` checks both packaged replays, provenance hashes, all 81×3 family rows, both census counts, saturation points and the separately checked crossing witness. Timing replay is expected to differ. `plot_census.py` uses matplotlib only for its optional chart. The unit suite contains 15 tests, including two deliberately altered-cube witnesses, wrong retained labels, invalid state, an independent small trial-division sieve check, and coarsening witnesses. Both full reports are byte-identical. An independent odd-only sieve in a separate review reproduced both windows and the salient brightness counts. Exact test and verification outputs are included. `sources.json` preserves source blob and commit identities. `SHA256SUMS` binds the packaged files; run `sha256sum -c SHA256SUMS` for integrity (not authorship authentication).

`CYPHER-MATH-REVIEW.md` contains mathematical challenge questions for independent review of this experiment. It is not a cryptographic ciphertext challenge, attack harness, or automated adversarial workflow; no external Cypher trial was conducted. Reversal here is explicit retained-label reconstruction of canonical residues only, not authorized private-key decryption. The public algebraic falsifiers apply to abstract finite maps, not a deployed cipher. Full UCNS/Stack/Weave suites were not executed; repository integration and security evaluation are NOT RUN. No PR was opened or merged.

## NEXT

A future claim about private-state necessity must identify a separately defined relation and compare its authorized recovery assumptions with publicly observable information; correctness, nontrivial geometry, and the number of preimages do not suffice. The native radius/metric question remains a distinct UCNS geometric research frontier. If the three-family brightness association is investigated in π or φ, define the digit-block admission and matched-information controls separately from this integer sieve. This finite mathematical receipt is the negative-control baseline, not an implemented asymmetric cryptosystem.

## hmmm

What is the independent relation that supplies more than one lost ternary digit, already retained as state? None was established. The finite map has an exact inverse relation, but not a demonstrated cryptographic trapdoor.
