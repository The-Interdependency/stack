# AHBG ↔ UCHC: native consumer contract

## Done when

AHBG installs the source- and wheel-locked UCHC candidate; independently verifies
its package files and complete-corpus identity; constructs, queries and replays
native English input; preserves unknowns; exposes the exact evidence to the
agent observation and persisted turn record; and refuses changed artifacts or
unlicensed operations. The AHBG engine and UCNS movement remain unchanged.

**Authority:** UCHC constructs. UCNS owns geometry. Stack remains the English
forge pending graduation. AHBG observes those native objects, never reimplements
them or treats structural similarity as a game rule or consciousness proof.

## Source and installation

The canonical immutable candidate selection already exists at
`research/zfae/UCHC_INPUT.json`. AHBG intentionally reuses the existing
`research/zfae/uchc_input.py` verifier. The candidate is UCHC `0.1.0a1`,
source `3d82007b88f74ded88ca913d6e85bcd6f6ff024d`.
Wheel SHA-256, logical receipt, and database byte SHA-256 are **read from the
trusted lock**, never discovered from the supplied database or guessed at run time.

Use `.github/workflows/uchc-input.yml` as the full-corpus reproducibility and
installed-artifact acceptance path. It fetches exactly pinned sources, builds
and verifies wheel bytes, constructs the full OEWN corpus, and runs both the
existing ZFAE consumer and AHBG's real native-language integration tests.

For a local install, first verify the wheel SHA-256 against the lock and
install the exact wheel from a local archive into a separate environment.
Use the corresponding verified complete `construct.db`:

```bash
python -m ahbg.integration.uchc \
  --database /artifacts/construct.db \
  text 'alpha letter alpha' --source-id 'ahbg:query:1'

python -m ahbg.integration.uchc \
  --database /artifacts/construct.db word alpha

python -m ahbg.integration.uchc \
  --database /artifacts/construct.db definition 1

python -m ahbg.integration.uchc \
  --database /artifacts/construct.db replay /artifacts/saved-frame.json

PYTHONPATH=.:libs/ucns/src python -m ahbg.runtime play \
  --agent a0 --turns 3 --out /tmp/ahbg-native \
  --uchc-database /artifacts/construct.db
```

The query CLI returns a source-bound frame, UCHC-native word object, complete
native definition with recovered source text, or verified replay. Definition
identities are corpus-local, not assumed universal IDs. In Python:

```python
from pathlib import Path
from ahbg.integration.uchc import UchcSession, UchcSettings

with UchcSession(UchcSettings(Path("/artifacts/construct.db"))) as uchc:
    frame = uchc.resolve_text("alpha letter alpha", source_id="ahbg:probe")
    frame.require_complete()
    assert frame.recover_utf8() == b"alpha letter alpha"
    assert uchc.replay(frame.to_bytes()) == frame
    all_candidates = uchc.definition_candidates(frame)
    assert all_candidates
    print(uchc.capabilities)
```

## Structural profile (separate exact wheel)

The **newer** UCHC `0.1.0a2` is also independently consumable. Its real
`StructuralField` performs text construction, admitted word/definition
recovery, exact record replay, and registered ordered-text/sentence composition.
It preserves both definition constituent topologies and definition succession.
It never supplies missing UCNS geometric displacement.

The exact candidate identities are in
[`UCHC_STRUCTURAL.json`](UCHC_STRUCTURAL.json): UCHC source
`c18d984438bc30764edb05fd5ccc05691958a24e`, wheel hash
`7f05fbbb...`, complete 711,983,104-byte structural database hash
`13ba2411...`, logical receipt `26ab095f...`. The consumer verifies the
**full** stored identities, not the abbreviated identifiers printed here.

Build the full structural field through the exact wheel as specified in
[`ahbg-uchc-structural.yml`](../../.github/workflows/ahbg-uchc-structural.yml),
then run:

