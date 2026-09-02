# AHBG submission blockers — pass 5

Everything source-backed is complete and merged. The following require live
external accounts or hardware and cannot be completed from this repository.

## 1. Construction (core mechanics) — CLOSED

- UCNS construction state merged: `The-Interdependency/ucns` PR #218, module
  `ucns.mobius_seed_construction@0.1.0`, merge commit `828c0b8`.
- AHBG binds `construct` through the same observe/plan/act contract as A0;
  regression coverage proves external harness + A0 both build.
- No remaining core-mechanics blocker.

## 2. Android release signing and store upload — EXTERNAL

- Signing config and versioning are in `ahbg/android/app/build.gradle.kts`
  (keystore supplied via gradle properties; never committed).
- Production HTTPS endpoint and network security config are in place.
- **Blocker**: a Play Console account, a release keystore, the store listing
  review, and the actual upload/publish step happen outside this repository.

## 3. RevenueCat production provisioning — EXTERNAL

- Client + runtime entitlement boundary complete.
- **Blocker**: the live RevenueCat project, product, `benchmark_lab`
  entitlement, offering, and public SDK key must be created in the dashboard.
  See `REVENUECAT_PROVISIONING.md`.

## 4. Publish + submission assets — EXTERNAL

- Store listing, privacy policy, demo storyboard, and Devpost material are in
  `ahbg/submission/`.
- **Blocker**: recording the ≤2-minute device demo, capturing screenshots,
  creating promo/trial codes, uploading assets, and obtaining the public store
  URL require the published store listing.

## Gate status

- Clean release build: source-ready; APK assembly is CI-verified for debug;
  signed release needs the production keystore.
- Connect conforming harness / A0 same contract / build / persist / reload:
  verified by `ahbg/runtime` tests (12 OK) and the HTTP bridge.
- Purchase/restore Benchmark Lab: code path complete; live verification needs
  the RevenueCat dashboard and a store sandbox purchase.
