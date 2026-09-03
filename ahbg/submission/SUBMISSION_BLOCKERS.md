# AHBG submission blockers — Google Play (primary)

The Android release artifact is source-buildable, but the billing/acquisition,
entitlement-delivery, runtime-enforcement, and production-deployment boundaries
are not complete. The remaining blockers are split below so a green build is
not mistaken for a publishable or sellable app.

## 1. Construction (core mechanics) — CLOSED

- UCNS construction state merged: `The-Interdependency/ucns` PR #218, module
  `ucns.mobius_seed_construction@0.1.0`, merge commit `828c0b8`.
- AHBG binds `construct` through the same observe/plan/act contract as A0;
  regression coverage proves external harness + A0 both build.
- Post-merge hardening is owned by UCNS; AHBG does not invent replacement
  construction geometry.

## 2. Billing + entitlement enforcement — REPOSITORY BLOCKERS

RevenueCat initialization and an asynchronous customer-info lookup exist, but
the Android/WebView/runtime path does not yet form a complete premium gate.

- **Blocker**: fetch the current RevenueCat offering/package.
- **Blocker**: launch purchase of `ahbg_benchmark_lab` from a user-visible
  control and surface success/cancel/error state.
- **Blocker**: expose an explicit restore control using RevenueCat restore.
- **Blocker**: notify/refresh the WebView when asynchronous customer-info refresh
  changes `benchmark_lab`; one synchronous read during page startup is not
  persistence evidence.
- **Blocker**: carry a server-verifiable entitlement claim to the runtime rather
  than trusting a local client Boolean.
- **Blocker**: enforce `benchmark_lab` at the actual premium runtime operations;
  a changed status label is not feature gating.
- Regression-test the acquisition, async-refresh, transport, and deny/allow
  runtime boundaries before calling the billing gate complete.

## 3. Production AHBG runtime — REPOSITORY/DEPLOYMENT BLOCKER

The Android build carries an intended production `RUNTIME_URL`; that build-time
constant is not proof that the service exists or is healthy.

- **Blocker**: deploy the canonical AHBG runtime at the exact configured HTTPS
  URL with valid TLS.
- **Blocker**: verify from a release-equivalent client that `board.html`, session
  creation, plan/state calls, entitlement verification, and a premium deny/allow
  operation work end to end.
- Preserve the Android layer as transport/presentation only; do not repair a
  missing service by embedding a second runtime into the app.

## 4. Google Play publication — EXTERNAL (primary path)

- Code/build compliance is present: `compileSdk`/`targetSdk` 36, AGP 8.9.1,
  Gradle 8.11.1, Play-native `bundleRelease` in CI, RevenueCat 10.19.1 core,
  and signing config outside Git.
- **Blocker**: Play developer account, app registration, first internal/closed
  test release upload, and production promotion.
- **Blocker**: complete Play Console App content requirements: Data safety,
  public privacy-policy URL, ads declaration, app-access declaration, target
  audience/content declarations, content-rating questionnaire, Financial
  features declaration, and Health apps declaration. Where AHBG has no
  financial/health features, submit the corresponding "none" declaration.
- **Blocker**: create and activate the `ahbg_benchmark_lab` non-consumable
  one-time-product purchase option, including price and regional availability.
- **Blocker**: configure the billing-test Google account under Play Console
  License testing before any sandbox purchase; test-track membership alone is
  insufficient.
- **hmmm**: if the developer account is a newly created personal account,
  Google currently requires 12 continuously opted-in testers for at least 14
  days before production access — start the closed test immediately.

## 5. RevenueCat production provisioning — EXTERNAL

- **Blocker**: live RevenueCat project, Google Play app, Google Cloud service
  account (Play Developer + Reporting APIs), Play permission grants,
  service-account JSON upload, product/entitlement/offering mapping, and the
  Google Play app's RevenueCat public SDK key (`goog_...`).
- RevenueCat v2 project IDs use the `proj...` form; project IDs are not valid
  substitutes for the Android Google Play public SDK key.
- **hmmm**: RevenueCat/Google Play service-account permissions can take time to
  propagate after provisioning.
  See `REVENUECAT_PROVISIONING.md`.

## 6. Publish + submission assets — EXTERNAL

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
- Sandbox purchase → async entitlement refresh → verified runtime unlock →
  restore → restart persistence → premium deny/allow: **BLOCKED** until the
  repository work in sections 2–3 is implemented, then requires the Play test
  track, License testing account, active purchase option, and RevenueCat Play
  credentials.

## Smallest repository next action

Add one explicit entitlement-state notification/refresh path from
`RevenueCatPremiumStore` to the WebView and a regression test proving a cold
start can transition from the initial locked state to the eventual RevenueCat
state without restart. This closes one concrete race without pretending that
purchase, restore, server verification, feature gating, or deployment are done.

## hmmm

A buildable AAB is not yet a sellable product. After the async entitlement
refresh is repaired, acquisition, verified runtime gating, and production
runtime acceptance remain living continuation before the external store gate.
