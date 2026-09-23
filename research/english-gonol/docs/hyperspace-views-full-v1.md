# Four views over the complete English construct

Every one of the **164,864 words** in the pinned OEWN 2025 construct was processed.
The native implementation and a separate exact reconstruction produced identical
evidence. The native execution also compared the complete record, including its
receipt, against the reconstruction for every word. There was no prefix, sample,
limit, disagreement, or early completion.

The four-view synthesis has **137,013 distinct values**. View 4 contributes no
additional distinction once view 2 or view 3 is present. Views 1, 2, and 3 each
contribute distinctions that the other views cannot recover in this corpus.
That establishes information contribution; inference usefulness still needs a
specified task and acceptance criterion.

## Historical scope and current replay gate

These sealed receipts qualify the frozen Stack and runner identities below.
Current main has since changed the view payload and synthesis representation;
this report does not qualify that implementation. The receipt gate reads the
historical Git objects and verifies their recorded digests. It does not rewrite
old receipts to match new source. The tightened runner additionally binds the
supplied manifest directly to the protocol's repository, commit, tree digest,
receipt, and counts; two identically altered manifest copies cannot pass.
A new current-source qualification requires a new protocol and full native and
independent corpus runs. The historical runner also requires the exact database
and historical source checkout; running it on current main fails closed.

## Complete-corpus results

| View | Distinct values | Repeated records | Singleton words | Colliding word pairs |
|---|---:|---:|---:|---:|
| 1 — definition constituent overlap summary | 1,829 | 163,035 | 1,235 | 9,724,683,619 |
| 2 — word-axis terminal phase/frame | 314 | 164,550 | 0 | 44,524,977 |
| 3 — provenance-interval lift | 100,778 | 64,086 | 57,107 | 91,813 |
| 4 — canonical-witness lift | 157 | 164,707 | 0 | 89,000,202 |
| Synthesis — all four | **137,013** | **27,851** | **113,554** | **33,120** |

The earlier report called `N - distinct_values` “collisions.” Here that quantity
is named **repeated records**. It differs from the number of words involved in
collisions and the number of colliding pairs. In the synthesis, **51,310 words**
belong to non-singleton groups; those groups contain **33,120 unordered pairs**.
The largest group has nine words. Distinct values are not a count of uniquely
identified words: only the 113,554 singleton words have unique synthesis values.

| Removed view | Remaining views | Distinct values | Distinctions lost from the full synthesis |
|---|---|---:|---:|
| 1 | 2+3+4 | 126,746 | **10,267** |
| 2 | 1+3+4 | 116,971 | **20,042** |
| 3 | 1+2+4 | 11,200 | **125,813** |
| 4 | 1+2+3 | 137,013 | **0** |

These removal effects are conditional on the remaining views; they cannot be
added as independent contributions. Appending coordinates cannot reduce the
number of distinct tuples, so winning the distinctness ranking alone never
establishes that every coordinate deserves independent integration.

## What each view can justify

**View 1 has measurable additional information, with limited coverage.** It is
absent for **139,294 words (84.49%)**, because they have fewer than two definitions.
It is available for 25,570 words. Absence remains `None`, distinct from measured
zero overlap. The 1,829 values include that absent bucket, which dominates its
pair count. The stored value is actually a four-integer summary: definition
count, pair count, zero-overlap pair count, and shared-constituent sum. The
calculated density fraction is not included in the view. Integrate this as
definition constituent-overlap metadata if that information is wanted. Shared
constituents do not establish that independently constructed definition axes
cease to be orthogonal.

**View 2 retains a terminal state, not the ordered word construction.** The
pinned native displacement reduces to an exact additive total:

```text
T = sum(glyph ordinal + character database ID)
phase = (T mod 157) / 157
frame = parity(floor(T / 157))
```

Consequently, it has at most 157 × 2 states. All **4,885 multiword groups** sharing
the same glyph multiset have the same view-2 state within their group: **10,692
words**, with **zero** groups distinguished by order. Reversing character IDs
changes view 2 for **164,466 words**, while preserving exact source glyphs and
their order. This is a source-bound terminal feature; the full ordered glyph
construction must remain available to recover spelling/order.

**View 3 provides address information.** Its deck is `floor(word_id / 157)` and
its lift is `157 * deck + residue`. This is coarse address context combined with
the terminal residue; it does not preserve the complete word ID. Numeric
addresses can be useful memory: they support retrieval, cross-reference, and
provenance. Preserve the full word ID with its corpus identity, alongside this
derived lift, and define remapping when the corpus changes. The full word-ID
baseline distinguishes all 164,864 words. Uniqueness measures indexing capacity;
it does not establish semantic similarity or inference quality.

**View 4 is a derivable witness.** It is `(residue, 157 + residue)`. View 2 already
determines the residue, and view 3 explicitly contains it. Every subset containing
either view 2 or view 3 is unchanged in discriminatory power when view 4 is
added. It can remain a named, recomputable witness for canonicalization or
checking; it warrants no independent information weight in this synthesis.

The supported integration proposal is therefore: retain view 1 as nullable
overlap metadata, view 2 as a terminal-state feature, view 3 as provenance/address
metadata, and expose view 4 as a derived witness. No geometry law, neural-input
selection, or inference quality is ratified by this proposal. The source view
formulas remain unchanged, and the machine receipts retain `selected: []`.

## Complete renumbering controls

Every control evaluates every word. References are relabelled consistently in
the counterfactual formulas; the source database remains read-only. The glyph
control uses the independently reconstructed formula after its equivalence to
the original native output was checked for every word. These controls were not
executed through separately materialized native databases.

