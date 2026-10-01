# Weave source-bound evaluation, run 1

## Decision and whole-system boundary
Determine what the declared construction currently establishes, without replacing it.
The whole design includes nested hyperspace/gonol plaintext construction, a private
gonol required in recovery, multiple related streams, corpus/material participation,
section-local last/first interleaving, final interleaving and the intended asymmetric
public/private relation. A result on one operation is not a result on that whole.

## Inputs frozen before execution
- Stack PR 62 head: 247af26527d0d76558dac1dd7fd05e41ce83112e.
- Its Weave directory contains BASE.json, README.md and SPECIFICATION.md; no implementation.
- UCHC hyperspace_construct.py blob: 8b55823805c87ad8c4cc9d7451dc2eb90bdedd3a.
- User's literal interleave: last, first, next-last, next-first, continuing inward;
  section arities illustrated by 5, 7, 3, followed by interleaving the whole.
- User's 'arity three, minimum' does not establish a minimum of three stages.

## Explicit experimental choices, not additional user laws
The composed-operation profile feeds one stage's output to the next, retains section
order, and uses explicitly supplied positive section lengths. Equal-partition cases
use lengths divisible by every selected arity: no invented remainder allocation.
Empty input is tested for the end-interleave primitive alone. Empty sections and
partial partition rules are not silently selected.

The independent inverse uses a closed-form position formula, not the encoder's
implementation or a permutation exported by it. None of these operations is named
'encrypt', 'decrypt', 'gonol', 'keygen', or a complete Weave implementation.

## Frozen checks and evidence domain
1. Exhaust all 8,191 binary inputs of lengths 0 through 12 for the end operation.
2. Exhaust all positive ordered partitions of lengths 3 through 12 with at least
   three parts. Distinct position labels test bijection on every position, implying
   the same recovery for any values occupying those positions.
3. Enumerate all schedules over (3,5,7) of lengths 1 through 8 on 105 positions.
   Compare exact induced maps, record collisions and stage periods. Distinct
   schedules are not presumed to define distinct maps.
4. Execute the stated (5,7,3) sequential profile on lengths 105, 210, 420, 840,
   8,400 and 67,200. Preserve position witnesses and exact inversion.
5. Attack the fixed-map profile at lengths 105, 840 and 8,400 using binary position
   labels and no access to the schedule in the attack function. Confirm inferred
   inverse on 64 held-out generated bitstrings per length. This attack assumes the
   same positional map across queries. No transfer to message-dependent maps or
   the unimplemented complete system.
6. Check weight preservation and constant-input witnesses. State the algebraic
   scope: rearranging bits, not the complete gonol/corpus/private-key construction.
7. Exercise refusal of malformed inputs and missing whole-system implementation.
   Readiness is not tested cryptographic strength; no substitute adapter is used.

## Preflight and terminal condition
Python standard library only, deterministic fixtures, no network, no secrets, no
external paid API. The largest enumerated table is 9,840 maps on 105 positions.
Expected memory is well within this container's available memory; output is small.
Finish the complete declared finite domains or report execution failure. There is no
scientific wall-clock stopping rule. SHA-256 identifies evidence, not encryption.

## Failure attribution
- A runtime disagreement in literal end-interleaving: implementation defect until
  independently reproduced against the written law.
- A schedule collision: falsifies assistant-added schedule-uniqueness claims, not
  the user's whole design.
- Fixed-map attack succeeds: that profile supplies no confidentiality against the
  declared attack. It says nothing decisive about the absent required relations.
- Missing native relation: BLOCKED for full execution, never FALSIFIED.

## Usage
Run `python probe.py > receipt.json`; run again and compare the exact output bytes.
Read REPORT.md with the receipt. Do not interpret a component pass as system approval.

## hmmm
Original thirteen-law conversation export was not recovered. The retrieved uploaded
URPCS law files describe the retired authenticated codec, not the intended encryption.
Thread/corpus original details are present here only as conversation context, not a
recovered exact transcript. Public/private-gonol binding and full composition are not
implemented in the inspected Weave directory. No replacement has been invented.
