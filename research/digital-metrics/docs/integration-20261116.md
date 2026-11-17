# Current-main integration

While #46 was under review, Stack main advanced to
`7240e669c58f0fbc13049994751a882d1f337ffb` through UCHC PR #111. The old PR
base field still named the earlier commit, but a fresh Git fetch and merge-tree
inspection reproduced two actual manifest conflicts. No stale-state inference is
used as conflict evidence.

The merge preserves every latest-main participant and human projection and adds
only #46's five research participants. The work-graph digest is recomputed; no
producer pin, authority or operational skill is advanced by #46. Consistency
passes with seven repositories and 72 research participant identities.

Because the receipt binds the root manifest, the prior receipt no longer describes
the integrated checkout. Its bytes remain historical. A new pending receipt is
generated, freshly replayed and attested at
`receipts/native-mobius-v0-integration-20261116.json`, then replayed byte for byte.
Its payload is `528a69e8440f24decf71cadd2e776922ae7ea9cede30058833b748944d68a7f3`.
CI now compares this new receipt. The original and November 15 receipts remain
unchanged. The generator, protocol and producer identities are unchanged.

All 36 reviewed tests and static linkage (30 contracts, 36 checks, zero behavioral
verification credit) pass. Portfolio validation passes. Run the initial repair's
acceptance commands with the new receipt path. The HTML/comment boundary repairs
and their failure witnesses remain documented in
[the review follow-up](review-followup-20261116.md).

hmmm: hosted checks and current-head review remain separate; the receipt supplies
no EDCM measurement, signature or authority transfer.

GPT generated; context, prompt Erin Spencer.
