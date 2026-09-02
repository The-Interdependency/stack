# AHBG submission blockers — pass 5

Everything source-backed is complete and merged. The following require live
external accounts or hardware and cannot be completed from this repository.

## 1. Construction (core mechanics) — CLOSED

- UCNS construction state merged: `The-Interdependency/ucns` PR #218, module
  `ucns.mobius_seed_construction@0.1.0`, merge commit `828c0b8`.
- AHBG binds `construct` through the same observe/plan/act contract as A0;
  regression coverage proves external harness + A0 both build.
- No remaining core-mechanics blocker.

## 2. Galaxy Store publication — EXTERNAL (now the primary path)

- RevenueCat upgraded to `10.19.1` + `purchases-store-galaxy` (this line);
  signing config, versioning, HTTPS endpoint, network security config, and
  submission assets are all in-repo.
- **Blocker**: Samsung Seller Portal registration and **Commercial Seller
  Status approval** (schedule risk — start first; PayPal is the documented
  easiest payout path; D-U-N-S/international-bank verification can take up to
  10 business days). Then app registration, Samsung IAP item, Galaxy review,
  and publish. See `GALAXY_STORE_RUNBOOK.md`.

## 3. RevenueCat production provisioning — EXTERNAL

- Client + runtime entitlement boundary complete; Galaxy billing backend is
  part of this line.
- **Blocker**: the live RevenueCat project, Galaxy Store app, Seller Portal
  service-account credentials, product, `benchmark_lab` entitlement, offering,
  and public SDK key must be created in the dashboard.
  See `REVENUECAT_PROVISIONING.md`.

## 4. Publish + submission assets — EXTERNAL

- Store listing, privacy policy, demo storyboard, Galaxy runbook, and Devpost
  material are in `ahbg/submission/`.
- **Blocker**: recording the ≤2-minute device demo, capturing screenshots,
  creating promo/trial codes, uploading assets, obtaining the public Galaxy
  Store URL, and submitting that URL to Devpost require the published listing.

## Gate status

- Clean release build: source-ready; APK assembly is CI-verified for debug;
  signed release needs the production keystore.
- Connect conforming harness / A0 same contract / build / persist / reload:
  verified by `ahbg/runtime` tests (12 OK) and the HTTP bridge.
- Purchase/restore Benchmark Lab: code path complete; live verification needs
  the RevenueCat dashboard and a store sandbox purchase.
