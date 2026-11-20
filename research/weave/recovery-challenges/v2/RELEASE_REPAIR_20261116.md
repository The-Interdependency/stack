# Verified-case release and grading

Review comment 4582074415 reproduces a remaining defect at
`4fdfb062b119c874d22b84cdd5199350e9edfd1e`: a verified B case whose plan changes
to W can still be exported at level six. Its supplied inverse produces bytes
that fail private grading. Resume and packaging reject the changed row, but the
release/grading path bypasses that check.

`load_verified_case` now owns case/receipt validation and returns the exact checked
ciphertext buffer with its receipt. Resume and packaging retain their checkpoint
API through that same loader. Release and grading load one case from the admitted
frozen plan, preserve ciphertext-symlink refusal, and validate its binding before
writing any export or evaluating a candidate. Export writes both challenge bytes
and receiver-request bytes from the one verified buffer, without reopening the
ciphertext after validation.

The 22-test integrity suite passes with zero skips. Changed message, schedule,
parameters and family refuse at every disclosure level and before grading; altered
ciphertext also refuses. Another witness changes the backing file immediately
after verification and proves the export uses the admitted buffer consistently.
Existing containment, checkpoint refusal and separate-directory migration tests
remain passing. All five source snapshot tests pass, including nine freshly
verified synthetic cases and nine standalone level-six receivers/private grades.
The 196-test current Weave suite passes with its source-stability guard.

The source bundle/lock, original adapter vectors, original blind archive and all
1,841 wires, v1 subtree and all earlier observation records remain unchanged.
The initial 16-test and later 20-test records remain historical. This follow-up
uses synthetic data; the actual operator archive was not accessed or migrated,
its original full-corpus harness was not rerun, and no attacker trial occurred.
Current identities are in [RELEASE_REPAIR_20261116.json](RELEASE_REPAIR_20261116.json).
`SHA256SUMS.4fdfb06` retains the preceding checksum list; `SHA256SUMS` covers current
files. Use the documented separate-directory verification before releasing or
grading cases from historical operator archives.

hmmm: snapshotting verified bytes is not an OS sandbox or a signature. Grading
reports exact byte equality for an admitted fixture, not cryptographic security.
Full-Weave construction and security obligations remain incomplete.

GPT generated; context, prompt Erin Spencer.
