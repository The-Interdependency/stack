# Unicode work-graph encoding repair

Review comment 4582094166 identifies an encoding mismatch at
`5602d7b6adf781d9246bc6878f914b3473762264`. The generator accepts the protocol's
UTF-8 canonical work-graph identity, while the auditor and checker escape Unicode
before hashing. A new regression fails all six positive subcases at that head.
The generator also incorrectly applies protocol encoding to the separate root
manifest identity, a discrepancy hidden while that manifest contains only ASCII.

Digital-metrics graph hashes and boundary projections now use sorted compact JSON
with `ensure_ascii=False`, matching the protocol. The root Stack manifest retains
its existing sorted compact `ensure_ascii=True` contract. The auditor selects the
graph encoding explicitly without importing inspected code; the generator uses
the root encoding explicitly when validating the root manifest.

The regression covers Unicode in both a participant relation and a boundary note,
using Möbius text, Greek plus a combining sequence, and an emoji. The generator,
actual pinned-parser loader and structural checker admit every consistent fixture.
Both generator and auditor reject a root-manifest digest incorrectly calculated
with protocol encoding. Git identity is tested separately; this encoding witness
varies only the serialized projections.

All 37 reviewed tests pass with zero skips. Static linkage has 30 contracts and 37
checks with zero behavioral proof credit. Consistency (seven repositories, 72
research participant identities), portfolio and four changed-source ratio gates
pass. Producer pins, WORK_GRAPH.json and both root manifests remain unchanged.

The repaired generator has a new execution identity, so a new pending receipt is
generated and freshly replayed/attested at
`receipts/native-mobius-v0-canonical-20261116.json`, then replayed byte for byte.
Its payload is `1f1eb74b2b19f2944f29fb1d214f84a77fca324717d568e30c1b5096d38d8336`.
The README and CI use this receipt; all three previous receipts remain unchanged.
Earlier test-count and payload records remain historical observations.

hmmm: these are encoding, provenance and structural-replay results, with no EDCM
measurement, producer signature, arbitrary-Python attestation or authority transfer.

GPT generated; context, prompt Erin Spencer.
