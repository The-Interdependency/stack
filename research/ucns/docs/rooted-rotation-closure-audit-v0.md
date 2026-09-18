# UCNS rooted rotation/closure audit v0

Date: 2026-09-18. Standing: **Stack-local research / UNRESOLVED**.

This audit rechecks the old based-traversal stop against current UCNS, PCEA,
Stack, METAPAT, skill-lib, Stack PR #42, and the unpublished VM audits. It adds
one executable explicit-assumption constructor and a separate post-freeze
successor gate. It makes no UCNS canon or PCEA runtime change.

## Result

The old `STOP_MISSING_ORIGIN_ATTACHMENT` remains correct as a **canonical
selection boundary**, but it was not a mathematical verdict on all later
fields. The corrected split is:

| Field | Why it is necessary | Current obstruction | Executable candidate |
|---|---|---|---|
| Origin attachment | Gives singular Structural Null a carrier-owned incident traversable object; a coordinate is not a morphism. | The unframed `Q/Z` target is homogeneous under translations, so it has no invariant point selector. Current canon also defines no attachment operation. | Explicitly assume `Structural Null -> model positive base object`. |
| Direction/chirality | Distinguishes a path from its reversal while retaining the one-turn frame flip and two-turn complete return. | Reversal preserves the unframed local data. A positive API argument is caller input, not geometry selection. | Explicitly use the existing positive native two-turn trace. |
| Rotation system | Cyclically orders all incident return germs; graph incidence alone does not define a ribbon embedding. | Two coherent rotations below preserve every earlier candidate field but yield different face closures and genus. | `paired-germs` and `sign-blocks`, both retained as competitors. |
| Marked outgoing dart | Converts a cyclic-conjugacy class into one based word and fixes the start of replay. | A cyclic order has no first element; rotating the start preserves the unmarked rotation system. | Explicitly mark the positive germ of the first declared relation participant. |
| Closure | Determines the complete orbit and whether it is merely traversed or installed as an attaching relation. | A closed walk does not itself authorize a two-cell, monodromy, or finite presentation. | Compute every orbit of `phi(d)=sigma(alpha(d))` and explicitly fill all face orbits. |

Under these assumptions the geometry is deterministic and byte-replayable:
`SURVIVED_LOCALLY`. The assumptions are not selected UCNS geometry, so the
canonical five-field construction remains `UNRESOLVED`.

Neither frozen rotation candidate produces the first observed successor. Both
give finite cellular order `1` from the one-role retained state, not `2881`:

```text
rooted-ribbon.paired-germs.v0 : 1 != 2881 -> FALSIFIED
rooted-ribbon.sign-blocks.v0  : 1 != 2881 -> FALSIFIED
```

The recursive second gate is therefore not executed. Separate scale-two and
scale-three constructions are retained only as structural diagnostics; they
are not predictions.

## Exact sources

| Source | Commit | Tree | Authority in this audit |
|---|---|---|---|
| skill-lib | `dd5027d99516831c0dcb83a176a67140d3819b66` | `a868ca319cc1400f2cc6ad645e2970eee8d75372` | Workflow, preservation, contracts, and evidence discipline |
| METAPAT | `e4165b0cac9eca41daef9c2f941881028ca55d48` | `9918f1188f64a517745851514804deb5fcae9c96` | Semantic and transfer restraint only |
| UCNS | `d8f0c505e6f5132e9711de0e7c24e4718e77e51a` | `259d7a8df72d38edee9e363f2041d86f70f8cd34` | Current geometry and canon standing |
| PCEA | `1595842abd1a5b443c6a601a2afe935b60c4adf7` | `f54527734328a08790c9c0941dec05d689d32d66` | Stable symmetric runtime |
| Stack PR #42 head | `57e3f047c092a6df5435ed4f502347664513a0ff` | `4494a6788924578c4534c3ee886da53613964bf7` | Research documentation base |
| PCEA crypto audit | `0b49672862a30cec0a0ee24e39a34241c9626f27` | `7ef9f01b3b71467b483b203990a73e03f0e850dc` | Unpublished/locally reachable negative cryptographic evidence |
| Trapdoor audit Stack base | `82dc5e39f1e0c3f162138c2e7b642814df14dd98` | `e859afb466d7dbced67e5b47d43a83514880702d` | Base beneath unpublished uncommitted trapdoor files |

