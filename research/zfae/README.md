# ZFAE construction research

Status: **stack-local research, incubating**. Started 2026-09-22 from Stack
`d713cc5f901d74deb902a191837ef5657dbaba94`.

The task is to construct the path by which admitted input and retained state
produce an attributable inference. Stack owns this experiment. ZFAE owns its
conceptual specification; PTCNA owns its eventual neural construction; a0 owns
runtime integration. The existing a0-betatest engine is a separate comparison
source. These names do not establish equivalent implementations.

## Usage guidance

Read the construction sequence below, then [INPUT_PROBE.json](INPUT_PROBE.json)
for the frozen first experiment and [BASE.json](BASE.json) for exact sources.
The selected source identities live in the root
[Stack manifest](../../stack-manifest.json), under `research/zfae/`.

Replay the input experiment from the Stack root with Python 3.12:

```bash
curl --fail --location \
  https://raw.githubusercontent.com/The-Interdependency/a0-betatest/5d51d70a0ae6044d1386d72bd0cada9d48887f77/backend/interdependent_lib/zfae/_parser.py \
  --output /tmp/zfae-parser.py
python research/zfae/input_probe.py --source-file /tmp/zfae-parser.py \
  --output /tmp/zfae-input-result.json
python -m unittest discover -s research/zfae/tests -v
python tools/check_stack_consistency.py
```

Source retrieval is separate from execution. A connector-fetched, byte-identical
file works with the same `--source-file` option. The runner checks its Git blob
identity before importing it and performs no network calls. It executes only
the inspected standalone parser, not the application or its package initializer.
Exit 0 means the research completed, including a FALSIFIED hypothesis; exit 2
means BLOCKED. The receipt carries source, plan, harness and work-graph identities.

## What exists

| Source | Observed surface | Construction standing |
|---|---|---|
| ZFAE `95fd37e` | Conceptual inference-event boundary; immutable fractional-phase carrier constructor | Carrier records exist. They supply no demonstrated learned input-to-answer path. |
| a0 `f4faf5c` | Producer-backed PTCNA state, explicit routing and checkpoint adapter; Zeta response evaluation | Runtime integration exists. Its code and documentation distinguish construction from usefulness. |
| a0-betatest `5d51d7` | Heuristic parser, intent selection, state transition, decoder with glyph-inscription and template routes | Separate executable candidate. This investigation executes its parser only. |
| PTCNA `a06a049` | Intended-construction gate | **BLOCKED** on UCNS neural-audit evidence; historical pre-audit scaffold is not the intended architecture. |
| UCHC `118b488` | English/Python constructs extracted from Stack | Intended construct dependency; release, Stack reconsumption and authority transition remain incomplete. Stack retains forge ownership. |

These are source-bound observations, not a whole-engine audit. PTCNA's sealed
historical experiment remains evidence about its particular scaffold/workload.
It is neither rerun nor generalized to the intended construction here.

## Construction narrative

1. **Admit the input without losing its construction.** The intended PTCNA
   language primitive is a UCNS Unicode-character gonol. Bind admitted glyphs,
   occurrences, order and source identity. Preserve the language construct's
   glyph origin, word origin, per-word definition origin and shared word
   identity when those layers participate. UCHC is the intended dependency;
   use its exact current lifecycle boundary. A heuristic feature view may be
   derived afterward, with a recoverable link to its source.
2. **Recover neural relations before choosing architecture.** Consume a UCNS
   audit of a functioning conventional neural network, including the exact
   network, weights, admitted inputs, state transitions and observations used
   to derive the construction. PTCNA owns the resulting candidate. Do not fill
   in layer counts, prime counts, role partitions, clocks, propagation or
   learning laws from the old scaffold or from an architectural picture.
3. **Construct the inference operation.** Make the admitted input, immutable
   weight identity and starting state explicit. Define which relations are
   traversed, which state changes, what makes an output admissible, and when
   inference abstains. Treat the operator as unresolved until derived or
   explicitly specified. A name, phase lock or changing output is insufficient.
4. **Demonstrate causal contribution.** Under frozen input and state, intervene
   on weights and on the proposed propagation separately. Compare the complete
   readout, task result and trace with matched controls. Declare thresholds,
   precision and any expected invariances before running. Mere output variation
   does not demonstrate useful inference; a universal requirement that every
   weight perturbation change the answer would also be wrong.
5. **Evaluate and integrate the surviving candidate.** Freeze a workload,
   held-out partition, baseline, failure conditions and resource budget before
   training or selection. Keep teacher/model outputs and fallback routes
   attributed. Route accepted runtime work into a0 after its producer gates
   close; preserve replay and checkpoint identities. EDCM may own later
   measurement contracts without defining the construction.

