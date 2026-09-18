# Composition option set: provenance and verification scope

Recorded: 2026-09-18 UTC. Standing: **stack-local research notes**.

## Ownership and exact inputs

The companion [work graph](composition-option-set-work-graph.json) binds the
following **document consultation** identities. It is separate from the root
stack manifest: it neither rebases `research/metapat/BASE.json`, refreshes `libs/`,
imports an implementation, nor changes repository authority or workspace lifecycle.

| Source | Exact commit | Role |
|---|---|---|
| The-Interdependency/stack | `545e135e2efbbcf29f033ab5530ac4876a68b718` | Starting repository state and edit owner |
| The-Interdependency/metapat | `e4165b0cac9eca41daef9c2f941881028ca55d48` | Current semantic and domain-restraint documents consulted |
| The-Interdependency/ucns | `d8f0c505e6f5132e9711de0e7c24e4718e77e51a` | Current geometric scope and unresolved-operation boundary consulted |
| The-Interdependency/skill-lib | `dd5027d99516831c0dcb83a176a67140d3819b66` | Current evidence, canon, domain-claim, and work-graph discipline |

The workspace's unchanged imported METAPAT base remains
`34d954aa1e2092e615b03a180500f6b6977f501e`, as recorded in [BASE.json](BASE.json).
Newer document citations above are explicit comparative inputs, not a claim that
the older imported view contains those newer statements.

## Source documents

| Document | Git blob SHA |
|---|---|
| [METAPAT AXIOMS.md](https://github.com/The-Interdependency/metapat/blob/e4165b0cac9eca41daef9c2f941881028ca55d48/AXIOMS.md) | `90b7fea71369f08bee09d4fa100491a66e0c498e` |
| [METAPAT POSTULATES.md](https://github.com/The-Interdependency/metapat/blob/e4165b0cac9eca41daef9c2f941881028ca55d48/POSTULATES.md) | `e6003140a569e26fbe22ac63f34c0525b27cab48` |
| [METAPAT DOMAIN_RESTRAINT.md](https://github.com/The-Interdependency/metapat/blob/e4165b0cac9eca41daef9c2f941881028ca55d48/DOMAIN_RESTRAINT.md) | `8d3626384c55350832767ba6f4fa913f48a5afd0` |
| [UCNS README.md](https://github.com/The-Interdependency/ucns/blob/d8f0c505e6f5132e9711de0e7c24e4718e77e51a/README.md) | `a7ac28b5f2c93b15a24f7b3ee69aa9a2b00e84fb` |
| [skill-lib AGENTS.md](https://github.com/The-Interdependency/skill-lib/blob/dd5027d99516831c0dcb83a176a67140d3819b66/AGENTS.md) | `9aa309971ece74234a8ba8da69fd8c42d0dccdcd` |

The named skills were read through canonical skill-lib. Already-resolved doctrine
was retained across this conversation; current work-graph and stack-update
instructions were checked for this repository update.

The Human Simplex statements and the scope correction originate in Erin's current
conversation. The candidate equations originate in the assistant's subsequent
response and are refined here to make their limits explicit. The user requested
"show me the math" and then "update where appropriate". Those instructions authorize
recording the proposal, not an empirical or universal truth claim.

The external quantum teaching source is linked in the mathematics note. The exact
two-qubit calculation is self-contained; no external webpage freshness or immutable
byte identity is claimed for that explanatory reference.

## Edit ownership and non-transfer

- `research/metapat/` owns these candidate notes only.
- METAPAT retains semantic authority; UCNS retains geometric/operation authority.
- The Human Simplex is an application sense, not a replacement root definition.
- Mathematics, physics, graph theory, and human needs retain their own meanings.
- No proof, theorem, measurement, empirical, certification, consciousness, or
  licensing standing transfers through these links or this work graph.
- The related From Photons to the Macroverse package is linked for discovery only.
  Its paper fragments, source receipts, claim ledger, and frozen protocol are not
  amended by this note or used to validate it.

## Verification scope

The update checks the finite graph example, the two-qubit joint-state witness,
local document links, and the consultation work-graph digest. These are bounded
document/example checks, not tests of a universal model or a UCNS implementation.

Local verification for this update:

| Check | Outcome |
|---|---|
| Finite graph cuts, complementary cuts, isolated component | PASS for the supplied examples |
| Both Bell-state marginals, orthogonality, joint expectations | PASS using exact rational density matrices |
| Consultation work-graph digest and source-commit shape | PASS |
| Relative document links | PASS, 20 links checked |
| From Photons to the Macroverse existing contract suite | PASS, 14 tests |
| Repository portfolio report validation | PASS |
| Git whitespace check | PASS |
| Equation renderer | hmmm: KaTeX unavailable in the verification environment |
| Full-history root stack consistency | PASS after the separately requested EPAC placement repair; the initial document-only baseline failed |

The root stack consistency checker at the starting commit, after fetching full
history, reports this pre-existing error:

> epac.graduation: forge Python implementation has returned

The user subsequently requested "repair epac placement". The six active carrier
experiment/test files now live in [`research/epac-carrier/`](../epac-carrier/),
with explicit Stack provenance and pinned independent EPAC source consumption.
Historical fixtures and retirement evidence remain byte-identical. The root
consistency gate and all 17 relocated research tests pass; all four report
outputs match their pre-move canonical bytes. The root manifests, authority
projections and EPAC workflow describe the repaired placement. The original
consultation graph still records the true failure at its pinned starting commit.

## Usage guidance

From the Stack repository root, verify the document-consultation graph identity:

```bash
python - <<'PY'
import hashlib
import json
from pathlib import Path
p = Path('research/metapat/composition-option-set-work-graph.json')
graph = json.loads(p.read_text())
payload = {name: graph[name] for name in ('repositories', 'boundaries')}
digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
assert digest == graph['work_graph_sha256']
print(digest)
PY
```

The root consistency command is `python tools/check_stack_consistency.py` and needs
the historical Git objects cited by EPAC's transition record. Recompute the graph
digest whenever the companion consultation graph changes. A matching digest proves
record consistency, not authenticity or scientific validity.

## hmmm

- An externally immutable conversation transcript identity is unavailable.
- The wider source pins remain exactly as declared by the root stack manifest.
- Candidate first principles, admission laws, physical coverage, and UCNS
  preservation maps remain unresolved; see the mathematical note's claim ledger.
