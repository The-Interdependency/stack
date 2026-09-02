# AHBG ≤2-minute device demo — storyboard

Recorded on the release build against the production HTTPS endpoint, no cuts,
one continuous device session.

| # | Time | Shot | Shows the gate item |
|---|---|---|---|
| 1 | 0:00 | Fresh install, app icon, open | clean install |
| 2 | 0:10 | Onboarding overlay → Start | install → onboarding |
| 3 | 0:20 | Start plane; board renders 7 UCNS tiles | start plane |
| 4 | 0:30 | Agent select: A0 (reference) | connect/select agent |
| 5 | 0:40 | Play turn 1 — A0 constructs RING_0; ring appears | observe/plan/act/build |
| 6 | 1:00 | Play turn 2 — construct RING_1; feed shows events | visible consequence |
| 7 | 1:15 | Persist/reload; board restores exactly | persist/reload |
| 8 | 1:30 | External harness connects via same JSON contract (show CLI posting a plan) | conforming harness |
| 9 | 1:45 | Benchmark Lab surface; purchase/restore with test card | purchase/restore |
| 10 | 1:55 | Repeat one full turn after restore | repeat successfully |

## Script voiceover (optional)

"AHBG is one Seed-of-Life plane and one contract. Any conforming harness can
observe, plan, and act — A0 is just the reference client on the same contract.
Every turn resolves simultaneously and persists. Benchmark Lab unlocks the
advanced packs; basic play stays free."

## Capture notes

- Device: emulator or physical device, 1080p, no on-screen debug overlays.
- Use a RevenueCat sandbox/test purchase for the purchase/restore shot.
- Export to `ahbg/submission/assets/demo.mp4` (asset file not committed here;
  add it before store submission).