The constructor reuses Stack's existing
[`ordered_complete_return_groupoid.py`](../ordered_complete_return_groupoid.py),
which preserves typed two-turn loops, ordered words, occurrence identities, and
relation provenance. Its historical source pins remain its own provenance; the
new audit does not relabel them as current upstream canon.

## Rechecking the old blockers

### Current Structural Null standing

UCNS PR #220 is merged, not open. Its final canonical wording is narrower than
the earlier Stack draft: Structural Null anchors the native construction, while
the intrinsic/extrinsic jurisdiction and representation across the carrier
remain candidate-scoped because current executable chapters do not yet agree.
The draft claim `jurisdictional model = RATIFIED` is therefore not current UCNS
authority.

This corrects provenance, but it does not construct the missing attachment.
Current canon still says that how origin attachment is represented remains
candidate-scoped.

### Origin: absence plus obstruction

The current missing-origin finding combines two distinct conditions:

1. **Missing implementation/authority:** no UCNS operation maps Structural Null
   or Public Gonol position zero into the promoted return groupoid.
2. **Mathematical obstruction for one candidate target:** on the unframed
   rational-displacement groupoid, every translation
   `tau_c([q])=[q+c]` preserves the admitted data and acts transitively. In
   particular `tau_1/2` has no fixed object. No generator-independent point can
   be selected from that target without added structure.

The obstruction is target-specific. A future nonhomogeneous recursive carrier
could contain a unique singularity or incidence. That structure is presently
absent, not disproven.

The old all-history audit now fails closed exactly as designed because current
UCNS history contains two new exact-term matches: commits `5d79bc2` and
`f6b5fd0` introduce the phrase `origin attachment`. Manual review finds that
both occurrences explicitly keep its representation candidate-scoped; neither
adds a callable attachment. Thus this is new evidence requiring review, not a
new constructor.

### Direction: implemented motion, missing selection

The actual UCNS transition remains:

```text
(t, epsilon) ~ (t+n, (-1)^n epsilon)
```

One visible turn changes local frame; two restore complete local state. This is
more than chirality and is retained intact. The map `rho(u)=-u mod 2` conjugates
positive motion to negative motion while preserving the unframed phase-zero
state. Therefore both directed traces exist and the sign still requires a
geometry-owned selector.

### Rotation: exact smallest counterexample

For two retained role occurrences `a,b`, let `alpha` exchange the two germs of
each loop and mark `a+`. Keep the same attachment, positive direction, mark, and
face-successor closure.

Candidate A:

```text
sigma cycle = (a+, a-, b+, b-)
faces       = (a+ b+), (a-), (b-)
genus       = 0
boundary    = [[1,1],[-1,0],[0,-1]]
finite cellular order = 1
```

Candidate B:

```text
sigma cycle = (a+, b+, a-, b-)
face        = (a+ b- a- b+)
genus       = 1
boundary    = [[0,0]]
finite cellular order = none
```

Both are valid oriented one-vertex ribbon maps. Their disagreement proves that
origin attachment, direction, participant identities, and a mark do not derive
the rotation system. Selecting A because it gives a finite readout, or B because
it resembles a handle, would be post-hoc.

### Mark: representation versus selection

The retained groupoid already represents all based words. A rotation system
only selects an oriented cyclic class. Choosing a starting germ is additional
pointing data. The executable candidate uses the first declared participant,
but records that provenance order is doing the selecting. It is not promoted as
intrinsic geometry.

### Closure: implementation versus topology

Once `alpha`, `sigma`, and a mark are supplied, face-orbit traversal is an
ordinary deterministic implementation problem and is now implemented. The
topological claim that an orbit is a filled attaching relation remains an
assumption. If it is only a traversed boundary, it adds no relator. If all
oriented ribbon faces are filled, the resulting ordinary surface cellular
readout is torsion-free or trivial in these candidates. Neither path yields the
nontrivial finite orders required by the observed successors.

Thus the five-field traversal chain is necessary but not sufficient for the
prime bridge. A separate global, geometry-derived torsion/monodromy presentation
would still be required.

## Retained structure

The implementation retains:

```text
R = (C_k(t), ordered relations, provenance)
C_k(t) = product_i (1 + p_i t)
```

Every prime role has a separate occurrence address and a binding to one exact
complete-return generator. Repeated prime values remain repeated occurrences.
The ordered mutually-constraining relation retains participant order and its
own provenance. The complete coefficient vector remains present in every
certificate.

The scalar collision remains a required control:

