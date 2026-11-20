# Complete matrix publication admission

At reviewed head `cd2d68cf329d62c3a8d1950a0192af76b8bb4063`, one verified B-only
case with matching generation counts reaches archive publication. The subsequent
coverage record would claim all 930 pair words and 393 transport schedules. This
reproduces comment 4582161488: receipts bind individual cases but do not establish
the promised complete composition census.

Publication now requires an exact multiset match against every structural row in
`matrix.schedules()`, excluding only each case's ID, selected private parameters
and message. It preserves schedule order and multiplicity, transport initial-lane
declarations and native-cycle round declarations. It also requires the selected
receiver controls to agree with those declarations and validates the frozen plan's
schema/status/salt encoding before publishing their corresponding claims. Existing
per-case checkpoint validation runs first; the census gate runs before ZIP creation
or coverage/result writes. Small fixtures remain usable for private generation.

All 25 integrity tests pass. The new witnesses admit the complete 1,841-row census
in either order, and reject missing, added, replaced and same-family substituted
schedules, mismatched lane/round controls and invalid publication metadata. A real
freshly verified one-case fixture refuses publication without changing private
evidence. During archive writing each case is revalidated and the checked buffer
supplies both the wire and its digest; a fault witness changes the backing file
after validation and confirms coherent archive bytes/checksums with bounded memory.
The full-census positive is structural data validation, not a new replay
of 1,841 encrypted cases. The five snapshot tests and 196 current Weave tests pass
with zero skips; the latter's source-stability guard passes.

The original source bundle/lock, vectors, blind archive and all 1,841 wires, v1 and
earlier observation records remain unchanged. The actual operator archive was not
accessed or migrated; the original full-corpus harness was not rerun. This repair
uses synthetic fixtures and conducts no attacker trial. Exact source identities
and preservation checks are in [CENSUS_REPAIR_20261116.json](CENSUS_REPAIR_20261116.json).
`SHA256SUMS.cd2d68c` retains the prior checksum list; `SHA256SUMS` covers current files.

hmmm: complete declared composition coverage does not implement the missing native
private construction, authentication or replay-state laws, and is no security proof.
Frozen status and salt shape validate a declaration, not its authenticity or entropy.

GPT generated; context, prompt Erin Spencer.
