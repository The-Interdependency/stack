# AHBG submission blockers — Google Play (primary)

Everything source-backed is complete and merged. The following require live
external accounts or hardware and cannot be completed from this repository.

## 1. Construction (core mechanics) — CLOSED

- UCNS construction state merged: `The-Interdependency/ucns` PR #218, module
  `ucns.mobius_seed_construction@0.1.0`, merge commit `828c0b8`.
- AHBG binds `construct` through the same observe/plan/act contract as A0;
  regression coverage proves external harness + A0 both build.
- No remaining core-mechanics blocker.

## 2. Google Play publication — EXTERNAL (primary path)

- Code compliance is done: `compileSdk`/`targetSdk` 36, AGP 8.9.1, Gradle
  8.11.1, Play-native `bundleRelease` in CI, RevenueCat 10.19.1 core (Play
  default), production HTTPS endpoint, signing config outside Git.
- **Blocker**: a Play developer account, app registration, listing review,
  first internal/closed test release upload, and production promotion.
- **hmmm**: if the developer account is a newly created personal account,
  Google currently requires 12 continuously opted-in testers for at least 14
  days before production access — start the closed test immediately.

## 3. RevenueCat production provisioning — EXTERNAL

- Client + runtime entitlement boundary complete.
- **Blocker**: live RevenueCat project, Google Play app, Google Cloud service
  account (Play Developer + Reporting APIs), Play permission grants,
  service-account JSON upload (up to 36h activation), product/entitlement/
  offering mapping, and public SDK key.
  See `REVENUECAT_PROVISIONING.md`.

## 4. Publish + submission assets — EXTERNAL

- Store listing, privacy policy, demo storyboard, Play runbook, and Devpost
  material are in `ahbg/submission/`.
- **Blocker**: recording the ≤2-minute device demo, capturing screenshots,
  creating promo/trial codes, uploading assets, obtaining the public Play
  Store URL, and submitting that URL to Devpost.

## Galaxy — deferred/optional compatibility

Not an active Shipaton dependency. If re-enabled later, add
`purchases-store-galaxy` (RevenueCat >= 10.7.0) back to the dependency graph
and follow the archived Galaxy notes.

## Gate status

- Signed API-36 AAB: source-ready; CI verifies `bundleRelease` unsigned each
  change; signing needs the production keystore (outside Git).
- Connect conforming harness / A0 same contract / build / persist / reload:
  verified by `ahbg/runtime` tests (12 OK) and the HTTP bridge.
- Sandbox purchase → `benchmark_lab` unlock → restore → restart persistence:
  code path complete; live verification needs the Play test track and the
  RevenueCat Play service credentials.
