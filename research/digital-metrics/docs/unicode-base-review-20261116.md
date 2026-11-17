# Unicode separator and BASE identity repair

Area: digital metrics for the EDCM workstream. Reviewed baseline:
`c7e6aa8781eae91e3278fdc0938725532852472f`; integration base:
`7240e669c58f0fbc13049994751a882d1f337ffb`.

The final review found two reproducible defects. Appending U+2028, U+2029
or U+0085 to a participant relation or boundary note produces six rejected
positive cases despite matching graph, machine and human projections. Python's
`splitlines()` treats these source characters as physical Markdown line ends.
The structural reader now splits only CR, LF and CRLF, preserving Unicode data
and the existing terminating-line behavior. All earlier comment/fence cases
remain covered.

The receipt generator also accepts a BASE record containing an incorrect
`source_commit` followed by the expected member, or the expected member twice.
Both new rejection subcases fail at the baseline. BASE parsing now uses the
existing duplicate-member hook before validating or hashing source identity.
A valid BASE record retains its exact byte hash; the structural checker and
generator both reject each ambiguous fixture.

Local acceptance: 38 reviewed tests pass with zero skips; static linkage closes
31 contracts and 38 checks, with no witness execution or behavioral proof credit.
Stack consistency and portfolio validation pass. Source ratio seals are
recomputed and checked for all three changed Python files.

The generator's source identity changes, so the new pending receipt is generated,
replayed and attested as `native-mobius-v0-unicode-base-20261116.json`. The
README and CI consume this receipt. Earlier receipts, producer pins, work graph
and root manifest bytes remain unchanged.

## Usage

With clean exact checkouts from `WORK_GRAPH.json`, run the README's linkage,
reviewed-test, pending-generation and post-replay attestation commands. Replay
the newly sealed receipt from Stack:

```bash
PYTHONDONTWRITEBYTECODE=1 python research/digital-metrics/verify_receipt_cli.py \
  research/digital-metrics/receipts/native-mobius-v0-unicode-base-20261116.json \
  --metapat-root /path/to/exact/metapat \
  --ucns-root /path/to/exact/ucns --edcm-root /path/to/exact/edcm
```

Require byte-identical replay, clean linkage and the complete nonempty passing
reviewed suite. Hosted checks and independent review must bind the published
head and current base before merge. Rollback selects the preceding source and
its matching historical receipt rather than rewriting any receipt.

hmmm: independent replay implementation, EDCM projection/calibration and producer
signatures remain outside this structural repair.

GPT generated; context, prompt Erin Spencer.
