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

## Runtime integration

Set `RuntimeConfig.uchc_database` (or `--uchc-database`) to activate native
language evidence; leave it unset to run AHBG without an installed UCHC wheel.
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

Real producer acceptance gate:
`.github/workflows/uchc-input.yml`, including
`ahbg/integration/tests/test_uchc_installed.py` against the **complete**
source-pinned corpus. A mocked reader alone is not sufficient evidence.

## hmmm

UCHC `0.1.0a2` structural admission, new ordinal construction, polyglot label
layer, binary producer and Hilbert frame bridge have **separate** implementation
and/or publication gates. This consumer must fail closed rather than silently
substitute them for the already locked `0.1.0a1` input package. AHBG may adopt
each only after its source and wheel/producer receipt, native semantics and
full-corpus or full-domain replay have been verified, with an explicit lock
migration. Independent UCHC graduation remains incomplete.
