# English Gonol Construction

## Active construction: ordinal affixiation

`english.ordinal/1` is the selected replacement for new English construction.
[ACTIVE_CONSTRUCTION.json](ACTIVE_CONSTRUCTION.json) owns that selection.
Distance follows repeated ordinal halving; angle comes from the expanded public
gonol. Closed interiors, order, multiplicity, whitespace and source provenance
remain recoverable. There is no fallback to previous geometry.

```bash
export PYTHONPATH=research/english-gonol
python -m english_gonol profile
python -m english_gonol build /path/to/admission /path/to/ucd /path/to/new-output
python -m english_gonol verify /path/to/new-output
python -m english_gonol query /path/to/new-output 'the geometry'
```

Use the exact UCNS and source identities, dependency setup and admission commands
in [ordinal construction](docs/ordinal-construction.md). The **English ordinal
affixiation** GitHub workflow can also be run manually from Actions. It builds
and independently replays the complete pinned corpus through the supported
entrypoint. An existing output directory is never overwritten.

The prior full construction recorded 4,698 public scalar positions, 103,053 closed
words, 420,006 frames and 4,792,299 placements. A changed implementation requires
a new exact-source build and replay; prior receipts do not certify current bytes. Source and geometry receipts belong
to `english.ordinal/1`; old counts and receipts are not interchangeable with it.
These counts establish constructed scope, not semantic or inference quality.

## Authority

UCNS owns geometric objects and the ordinal operation. Stack owns this English
construction and its source/admission profile. METAPAT owns affixiation semantics;
EDCM may measure completed outputs but does not define them. Selecting this
profile does not graduate UCHC or refresh the root `libs/` snapshots. The exact
work graph in `docs/ordinal-work-graph.json` binds the consumed geometry separately.

## Identity and scale

In this text-domain construction, every admitted character is a gonol:
one exact scalar -> one shared character identity; one exact surface -> one shared word identity.
Once closed, a gonol is atomic at an admissible consuming scale, while its ordered
interior remains recoverable. This does not impose a mandatory adjacent-scale ladder.

Authority routing remains METAPAT -> affixiation semantics; UCNS -> exact geometry;
English Gonol Construction -> text-domain participants; EDCM -> measurement/evaluation only.
Construction/recovery does not validate EDCM measurement. See
[the language boundary](docs/GONOL_LANGUAGE_BOUNDARY.md).

## Replaced and retained

The structural-only build is **deprecated as a completed geometric construction**.
`structural_construct` remains the verified source-admission/replay stage consumed
by the replacement, not a competing geometry. `StructuralField` inspects that
source stage only. Its 13-file sealed import closure remains unchanged so existing
source evidence remains independently replayable.

Full construct v2, orthogonal-axis placement and constituent-overlap views are
**historical, not supported routes for new construction**. Their old build commands
are removed from this entrypoint and usage path. Retained source modules support
sealed admission and explicitly historical replay; retention grants no current
geometry authority. The supported CLI rejects retired profile commands and does
not silently return an old artifact when the ordinal constructor is unavailable.

Historical documentation and evidence:

- [Full construct v2](docs/full-construct-v2.md) and `experiments/full-construct-v2/`.
- [Four-view audit](docs/hyperspace-views-full-v1.md) and `FULL_VIEW_AUDIT.json`.
- [Hilbert candidate](docs/hilbert-inference.md), a separately declared historical
  representation, not the new relational geometry or evidence of inference quality.

The previous active profile's [segmentation contract](docs/structural-profile-v1.md)
remains the source-admission contract. Punctuation is not silently folded into word
identity; raw source, shared words, exact scalars and ordered participation survive.
Any future source-rule alteration needs its own profile and complete replay.

## Tests and migration

```bash
python -m pytest -q research/english-gonol/tests
```

Use the UCNS dependency specified by the work graph. The new default's tests cover
ordinal-only routing, retired-command rejection, selection mismatch and no-compute
profile/help. Geometry tests and full-corpus replay remain separate witnesses.

[MIGRATION.json](MIGRATION.json) retains the UCHC extraction/release standing.
Older pinned consumers are not silently upgraded by this source merge. They must
consume the new profile explicitly and replay their own contracts; historical
metrics are not renamed as ordinal measurements.

## hmmm

[Questions and remaining work](docs/ordinal-questions.md) distinguish missing
construction laws from engineering work. The radius/angle rule is settled;
global frame transport, compound origins, native Mobius lift, operator actions
and downstream inference evidence remain open.
