# AHBG calibration evidence

Extracted from the closed calibration PRs #18 (Codex) and #19 (DeepCode) on
2026-09-01. The provider workspace trees (`stack/ahbg/codex`,
`stack/ahbg/deepseek`) remain branch-resident experiment receipts; only the
comparison results, corpus receipts, and reproducible calibration evidence are
carried here.

Machine-readable record: [`CALIBRATION_EVIDENCE.json`](CALIBRATION_EVIDENCE.json).

## Frozen builds

| Builder | Branch | Frozen build SHA |
|---|---|---|
| Grok | `agent/ahbg-grok` | `cce9cec7dae61304118efcd47bc0d7461200d335` |
| Codex | `agent/ahbg-codex` | `ffb64c274583d8539f8f4fe7e0aa77366689e910` |
| DeepCode | `agent/ahbg-deepcode` | `ec07f465184e7a37af856bc5b301bd8eaa4f097b` |

Branch heads at extraction: Codex `af67642`, DeepCode `34648ed`, Grok `03e77a3`.

## Successor corpus receipt

- Corpus `calibration-family`, proposal `1.0.1-proposal-1`, 35 scenarios.
- Canonical scenarios digest:
  `371d2361f57b56d73544f58b247704617d550a7a0685a133c4f8b1ff3b36c835`.
- Corpus JSON file digest at the successor runs:
  `ea172cb68a1a31be843f45c9886590f95f60daad4f10b9e42732bfd416ef73ab`.
- Canonical main re-serialized the corpus file; current
  `ahbg/deepseek/corpus-proposal/corpus.json` file digest is
  `bc521113ffa7bd6d5094c71f3ad66547d5f00260f380258e43c2086533a5d7ed`
  with the same scenario digest.
- Predecessor `1.0.0-proposal-1`, digest
  `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`,
  merged to main as `3a92c7b0` via PR #5.

## Successor runs

All three builders: **35 SURVIVED / 0 FALSIFIED / 0 UNRESOLVED / 0 BLOCKED**.

Codex freeze verification: `a0` tests 7 OK, `ahbg` tests 12 OK, Python
compile 15 files OK, artifact check SURVIVED, calibration smoke summary
4 survived / 0 falsified / 2 unresolved / 0 blocked.

## Six directional checks — all SURVIVED

| Checker | Subject | Subject frozen build | Checker artifact |
|---|---|---|---|
| Grok | Codex | `ffb64c2` | `ahbg/grok/reviews/codex-review.json` |
| Grok | DeepCode | `ec07f46` | `ahbg/grok/reviews/deepcode-review.json` |
| Codex | Grok | `cce9cec` | `ahbg/codex/reviews/grok-review.json` |
| Codex | DeepCode | `ec07f46` | `ahbg/codex/reviews/deepcode-review.json` |
| DeepCode | Grok | `cce9cec` | `ahbg/deepseek/reviews/grok-review.json` |
| DeepCode | Codex | `ffb64c2` | `ahbg/deepseek/reviews/codex-review.json` |

No builder was falsified. Agreement across independent builds is replication
evidence, not proof.

## Evidence caveats (preserved, not erased)

- Codex recorded that its conversation inspected sibling DeepCode/DeepSeek
  files before the workspace correction; the frozen implementation lives under
  `stack/ahbg/codex` and does not import sibling code.
- DeepCode's frozen build was reviewed by Grok and Codex; later commits on the
  branch are metadata, extension evidence, and reciprocal-review records that
  do not alter the frozen implementation.

## hmmm

- World-digest mismatches remain 35 of 35 in the burden-coupling comparison
  (expected while standing is binding).
- Formal successor sealing is recorded as adopted on main, not as a three-way
  branch merge.
- Provider workspace trees on the closed branches are receipts only and are
  intentionally not merged into main.