For organizing the research only, write

\[
  (s_{t+1}, r_t, w_t) = F_{\theta}(C(x_t), s_t).
\]

Here `C` denotes the admitted construction, `s` the retained state, `theta` the
weight identity, `r` the proposed readout, and `w` its evidence trace. This is
notation for unanswered obligations, not a selected algorithm. The equations
for `C`, `F`, state evolution, learning and readout must come from their owning
sources or remain `hmmm`. This expression supplies no neural, semantic,
consciousness or privacy result.

## First experiment: input distinctions

The proposed reuse hypothesis is that a0-betatest's complete `SemanticFeatures`
record can serve **alone** as the lossless character-input boundary. That is a
research hypothesis about reuse, not the parser's own declared heuristic promise.

The frozen fixture contains six required distinctions and three controls:
identical input, different words, and reversed word order. The six distinctions
are single ASCII glyphs, non-Latin glyphs, digit values, punctuation, case and
whitespace. Targets were selected after reading the source and before execution;
this is a directed counterexample search, not a blinded or representative benchmark.

Equality compares the complete returned record, including ordered tokens.
Exact Unicode scalar sequences are the independent identity witness, not a
replacement gonol representation. Every side is evaluated twice. Any source
mismatch, invalid plan, execution error, unstable repeat or control failure
blocks interpretation. Every pair is evaluated before classification.

Resource preflight: nine short synthetic pairs, 36 parser calls, standard-library
Python, no training, GPU, service credentials or paid model calls. The natural
terminal condition is completion of all pairs. No wall-clock stopping rule is
part of the claim.

Read [receipts/input-distinction-v0.json](receipts/input-distinction-v0.json) for
the recorded observations. The first run **FALSIFIED this reuse hypothesis**:
all six required-distinction pairs collided; all three controls and all repeats
passed. For example, `a`/`b`, `α`/`β`, and `1`/`2` each produced identical full
feature records. This does not falsify the parser's advertised heuristic role
or either complete runtime. The parser can remain an optional derived view.

A collision rejects the sole-input-boundary reuse
and directs the next step to a source/gonol/occurrence adapter. A clean finite
run only permits a broader fixture. Failed controls require harness or source
repair before either conclusion.

The path-scoped CI job repeats the frozen run and compares source, plan,
harness, work-graph and observations against the receipt. Python patch-version
differences are disclosed and excluded from semantic comparison. Changes to a
bound source, harness, plan or graph require an inspected new replay receipt.

## Domain and authority boundaries

- `the-interdependency.zfae.inference`: ZFAE is the project handle; its
  conceptual inference-event proposal is distinct from an agent, provider,
  implementation variant or proof of self-awareness. No acronym expansion is
  made globally identity-bearing here.
- `stack.zfae.input-distinction`: exact scalar identity distinguishes source
  strings. It does not establish different meanings or require every eventual
  readout to differ for different inputs. Deliberate normalization can be a
  derived view when its source remains recoverable.
- METAPAT consultation at `e4165b0` contributes the distinction between state,
  measurement, transformation and registration, and the domain-restraint rule.
  No consciousness property or physical propagation law transfers into an
  executable inference operator by structural resemblance. METAPAT root impact: none.
- ZFAE's own provisional inference-event/agent boundary remains open. The
  first probe does not equate inference with self-awareness.
- No runtime privacy claim follows from PCEA naming, deterministic state,
  digests or repeated-state linkage. Private deployment requires a separately
  validated security construction.
- Source licenses remain source-local. No upstream implementation is vendored
  by this workspace; the parser is retrieved at its immutable identity for replay.
  No release, extraction, or authority transfer is performed.

## hmmm — construction frontier

- Resolve and bind the exact UCNS neural-audit evidence required by current
  PTCNA, or conduct that audit in its owning research boundary. The current
  PTCNA gate remains authoritative until explicitly satisfied or revised.
- Complete the UCHC release/reconsumption boundary before using it as a released
  dependency; preserve the current Stack-owned construction in the meantime.
- Define the source/gonol/occurrence adapter and its recovery witness without
  collapsing distinct glyphs or substituting token IDs for the required primitive.
- Derive the state, propagation, learning and readout laws; justify any triad,
  sentinel partition or phase-lock threshold rather than inheriting old counts.
- Select a task, held-out data and admissible controls for useful inference.
- Replay and source identity are delivered evidence; inference capability remains
  the work ahead. The blueprint has acquired a workbench.