```text
(1+3)(1+11) = (1+5)(1+7) = 48
```

while the coefficient vectors are `(1,14,33)` and `(1,12,35)`. No scalar
breadth or radius replaces `R`.

Prime roles used in the observation gate are supplied after freeze. Their top
coefficient replays each observed cardinality, but the constructor does not
discover a next role `q`. The three observed role sets are nonnested, so the
exact append update is not the observed successor law.

## Post-freeze successor gate

The target-free constructor source contains none of `157`, `2881`, or
`54837698421`. Its source bytes, synthetic receipt, and both explicit
assumption records are hashed into one freeze digest before the observations
are admitted.

The separate gate then constructs complete retained records for:

```text
157         -> (157)
2881        -> (43, 67)
54837698421 -> (3, 11, 1661748437)
```

Both candidates fail at `157 -> 2881`, so no recursive application to `2881`
is called a prediction. This falsifies these two explicit successor laws. It
does not falsify every possible UCNS successor law.

## Unpublished VM evidence recovered

### PCEA cryptographic audit `0b49672`

The exact commit is locally reachable and its original six-test suite replays
against PCEA PR #41 source. It observes deterministic state reuse, known
plaintext recovery under reused state, unauthenticated modification and
truncation, replay/rollback/reordering failures, plaintext-as-state evolution,
and no post-compromise recovery. AES-GCM and ChaCha20-Poly1305 controls reject
matched modification/truncation; the ratchet comparison preserves the distinct
state-evolution requirements.

The original verdict is `FALSIFIED`. A later local parity-gate patch explicitly
accepts equivalence rather than superiority and still fails eight tested
security criteria. This audit does not import that uncommitted patch as canon;
it records that the relaxed threshold does not change the result.

### Trapdoor-lift falsification v0

The unpublished files replay ten tests, including the complete unit domain for
`3222229 = 19 * 169591`. Exact identities:

```text
producer SHA-256          = 9039d55c3d6230327338fd6c1d004a351ed5f9084f22ac546d675151ecfd8903
test SHA-256              = d129cc090b06893f412bc05e31320838578a4b9d9f22d073a027b64d054f12f8
canonical receipt SHA-256 = 4d8ae8cbe68344c6f4847fefd6659f228a3112e3810ee997af1dfa807eeaed7f
formatted JSON SHA-256    = 991a48b0df0bd6ded5d8cae9c6d507eb7b0642b3a58ae302b3beee389411690c
```

The overall existing-trapdoor question remains
`UNRESOLVED_NOT_RECONSTRUCTED`. The natural public map `x -> x^4 mod n` is
`FALSIFIED`: `y=1` has four factor-assisted CRT roots, inversion decomposes into
two local sign problems, the map is deterministic and multiplicatively
malleable, and the fixed carrier supplies neither authentication nor a security
parameter. The four `C2 x C2` quotient branches remain public algebra, not
secrecy.

## METAPAT consultation

Question: which parts of the candidate relation are identity-bearing, and what
can METAPAT legitimately transfer?

Current v4 doctrine supports preserving multiplicity, thing/boundary/state,
declared relation, addressable participant identity, participant order where
declared, and provenance through affixiation and recursive integration. Closure
is relative to a declared boundary; observation does not create structure.

METAPAT does **not** choose a UCNS carrier, attachment, chirality, rotation,
marked dart, coordinate law, prime role, arithmetic presentation, or successor.
Its contribution here is preservation and domain restraint, not a selector or
geometric proof. No EDCM measurement is used.

## Cryptographic standing

The new code establishes no cryptographic property. Its entire geometry,
assumption set, relation order, coefficients, and receipts are public. It adds
no entropy, one-way function, authentication, replay state, forward secrecy, or
post-compromise recovery.

```text
explicit-assumption ribbon constructor = SURVIVED_LOCALLY
canonical UCNS based traversal          = UNRESOLVED
paired-germs successor law              = FALSIFIED
sign-blocks successor law               = FALSIFIED
UCNS prime successor selector S(R)       = UNRESOLVED
minimal fourth-power trapdoor            = FALSIFIED
PCEA cryptographic security              = FALSIFIED
```

Geometric correctness and cryptographic security remain separate proof
obligations.

## First remaining irreducible assumption

The first unresolved assumption in dependency order is:

```text
geometry-owned pointed origin attachment
```

