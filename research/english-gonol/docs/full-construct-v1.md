# English Gonol full construct v1

Status: stack-local research construction. The corpus supplies evidence; UCNS
supplies established geometry only. No unresolved geometric quantity is filled
by convention.

## Construction identity

Builder: `english_gonol.full_construct_run`

Source evidence: Open English WordNet 2025 at
`globalwordnet/english-wordnet@dc343f2683279ecbb13fab4e2fd778d7b162d287`.

Public Gonol authority: the exact 157-position carrier in UCNS. The builder
verifies the pinned UCNS checkout and `public_gonol.py` bytes before a production
run.

## Fixed identities

The construct admits exactly one identity for each exact Unicode scalar it
uses and exactly one identity for each exact word surface it uses.

```text
character scalar -> one character id
word surface      -> one word id
word              -> ordered character-id references
```

Repeated characters reuse the same character identity while their positions in
a word preserve order and multiplicity. Repeated words reuse the same word
identity everywhere they occur.

No normalization, case folding, stemming, lemmatizing, punctuation folding, or
confusable substitution changes an admitted surface.

## Word-origin definitions

Every definition of a word points back to the same shared word identity as its
origin. Definitions do not create alternate copies of the word.

Source sense order and source definition order are preserved as ordinal
evidence. The OEWN loader must therefore preserve the original order of each
`sense` list; sorting by sense identifier is forbidden because it changes the
ordinal evidence.

Sense ids and synset ids remain provenance locators on definition evidence.
They are not promoted to gonols.

## Evidence channels

Three distinct evidence channels are retained:

1. **ordinal** — the source order of the definitions belonging to the word;
2. **semantic** — OEWN sense relations, synset relations, and synset membership
   resolved to the already-existing shared word identities where possible;
3. **sentence-context** — the exact ordered word identities appearing in the
   definition, including source offsets.

The declared resolution rule is:

> preponderance relative to the rest of the sentence in which the word appears

The builder records those inputs but does not invent a numeric weighting law.
The geometric construction must determine any resulting weight, direction,
distance, movement, or equilibrium.

## Materialized representation

The artifact is normalized once in SQLite:

```text
meta
characters
words
word_characters
definitions
definition_words
semantic_evidence
unresolved_semantic_evidence
```

`semantic_evidence` resolves source relation targets to shared word identities.
`unresolved_semantic_evidence` preserves source relation targets that cannot yet
be resolved to an admitted word identity. Incompletion remains visible rather
than being guessed away.

The following old architecture is forbidden in this builder:

```text
sentence/sense/synset/n-gram singleton tables
occurrence-object ledgers
closure graphs or cycle covers
relation circles made from spelling positions
alphabetical or otherwise synthetic tangency pairings
attention/Mobius bookkeeping views
serialized duplicate copies of the database
```

The builder asserts that none of those tables exist before accepting a run.

## Geometric boundary

The Public Gonol carrier position of an admitted scalar may be recorded because
that mapping is established UCNS geometry. No further geometry is synthesized.

The construct does not contain invented:

```text
weights
vectors
coordinates
centers
radii
tangencies
motion
```

Those are outputs only when an established geometric law derives them.

## Replay

The receipt is SHA-256 over a canonical ordered walk of the normalized logical
rows, not over raw SQLite file bytes. This proves the logical construction can
be replayed while avoiding a second giant serialization of the same state.

Production command:

```bash
python -m english_gonol.full_construct_run \
  --source-root /path/to/oewn-2025/src/yaml \
  --ucns-source-root /path/to/ucns \
  --out-dir experiments/full-construct-v1
```

Output:

```text
construct.db
manifest.json
```

## Acceptance

A completed run must demonstrate all of the following:

- one row per exact character identity;
- one row per exact word identity;
- exact character order and multiplicity for each word;
- every definition bound to one shared origin word;
- source definition ordinal preserved;
- ordinal, semantic, and sentence-context evidence kept distinct;
- relation targets either resolved to existing word ids or preserved visibly as
  unresolved evidence;
- no forbidden evidence-as-gonol tables;
- no invented geometric output;
- deterministic logical receipt on replay.

## hmmm

The exact UCNS law mapping ordinal + semantic + sentence-context evidence to
geometric displacement remains unresolved. That is the next genuine geometric
boundary. It is not permission to invent weights, directions, distances,
centers, radii, tangencies, or movement in the English builder.