```bash
PYTHONPATH=.:libs/ucns/src python -m ahbg.runtime play \
  --agent a0 --turns 3 --out /tmp/ahbg-uchc-structural \
  --uchc-structural-field /artifacts/structural-field
```

Native Python surface:

```python
from pathlib import Path
from ahbg.integration.uchc_structural import (
    UchcStructuralSession, UchcStructuralSettings
)

with UchcStructuralSession(
    UchcStructuralSettings(Path("/artifacts/structural-field"))
) as uchc:
    graph = uchc.construct("Dr. creates geometry.")
    assert uchc.replay(graph) == graph
    word = uchc.word("geometry")
    relation = uchc.compose(graph, relation="ordered-text")
```

The input and structural profiles use **different pinned wheel versions and
different databases**. One Python process selects exactly one; attempting to
activate both fails explicitly. Multiple profiles can be compared through
separately installed processes without redefining their geometric authority.

## Runtime integration

Set `RuntimeConfig.uchc_database` (or `--uchc-database`) to activate native
input evidence, or `uchc_structural_field` (or `--uchc-structural-field`) for the
separately pinned structural profile; leave both unset to run AHBG without an
installed UCHC wheel.
An optional `uchc_lock` selects an explicitly trusted artifact lock.
`uchc_require_complete=True` rejects unadmitted glyphs/words rather than
concealing them. `uchc_max_text_bytes` is an optional explicit memory bound:
oversized inputs fail rather than truncate. The default does not impose a
hidden text-length limit.

Each inbox message containing a `text` field is resolved in original order.
No normalization, case folding, punctuation erasure, or inferred translation.
A message's exact source-scoped native input frame and receipt appear in
`observation.language_evidence` for a harness turn, alongside the unmodified
`observation.inbox`. These are then persisted in
`result.json.turn_records[].uchc_evidence`; the immutable UCHC wheel,
database and lock identities appear in `result.json.provenance.uchc`.
No modification to UCNS geometry, legal actions, game transitions, agent
capabilities, or reward signals occurs.

All definitions are available via native
`session.word`, `session.definition`, `session.recover_definition`, and
`session.definition_candidates`; the inline frame preserves source-order
definition IDs and all native word identities. Semantic selection is not
licensed. Unknown input is retained as `PARTIAL` unless strict admission is
explicitly enabled, which raises `UchcConsumerError`.

## Rejection and proof

- Missing UCHC wheel, editable/source-shadowed installation, wrong version,
  altered installed files or wheel hash: refuse before game initialization.
- Wrong complete construct SHA-256, logical receipt, schema or integrity:
  refuse before game initialization.
- Unexpected input shape, non-scalar Unicode, incomplete strict admission,
  stale frame, mismatched record, unsupported/unpublished operation or
  altered replay: refuse with an explicit error.
- Neither a passing test nor a matching hash proves external authentication,
  semantic truth, sense choice, neural inference, cross-origin Hilbert geometry,
  or consciousness.

Fast wiring gate:
`PYTHONPATH=.:libs/ucns/src python -m unittest discover -s ahbg/runtime/tests -q`

Real input producer acceptance gate:
`.github/workflows/uchc-input.yml`, including
`ahbg/integration/tests/test_uchc_installed.py` against the **complete**
source-pinned corpus. Structural acceptance independently executes
`.github/workflows/ahbg-uchc-structural.yml` against the distinct complete
UCHC `0.1.0a2` field. A mocked reader alone is not sufficient evidence.

## hmmm

UCHC `0.1.0a2` structural admission now has its own independent AHBG
consumer and complete-corpus gate. The new ordinal construction, polyglot
label layer, binary producer and Hilbert frame bridge still have separate
implementation and/or publication gates. No unfinished machinery may be
silently substituted for either pinned candidate package. AHBG may adopt
each only after its source and wheel/producer receipt, native semantics and
full-corpus or full-domain replay have been verified, with an explicit lock
migration. Independent UCHC graduation remains incomplete.