UCNS must add or derive one carrier-owned incidence from singular Structural
Null to a native traversable object. Current canon has no such operation, and
the homogeneous unframed `Q/Z` target has no equivariant point selector.
Coordinate zero, source order, an occurrence hash, or PCEA expectations cannot
substitute for that incidence.

Even if that assumption is later ratified, the first remaining arithmetic
assumption will be a separate geometry-derived torsion/monodromy presentation;
ordinary ribbon-face closure does not provide the required nontrivial finite
orders.

## Next experiment

Run a target-specific stabilizer comparison over only native UCNS candidates:

1. visible phase basepoint as an unframed target;
2. its `C2`-invariant two-lift fiber as a set-valued target;
3. a singly framed lift only as an explicitly stronger control.

For each target, define the carrier-owned incidence type, compute the
automorphisms that preserve all currently admitted UCNS structure, and ask
whether the target is invariantly distinguished. Freeze this comparison before
choosing a target. If every target remains transitive or reversal-symmetric,
the attachment remains `UNRESOLVED` and later fields stay unpromoted. If one
target is well-typed, invariantly unique, source-linked, and replayable without
coordinate defaults or provenance order, it may advance to a UCNS
pre-ratification attachment candidate.

## Replay

From the Stack PR #42 research worktree with this patch:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  research/ucns/tests/test_rooted_rotation_closure_constructor.py -v

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/ucns/rooted_rotation_closure_constructor.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/ucns/rooted_rotation_successor_gate.py --format markdown

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/ucns/rooted_rotation_successor_gate.py \
  --write-receipts research/ucns/receipts

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  research.ucns.tests.test_ordered_complete_return_groupoid \
  research.ucns.tests.test_ordered_return_invariant_audit \
  research.ucns.tests.test_geometry_selected_based_traversal_audit \
  research.ucns.tests.test_based_traversal_constructor_contract \
  research.ucns.tests.test_based_traversal_provenance_history_audit \
  research.ucns.tests.test_origin_attachment_basepoint_symmetry \
  research.ucns.tests.test_origin_attachment_canon_gap \
  research.ucns.tests.test_relation_factor_bridge_obstructions \
  research.ucns.tests.test_rooted_rotation_closure_constructor
```

The unpublished audits were replayed from their evidence worktrees with:

```bash
STACK_CRYPTO_REPLAY=$(mktemp -d /tmp/stack-crypto-0b49672.XXXXXX)
git -C /home/wayseer_interdependentway_org/src/stack worktree add --detach \
  "$STACK_CRYPTO_REPLAY" 0b49672862a30cec0a0ee24e39a34241c9626f27
cd "$STACK_CRYPTO_REPLAY"
PCEA_AUDIT_SOURCE_ROOT=/home/wayseer_interdependentway_org/src/pcea-typed-carrier-repair \
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  research.pcea.tests.test_cryptographic_claims_audit

cd /home/wayseer_interdependentway_org/src/stack-ucns-trapdoor-audit-20260917
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  research.ucns.tests.test_trapdoor_lift_falsification
```

The crypto replay worktree was detached at
`0b49672862a30cec0a0ee24e39a34241c9626f27`; the PCEA source-identity assertion
inside that suite binds the PR #41 runtime bytes. The trapdoor files are
unpublished and uncommitted, so their producer, test, and receipt content
digests above—not the worktree base alone—are their evidence identities.

Exact frozen hashes and final replay counts are in
[`rooted-rotation-successor-gate-v0.json`](../receipts/rooted-rotation-successor-gate-v0.json).

The focused new suite passes `14/14`. A combined 69-test run over inherited
groupoid, invariant, geometry-selection, constructor-stop, origin, factor-
bridge, and new modules yields 56 passes, 4 receipt-drift failures, and 9
fail-closed provenance errors. The four failures are old receipts whose source
digests no longer match the evolved Stack tree. The nine errors all descend
from the history audit detecting the two current UCNS commits above and
requiring manual review. No inherited historical receipt is silently rewritten
to manufacture a pass.

The repository-wide Stack consistency gate currently fails identically on PR
#42 and current Stack main at the pre-existing `epac.graduation: forge Python
implementation has returned` check. That baseline structural defect is not
reclassified as a failure of this isolated research module.

## hmmm

The missing door is now separated from the hallway: a rooted ribbon carrier can
be constructed once its marks are supplied, but current UCNS still does not
select the origin attachment, the rotation, or the torsion-producing arithmetic
presentation.
