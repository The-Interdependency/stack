# AHBG submission package

Shipping material for the Google Play (primary) path. The source-side,
buildable parts live in the repo; everything that requires a live external
account is listed in [`SUBMISSION_BLOCKERS.md`](SUBMISSION_BLOCKERS.md).

| Asset | File |
|---|---|
| **Google Play publication runbook** | `GOOGLE_PLAY_RUNBOOK.md` |
| Store listing copy | `STORE_LISTING.md` |
| Privacy declaration | `PRIVACY_POLICY.md` |
| ≤2-minute device demo | `DEMO_STORYBOARD.md` |
| Devpost material | `DEVPOST.md` |
| RevenueCat production provisioning | `REVENUECAT_PROVISIONING.md` |
| Remaining external blockers | `SUBMISSION_BLOCKERS.md` |

## Shipping path

**Google Play first.** AHBG targets Android 16 / API 36 (AGP 8.9.1, Gradle
8.11.1), ships a signed AAB, and uses RevenueCat `10.19.1` core (Play billing
by default). Galaxy Store is deferred/optional compatibility.

## Current release identity

- App id: `org.interdependency.ahbg`
- versionCode `3`, versionName `0.3.0`
- compileSdk / targetSdk `36`
- Production runtime endpoint: `https://ahbg.interdependentway.org`
- Entitlement: `benchmark_lab` (RevenueCat `10.19.1`, Play backend)
- Construction authority: `ucns.mobius-seed-construction@0.1.0`
  (The-Interdependency/ucns, merged `828c0b8`)
