# OEWN 2025 full-corpus orthogonal definition affixiation — v0

Status: `UNRESOLVED` experimental full-corpus run. Standing: implemented
experimental candidate inside English Gonol Construction only. Nothing here is
UCNS geometry canon, an English lexical truth claim, a word embedding, or a
measurement of semantic quality.

## Question

Run the **complete** pinned OEWN 2025 corpus through English Gonol
Construction, reusing every already-closed word gonol, and affixiate each
word's ordered definitions orthogonally without imposing any semantic axis or
carrier bucket beforehand.

Boundary contract applied:

- **Do not sample**: every lexeme, sense, and definition is processed.
- **Do not hash-place**: gonol identity comes from exact surface identities.
- **Do not bucket words onto carriers**: no carrier or angle cell exists here.
- **Do not stop on collisions**: there is no collision concept in this run.
- **Do not rebuild lexical identity**: each unique surface is closed once and
  reused everywhere it appears.
- **Do not invent orthogonal geometry**: the exact UCNS orthogonal-affixiation
  geometry remains unresolved, so the run closes every definition gonol from
  existing authority and exposes the affixiation boundary as `hmmm` with no
  substitute.

The earlier `1..7` hash-carrier sweep is unchanged and remains a control
experiment; it supplies no placement rules to this run.

## Method

1. Load the pinned OEWN 2025 YAML tree
   (`globalwordnet/english-wordnet@dc343f2683279ecbb13fab4e2fd778d7b162d287`,
   tag `2025-edition`, 73 files, verified counts).
2. Collect every surface used by the corpus: lemmas, lemma token splits,
   forms, form token splits, and every whitespace token of every definition.
   Single-token surfaces become word gonols; multiword surfaces are
   compositions, not word gonols.
3. Close each single-token surface exactly once:
   `construct_gonol(scale="word", source=surface, source_id="oewn:surface:<surface>")`.
4. Reuse that one word gonol everywhere the surface appears. Multiword lemmas
   that own senses are composed from their ordered constituent word gonols
   through the existing recursive scale
   (`scale="recursive"`, `relation="oewn:lemma:<lemma>:<pos>"`).
5. For every sense of every lexeme, for every definition of its synset, close
   a definition gonol from the definition's ordered constituent word gonols:
   `construct_gonol(scale="definition", participants=(G(w_1),...,G(w_m)),
   relation="oewn:sense:<sense_id>", source_id="oewn:def:<sense_id>:<index>")`.
6. Order each word's definition gonols and record the requested affixiation
   sequence `G(w); affixiate; D_1 ⊥ D_2 ⊥ ... ⊥ D_n` with
   `geometry_state = hmmm` and the UCNS boundary reason. No substitute
   geometry is implemented.
7. Persist word identity, sense identity, constituent identities, definition
   order, orthogonal affixiation order, provenance digests, corpus hashes,
   constructor and UCNS authority identities, and a deterministic replay
   digest.

## Frozen run

- Module: `english_gonol.definition_affixiation_run`
- Manifest: `experiments/oewn-affixiation-v0/manifest.json` (committed)
- Records: `experiments/oewn-affixiation-v0/records.jsonl` (545,890 lines,
  ~265 MB; local persisted state, not committed, bound by `records_sha256`)
- Replay:
  `python -m english_gonol.definition_affixiation_run --source-root /path/to/oewn-2025/src/yaml --out-dir experiments/oewn-affixiation-v0 --workers 2`

## Results

| quantity | value |
|---|---|
| OEWN lexeme entries | 135,969 |
| OEWN synsets | 107,519 |
| OEWN senses | 185,129 |
| OEWN relations | 244,727 |
| word gonols closed | 122,520 |
| multiword lemma compositions | 53,060 |
| definition gonols closed | 185,155 |
| affixiation records | 185,155 |
| source tree sha256 | `3a46546a1ffbb4aed98990535ad5155c69be12ad09fdf093701b257d2a3e468f` |
| records sha256 | `0eb37abb8975a1896bb80dfa02cb11b736cc352a798ee147263560113eb9ee9a` |
| replay digest | `a67ed0a1af86710fa880a6b5b6eae0ba3861a22bcd7b12076996dde6cf3bd729` |

- `word_gonols` = unique single-token surfaces (lemmas + form tokens +
  definition tokens). Each was closed once and reused; no lexical identity was
  rebuilt.
- `definition_gonols` = sense-definition pairs over the whole corpus, i.e.,
  every definition belonging to every sense of every word. No sense or
  definition was sampled out.
- `affixiation_records` = one per definition gonol, carrying its per-word
  order, the previous orthogonal target, and the exposed `hmmm` geometry
  boundary.

## What is constructed vs what remains boundary-exposed

Constructed and persisted (existing authority):

- the complete closed word gonol registry for the corpus;
- recursive compositions for every multiword lemma that owns senses;
- a definition gonol for every sense-definition, composed from the exact
  ordered constituent word gonols;
- per-word ordered affixiation sequences.

Boundary-exposed, not implemented:

- the geometric realization of `D_1 ⊥ D_2 ⊥ ... ⊥ D_n`. The exact UCNS
  orthogonal-affixiation geometry is unresolved, so every affixiation record
  carries `geometry_state = hmmm` and the reason string. No orthogonal axis
  was invented and no placement was substituted.

The resulting persisted structure is therefore the full recursive
word -> definition -> constituent word gonol graph, with the orthogonal
affixiation geometry explicitly pending UCNS authority.

## hmmm

- Emergent-relationship analysis is deferred until after construction, as
  instructed; it has not been performed here.
- The exact UCNS orthogonal-affixiation geometry remains unresolved; until it
  is bound, `D_1 ⊥ D_2 ⊥ ... ⊥ D_n` cannot be geometrically realized.
- Whether definition gonols should bind the raw definition text as a source
  unit (rather than as a receipt field only) is an open construction decision.
- The word surface registry is surface-keyed; exact homograph/part-of-speech
  identity is preserved in the sense records, not by splitting word identity.
