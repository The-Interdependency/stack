# AHBG submission blockers — Google Play (primary)

The Android release artifact and entitlement-check boundary are source-ready.
The remaining blockers are split below between repository work and live external
Play/RevenueCat work so a green build is not mistaken for a publishable app.

## 1. Construction (core mechanics) — CLOSED

- UCNS construction state merged: `The-Interdependency/ucns` PR #218, module
  `ucns.mobius_seed_construction@0.1.0`, merge commit `828c0b8`.
- AHBG binds `construct` through the same observe/plan/act contract as A0;
  regression coverage proves external harness + A0 both build.
- Post-merge hardening is owned by UCNS; AHBG does not invent replacement
  construction geometry.

## 2. Billing controls — REPOSITORY BLOCKER

RevenueCat initialization and entitlement lookup exist, but the Android/WebView
surface does not yet expose a complete acquisition flow.

- **Blocker**: fetch the current RevenueCat offering/package.
- **Blocker**: launch purchase of `ahbg_benchmark_lab` from a user-visible
  control and surface success/cancel/error state.
- **Blocker**: expose an explicit restore control that calls
  `Purchases.sharedInstance.restorePurchases` and refreshes entitlement state.
- Regression-test the bridge/API boundary; do not mark the sandbox billing gate
  complete from `getCustomerInfo` alone.

## 3. Google Play publication — EXTERNAL (primary path)

- Code compliance is done: `compileSdk`/`targetSdk` 36, AGP 8.9.1, Gradle
  8.11.1, Play-native `bundleRelease` in CI, RevenueCat 10.19.1 core, production
  HTTPS endpoint, signing config outside Git.
- **Blocker**: Play developer account, app registration, first internal/closed
  test release upload, and production promotion.
- **Blocker**: complete Play Console App content requirements: Data safety,
  public privacy-policy URL, ads declaration, app-access declaration, target
  audience/content declarations, and content-rating questionnaire.
- **Blocker**: create and activate the `ahbg_benchmark_lab` non-consumable
  one-time-product purchase option, including price and regional availability.
- **Blocker**: configure the billing-test Google account under Play Console
  License testing before any sandbox purchase; test-track membership alone is
  insufficient.
- **hmmm**: if the developer account is a newly created personal account,
  Google currently requires 12 continuously opted-in testers for at least 14
  days before production access — start the closed test immediately.

## 4. RevenueCat production provisioning — EXTERNAL

- Client/runtime entitlement-check boundary complete.
- **Blocker**: live RevenueCat project, Google Play app, Google Cloud service
  account (Play Developer + Reporting APIs), Play permission grants,
  service-account JSON upload, product/entitlement/offering mapping, and the
  Google Play app's RevenueCat public SDK key (`goog_...`).
- `rc_...` project identifiers are not valid substitutes for the Android Google
  Play public SDK key.
- **hmmm**: RevenueCat/Google Play service-account permissions can take time to
  propagate after provisioning.
  See `REVENUECAT_PROVISIONING.md`.

## 5. Publish + submission assets — EXTERNAL

- Store listing, privacy policy, demo storyboard, Play runbook, and Devpost
  material are in `ahbg/submission/`.
- **Blocker**: recording the ≤2-minute device demo, capturing screenshots,
  uploading assets, obtaining the public Play Store URL, and submitting that
  URL to Devpost.

## Galaxy — deferred/optional compatibility

Not an active Shipaton dependency. If re-enabled later, add
`purchases-store-galaxy` (RevenueCat >= 10.7.0) back to the dependency graph
and follow the archived Galaxy notes.

## Gate status

- Signed API-36 AAB: source-ready; CI verifies `bundleRelease` unsigned each
  change; signing needs the production keystore outside Git.
- Connect conforming harness / A0 same contract / build / persist / reload:
  verified by `ahbg/runtime` tests and the HTTP bridge.
- Sandbox purchase → `benchmark_lab` unlock → restore → restart persistence:
  **BLOCKED** until purchase/restore controls are implemented, then requires
  the Play test track, License testing account, active purchase option, and
  RevenueCat Play credentials.

## hmmm

A buildable AAB is not yet a sellable product. The smallest repository-owned
next step is purchase + restore wiring; the rest of the gate then crosses into
live Play/RevenueCat accounts.
