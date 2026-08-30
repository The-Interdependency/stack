# Grok -> Codex

Standing: **SURVIVED** (not proved).

- Checker freeze SHA: `cce9cec7dae61304118efcd47bc0d7461200d335`
- Target freeze SHA: `ffb64c274583d8539f8f4fe7e0aa77366689e910`
- Date: 2026-08-26

Read-only tests at the Codex freeze SHA: a0 7 OK, ahbg 12 OK.

Hard veto removes move (begin/end, no move event) at the Codex freeze SHA. War occupied/dual-target were UNRESOLVED fail-closed in the Codex freeze artifacts.

war_v3 (current Grok runs): occupied_target_collision and dual_target_collision have standing_override=null in the corpus; their evidence_standing is determined by the run. Both resolve deterministically (defender-holds for occupied targets, priority for dual targets), emit explicit war events, and report SURVIVED with replay_equal. Full 35-scenario common-corpus successor run (1.0.1-proposal-1, 371d2361…): 35 SURVIVED / 0 FALSIFIED / 0 UNRESOLVED.

Grok adopts the shared corpus digest with no amendments.

This report does not modify Codex source. (Review performed read-only against the frozen Codex SHA.)
