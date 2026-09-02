# AHBG submission blockers — Google Play (primary)

Source-backed Android purchase/restore wiring, Play artifact generation, and
submission documentation are complete in the repository. The remaining items
below require live external accounts, Play state, credentials, or hardware and
must not be reported as repository-complete evidence.

## 1. Construction (core mechanics) — CLOSED

- UCNS construction state merged: `The-Interdependency/ucns` PR #218, module
  `ucns.mobius_seed_construction@0.1.0`, merge commit `828c0b8`.
- AHBG binds `construct` through the same observe/plan/act contract as A0;
  regression coverage proves external harness + A0 both build.
- No remaining core-mechanics blocker.

## 2. Google Play publication — EXTERNAL (primary path)

- Code compliance is done: `compileSdk`/`targetSdk` 36, AGP 8.9.1, Gradle
  8.11.1, Play-native `bundleRelease` in CI, RevenueCat 10.19.1 core, production
  HTTPS endpoint, signing config outside Git, explicit purchase + restore UI.
- **Blocker**: Play developer account, app registration, listing, signed test
  release upload, review, and production promotion.
- **Blocker**: complete every required Play **App content** declaration,
  including Data safety, privacy-policy URL, Ads, App access, Target audience
  and content, Content rating, plus any additional requirement shown by the
  live console.
- **hmmm**: developer-account production-access testing requirements are live
  account state; start any required closed test immediately and record the
  console's exact current requirement rather than assuming publication access.

## 3. One-time product + sandbox — EXTERNAL

- Repository product contract: `ahbg_benchmark_lab` → `benchmark_lab`.
- **Blocker**: create/publish the Play one-time product and an **active
  non-consumable purchase option** with region availability and price.
- **Blocker**: add the purchasing Google account under Play Console **License
  testing** as well as the chosen test track. Track membership alone does not
  make purchases sandbox transactions.
- **Gate**: before buying, confirm the Play purchase sheet is a test transaction;
  stop if an ordinary payment method would create a real charge.

## 4. RevenueCat production provisioning — EXTERNAL

- Client purchase/restore + runtime entitlement boundary complete.
- **Blocker**: live RevenueCat project, Google Play app, Google Cloud service
  account (Play Developer + Reporting APIs), Play permission grants,
  service-account JSON upload/activation, product→entitlement→current-offering
  mapping, and the app-specific `goog_...` public SDK key.
  See `REVENUECAT_PROVISIONING.md`.

## 5. Publish + submission assets — EXTERNAL

- Store listing, privacy policy, demo storyboard, Play runbook, and Devpost
  material are in `ahbg/submission/`.
- **Blocker**: record the ≤2-minute device demo, capture screenshots, upload
  assets, obtain the public Play Store URL, and submit that URL to Devpost.

## Gate status

- Signed API-36 AAB: source-ready; CI verifies `bundleRelease` unsigned each
  change; signing needs the production keystore (outside Git).
- Connect conforming harness / A0 same contract / build / persist / reload:
  verified by `ahbg/runtime` tests and the HTTP bridge.
- In-app purchase + restore controls: source-complete; Android build must compile
  them and live verification needs Play + RevenueCat provisioning above.
- Sandbox purchase → `benchmark_lab` unlock → restore → restart persistence:
  **EXTERNAL/UNVERIFIED** until exercised from the Play-installed test build.

## hmmm

Green source CI is permission to enter the store test, not evidence that Google
has sold, restored, reviewed, or published anything.
