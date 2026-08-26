# DeepCode AHBG calibration status

Builder: DeepCode — workspace `stack/ahbg/deepseek/`, branch `agent/ahbg-deepcode`.
Frozen build SHA: `ec07f465184e7a37af856bc5b301bd8eaa4f097b`.

## Sealed corpus

- Corpus: `calibration-family`, version `1.0.0-proposal-1`.
- Canonical scenarios digest: `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`.
- Recorded by all three builders in their `BUILD_MANIFEST.json` under `sealed_corpus_identity`.
- Merged to `main` as commit `3a92c7b0f8568e6fc2600b45bca760030ea2ba3f` via PR #5.
- Reproduction status across builders is partial (Grok: smoke_epoch four scenarios; Codex: codex_smoke_epoch six scenarios; DeepCode: full 35 scenarios). Differences are recorded as `hmmm`, not corpus edits, per the adoption procedure.

## Frozen build SHAs

| Builder | Branch | Frozen build |
|---|---|---|
| Grok | `agent/ahbg-grok` | `cce9cec7dae61304118efcd47bc0d7461200d335` |
| Codex | `agent/ahbg-codex` | `ffb64c274583d8539f8f4fe7e0aa77366689e910` |
| DeepCode | `agent/ahbg-deepcode` | `ec07f465184e7a37af856bc5b301bd8eaa4f097b` |

## Six directional checks

| Direction | Standing | Checker artifact |
|---|---|---|
| Grok → Codex | SURVIVED | `ahbg/grok/reviews/codex-review.json` (subject `ffb64c2`) |
| Grok → DeepCode | SURVIVED | `ahbg/grok/reviews/deepcode-review.json` (subject `ec07f46`) |
| Codex → Grok | PENDING | not yet written on `agent/ahbg-codex` |
| Codex → DeepCode | PENDING | not yet written on `agent/ahbg-codex` |
| DeepCode → Grok | SURVIVED | `ahbg/deepseek/reviews/grok-review.json` (subject `cce9cec`) |
| DeepCode → Codex | SURVIVED | `ahbg/deepseek/reviews/codex-review.json` (subject `ffb64c2`) |

## Divergence register (visible, not averaged)

1. **Hard veto during the shadow epoch.** Grok and Codex gate the permission-field
   hard veto during shadow-epoch runs; DeepCode records the veto in the
   regulatory shadow layer without gating first-epoch decisions. `hmmm`.
2. **Admitted observation fields.** Codex admits `turn/tiles/units/context`;
   DeepCode admits `turn/tiles/units`; Grok has no explicit admitted-field set.
   `hmmm`.
3. **Scenario id set.** Codex: `hard_veto_removes_move`, `prompt_injection_refusal`,
   `unknown_context_distinct`. DeepCode: `hard_veto_illegal_action`,
   `prompt_injection`, `adversarial_info`, `known_neutral`, `unknown_same_posterior`,
   plus the common smoke subset. `hmmm`.
4. **Fail-closed turn closure.** Grok leaves collision turns without a `turn.end`
   event; DeepCode and Codex emit `turn.end` with the unchanged digest. `hmmm`.
5. **Genesis prev hash.** Grok uses `0*64`; DeepCode uses the empty string;
   Codex genesis convention is its own. All verify internally. `hmmm`.
6. **Corpus reproduction.** Grok and Codex record partial reproduction of the
   35-scenario sealed corpus; DeepCode reproduces all 35. `hmmm`.

## Remaining to close the program

- Codex writes its two read-only reviews (Codex → Grok, Codex → DeepCode).
- The final cross-build comparison publishes which regulatory components
  SURVIVED / FALSIFIED / UNRESOLVED / BLOCKED, with the divergence register
  above kept visible.
