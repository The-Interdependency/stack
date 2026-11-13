# Cross-base recurrence controls v1

Status: exploratory follow-up, fixed before control execution. The pi results
were already observed; this is not a preregistered discovery or held-out test.

## Question and fixed design

Does pi's count of distinct primes present in at least two bases, using canonical
blocks of lengths 2–4, exceed an ordinary same-number cross-radix baseline?
Keep EXPERIMENT.json's seven bases, 500 fractional symbols, and 2400-bit
resolution horizon. The primary statistic is the common-horizon recurrence
count (previously 8); fixed-500 count (12) is secondary. Do not test the exact
eight values as if they were selected before seeing pi.

Run exactly 199 replicates, with seed text `stack/pi-radix/controls/v1`.
SHAKE256 domain-separated counter bytes supply reproducible pseudorandom draws;
this is a simulation assumption, not a theorem of randomness.

Primary control: draw one 8192-bit integer J per replicate; convert the SAME
interval [J/2^8192, (J+1)/2^8192) to every radix using integer arithmetic.
Require the whole interval to determine each requested 500-symbol prefix;
otherwise fail, without retrying or silently conditioning the sample.
This retains correlations caused by expressing one number in several bases.

Secondary control: independently Fisher–Yates shuffle pi's digits in each
base and profile, using rejection-sampled bounded integers. Preserve each
profile's exact digit histogram, length, alphabet, and terminal sieve, but
destroy order. These shuffled streams are NOT one common number, and remain
a sensitivity diagnostic rather than the primary null.

Report every replicate's two recurrence counts, means, medians, min/max,
central 95% empirical range and upper-tail Monte Carlo rank (1+# >= observed)/200.
No automatic significance claim: bases and statistics arose in exploration.
Do not infer pi normality, independence, entropy, or a base-independent law.

## Falsifiable obligations and file plan

- pi_radix.py + existing tests: repair horizon truncation, configurable report
  lengths/labels, unequal-prefix angle comparisons, and unbounded base allocation.
- recurrence_controls.py: exact common-number conversion, histogram control,
  deduplicated recurrence counter, source-bound receipt and report.
- tests/test_recurrence_controls.py: known-answer and boundary rejection tests,
  independent trial-division counter, planted recurrence, histogram preservation,
  deterministic replay and source-hash verification.
- receipts/ and docs/: deterministic outputs, including all replicate counts.
- README.md: reproduction commands and interpretation.

No participant, authority, canon, UCNS, encryption, or merge change.
Failure is visible; a normal-range result retires the recurrence count as evidence
of an anomaly in this bounded comparison, not the broader search for invariants.

hmmm: one number gets seven outfits; the control must keep the person inside them.