| Complete control | Distinct synthesis values | Original colliding pairs separated | Newly colliding pairs |
|---|---:|---:|---:|
| Baseline | 137,013 | — | — |
| Reverse word IDs: `i → N+1−i` | 137,006 | 5,999 | 5,955 |
| Permute word IDs: `i → 1+(157*(i−1) mod N)` | 138,844 | 33,120 | 29,903 |
| Reverse character IDs: `j → C+1−j` | 138,068 | 24,230 | 22,670 |

The affine word-ID map is a verified bijection for this corpus. Both word-ID
controls leave views 1, 2, and 4 unchanged and alter view 3. Character-ID reversal
leaves view 1 unchanged and alters views 2, 3, and 4. These results demonstrate
address dependence, while leaving the possible usefulness of those addresses
intact. The alternative counts are controls, not proposed replacement layouts.

## All fifteen nonempty combinations

| Views | Distinct values | Repeated records | Colliding pairs |
|---|---:|---:|---:|
| 1 | 1,829 | 163,035 | 9,724,683,619 |
| 2 | 314 | 164,550 | 44,524,977 |
| 3 | 100,778 | 64,086 | 91,813 |
| 4 | 157 | 164,707 | 89,000,202 |
| 1+2 | 11,200 | 153,664 | 31,612,961 |
| 1+3 | 116,971 | 47,893 | 64,878 |
| 1+4 | 9,046 | 155,818 | 63,186,821 |
| 2+3 | 126,746 | 38,118 | 46,649 |
| 2+4 | 314 | 164,550 | 44,524,977 |
| 3+4 | 100,778 | 64,086 | 91,813 |
| 1+2+3 | 137,013 | 27,851 | 33,120 |
| 1+2+4 | 11,200 | 153,664 | 31,612,961 |
| 1+3+4 | 116,971 | 47,893 | 64,878 |
| 2+3+4 | 126,746 | 38,118 | 46,649 |
| 1+2+3+4 | 137,013 | 27,851 | 33,120 |

## Scope, identity, and replay

The protocol was frozen before full-corpus execution, after the earlier
20,000-word exploratory result. This is not a blinded study. The complete scope
contains 118 characters, 1,739,949 ordered glyph references, 185,155 definitions,
3,535,375 definition components, and 866,183 resolved semantic-evidence rows.
All 198,322 unordered within-word definition pairs were included. SQLite
integrity passed and the database hash remained unchanged across both runs.

| Binding | Exact identity |
|---|---|
| Stack source | `1f9a35eb355296fc88d09784c7a3e2e95511ca31` |
| UCNS source | `1cf10c2df2541a332a77f2ed3feda0c6bef4abcc` |
| OEWN source | `dc343f2683279ecbb13fab4e2fd778d7b162d287` |
| Full construct logical receipt | `12277b4959c0c72b7af12097b8a77bf91866bbf669e7f4ac07b6a5f1426ebb57` |
| Generated database SHA-256 | `350e819d1d6f3312dec9aaada396c351180da0030c4d07d37559d7a2686c353e` |
| Frozen protocol SHA-256 | `de4f123357a340f744d6cf1f8c1067985f22f9379a51214e7a8c7dceafec9c7e` |
| Ordered complete-observation SHA-256 | `c5856ec7cd49041756e163644f6e10197e715801e7a27814e985f231898833a3` |
| Complete audit receipt | `61aa21995be2428a351245e1de66c884bff394fa9562e539f0ab3b5aefe78264` |

[FULL_VIEW_AUDIT.json](../FULL_VIEW_AUDIT.json) binds each consumed source blob,
the work graph, complete corpus counts, controls, and interpretation rules.
[Native evidence](../experiments/hyperspace-views-full-v1/native.json) and
[independent evidence](../experiments/hyperspace-views-full-v1/independent.json)
have exactly equal `evidence` objects. Execution metadata is outside that
digest: native 102.806 seconds, independent 28.411 seconds; peak RSS 1,224,740
and 1,218,672 KiB respectively, Python 3.12.14.

The native run loads the exact verified eight-file UCNS dependency closure as
a namespace package; the package entrypoint is not executed. It binds the
verified native motion function once to avoid per-word source hashing and Git
subprocesses. Native view, geometry, and motion formulas are unchanged. Both
engines use the same generated database: their agreement independently checks
the view computation, not the corpus materialization.

From Stack, with the exact database plus its manifest and pinned UCNS sources:

```bash
PYTHONPATH=research/english-gonol python -m english_gonol.full_view_audit \
  --state-dir /path/to/full-construct \
  --ucns-source-root /path/to/pinned-ucns \
  --engine native --output /tmp/full-views-native.json
PYTHONPATH=research/english-gonol python -m english_gonol.full_view_audit \
  --state-dir /path/to/full-construct \
  --ucns-source-root /path/to/pinned-ucns \
  --engine independent --output /tmp/full-views-independent.json
```

Compare the complete `evidence` objects. There is no sampling option. The frozen
protocol requires the exact generated database bytes; a logically equivalent
rebuild with different SQLite bytes needs a newly bound protocol and complete
run. The database remains generated state; compact complete evidence is tracked.

The hosted CI gate checks sealed receipt/source integrity and audit mechanics.
It does not download the database or repeat the complete corpus run. Its small
mechanical fixtures are not evidence for inclusion or exclusion of any view.

## hmmm

The full census resolves these views' contribution to this fixed construct.
Whether the retained information improves inference still requires a concrete
task, acceptance criterion, and complete evaluation scope. Stable memory across
corpus revisions also needs explicit source-qualified identity and remapping.
