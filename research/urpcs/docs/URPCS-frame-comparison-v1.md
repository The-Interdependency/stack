# URPCS native-frame comparison consumer v1

## Completed construction and bounded consumer

UCNS owns the exact derived comparison in `ucns.mobius_comparison` at commit
`ee3df862112811711b43afed4174592a241c373d` (UCNS PR #233). Stack consumes that
implementation; it does not copy its algebra or change the global UCNS pin.
The shared **input** authority graph is
`bd1059322ef8223d2a6531f84591e76970db67aa3982f1cbfd174d5039b5ecd5`, in that
producer's `docs/work-graphs/native-mobius-comparison-inputs.json`. The graph's
UCNS baseline is the unchanged native-law input, while the commit above is
the actual delivered comparison implementation consumed here.

This work completes a coordinate-covariant comparison on the already identified
native root-loop, **not** a transport protocol between independent origins.
The existing `RELATION_PRESENT_SHEET_RELATION_NOT_INVARIANT` receipt remains
sealed and correct for the naive endpoint product it tested.

## Domain distinction

For native framed state `(p,e)`, UCNS derives `q=p+(1-e)/2 mod 2`, and compares
complete states by `D(a,b)=q(b)-q(a) mod 2`. The source's proof establishes
reconstruction, common-motion invariance, composition, inversion, and the seam
carry. The corrected sign compares the target with a transported frame, rather
than multiplying untransported endpoint signs. Reflection negates the result;
it is covariant, not invariant under every conceivable coordinate change.

That geometry does not identify independent codec origins. `compare_local`
therefore requires the **same case, origin, and gonol anchor**. Even a shared
origin is not enough to invent alignment between unrelated roots. Separately,
the full replay consumes only attachment edges already present in the sealed
native graph and checks their recorded displacement before comparison.

The distinct-state all-pairs probe repeats the old instrument's 120 checks as
a geometric counterfactual. It is not evidence that every pair of actual codec
objects has an authorized transport edge.

## Full population, not a reduced sample

Input: `receipts/urpcs-relational-carrier-v0.json`, SHA-256
`f415c486df88cd3d0f8c6ad861d375e01553eba58f3f5a2807e1e23b097b419b`, retained
at Stack input commit `4a03f68c1ea841da5767813c6a65c41620f561f6`.

The consumer admits all 2,737 observations (948 gonol states and 1,789 member
states), independently checks each exact phase/frame against the recorded
native displacement, and uses every trace. It reproduces the old six-state,
120-check, 44-naive-product-change result, then requires zero corrected changes.
It also checks every pair sharing a gonol anchor and every native attachment
edge. Counts for these additional probes come from execution, not prediction.

`receipts/urpcs-frame-comparison-v1.json`, when sealed after replay, records the
exact counts, source hashes, producer commit, input graph, and nonclaims. The
CI artifact `urpcs-frame-comparison-evidence` retains the generated receipt,
exact consumer source archive, and source commit/tree identity. The receipt
has no runtime-dependent timestamps; two runs must be byte-identical.

## Admission and tests

`load_geometry` checks the exact producer Git HEAD and both consumed module
hashes before compiling those same byte buffers in a private namespace. It
neither executes the package facade nor admits a stale bytecode cache. The
sealed receipt hash is checked before JSON interpretation. Loaded input bytes
are checked again after measurement. Digests establish identity, not producer
signatures or newly performed authentication of the historical trace.

Six accountable consumer tests cover complete replay, strict anchor scope,
wrong producer commits, dirty consumed bytes, altered receipt bytes, and
malformed/inconsistent observations. Negative fixtures do not rewrite real
inputs. The dedicated workflow runs those checks, byte replay, and Stack
consistency against the exact PR head; frozen codec tests remain separate.

## Usage

Check out the separately pinned producer without changing `libs/ucns`:

```bash
git clone https://github.com/The-Interdependency/ucns.git /tmp/ucns-comparison
git -C /tmp/ucns-comparison checkout ee3df862112811711b43afed4174592a241c373d
UCNS_COMPARISON_ROOT=/tmp/ucns-comparison \
  python research/urpcs/frame_comparison_tests.py
python research/urpcs/urpcs_frame_comparison.py \
  --ucns-root /tmp/ucns-comparison --out /tmp/frame-comparison.json
python research/urpcs/urpcs_frame_comparison.py \
  --ucns-root /tmp/ucns-comparison --out /tmp/frame-comparison-replay.json \
  --check /tmp/frame-comparison.json
```

Output paths must be new: exclusive creation prevents overwriting prior
evidence or source. Python 3.10+ and Git suffice; this replay performs no
network requests and adds no third-party runtime dependency.

Rollback removes this consumer, its dedicated tests/workflow/report and new
receipt. Frozen URPCS v1 code, specification, vectors, previous receipts,
original analyzer, projection, WORK_GRAPH and SOURCE_RECEIPT remain unchanged.

## hmmm

Independent-origin alignment, synchronization, stream interlacing, typed event
promotion, path winding beyond modulo two, nontrivial path holonomy, protocol
adoption, security and operational/inference utility are separate claims. The
comparison completes its declared geometric task without filling those gaps
with invented relations or promoting a full UCNS carrier.
