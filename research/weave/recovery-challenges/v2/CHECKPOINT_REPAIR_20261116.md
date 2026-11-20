# Frozen-case checkpoint binding

At reviewed head `bea565d2c8ccfd7e6b29f696caedc3189a293bdb`, a changed message
and schedule still reuse the original VERIFIED receipt. Packaging reaches archive
publication with that inconsistent plan. Both behaviors reproduce review comment
4581976715, independently of the earlier frozen-source startup repair.

Current `weave.challenge-checkpoint/v1` receipts bind SHA-256 of the entire frozen
case row using sorted compact JSON. One shared validator checks that binding, the
opaque ID, VERIFIED state, wire hash/size, message size and fresh-receiver marker
for both resume and packaging. Failed, malformed, historical/unbound or mismatched
receipts remain rejected and are never rewritten. Generation and packaging also
reject empty/duplicate case plans and packaging requires matching planned counts.

The 20-test integrity suite passes without skips, including changed message,
schedule, parameters and family; missing binding/verification fields; refused
publication before ZIP creation; duplicate/empty plans; and existing containment,
interruption and orphan-wire behavior. A positive separate-directory migration
recomputes and freshly verifies the unchanged synthetic wire while retaining the
original receipt/wire bytes, timestamps and original wire inode. The five source
snapshot tests and all 196 current Weave tests also pass, zero failures/errors/skips.
The full suite's source-stability guard passes.

Run and migration commands are in [README.md](README.md); exact source identities
and checks are in [CHECKPOINT_REPAIR_20261116.json](CHECKPOINT_REPAIR_20261116.json).
The original source lock/bundle, adapter vectors, blind archive and all 1,841 wires,
v1 subtree and earlier observations remain unchanged. The startup repair's 16-test
and source-digest observations remain historical; this follow-up has 20 integrity
tests and its own current-source receipt. `SHA256SUMS.bea565d` retains the preceding
checksum list, and `SHA256SUMS` covers current files.

Rollback this receipt/validator change together; do not relabel original receipts
as newly verified. Old operator evidence can be copied without receipts into a
separate private root and freshly verified as documented. The actual original
operator archive was not accessed or migrated, and its full-corpus harness was
not rerun. This repair uses synthetic data and conducts no attacker trial.

hmmm: a case digest is not a signature or an authenticator of hostile operator
input. Same-input resume reuses prior evidence rather than claiming fresh execution
on every invocation. Full-Weave construction and security obligations remain open.

GPT generated; context, prompt Erin Spencer.
