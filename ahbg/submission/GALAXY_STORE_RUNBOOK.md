# Samsung Galaxy Store publication runbook

Shipaton accepts a fully published Galaxy Store URL. This runbook follows the
Galaxy-first order: Seller Portal approval first, code/RevenueCat in parallel,
then register, IAP, closed-beta purchase verification, review, publish.

## 0. Code (done in this PR)

- RevenueCat upgraded `8.10.1 → 10.19.1` with the `purchases-store-galaxy`
  billing backend (native Galaxy IAP requires RevenueCat >= 10.7.0 + that
  module). Store is auto-detected at runtime.
- Package stays `org.interdependency.ahbg`; target API 35 (Galaxy does not
  currently impose Play's API-36 rule).

## 1. Samsung Seller Portal (start immediately — longest lead time)

1. Register a Samsung account at the Seller Portal.
2. Request **Commercial Seller Status** (required even for free distribution).
   - Provide identity/business documentation and financial information.
   - PayPal is the supported/easiest payout path.
   - D-U-N-S or international-bank verification can take up to 10 business
     days; Samsung also documents applying without D-U-N-S using business
     documentation.
3. Record approval here when granted: `SELLER_PORTAL_APPROVED=<date>`.

## 2. Register AHBG

1. Seller Portal → Add Application.
2. Package name: `org.interdependency.ahbg`.
3. Upload the signed release binary (APK or AAB) built with:
   ```bash
   gradle assembleRelease \
     -PruntimeUrl=https://ahbg.interdependentway.org \
     -PrevenueCatApiKey=<rc_public_key> \
     -PahbgStoreFile=/secure/ahbg-release.jks -PahbgStorePassword=... \
     -PahbgKeyAlias=... -PahbgKeyPassword=...
   ```
4. Fill listing with `STORE_LISTING.md`, privacy policy `PRIVACY_POLICY.md`,
   icon, and screenshots (see `DEMO_STORYBOARD.md`).

## 3. Samsung IAP

1. Seller Portal → In-App Purchase → create item `ahbg_benchmark_lab`
   (one-time, non-consumable), matching the RevenueCat product id.
2. Keep the free core playable without IAP; `benchmark_lab` gates only
   Benchmark Lab.

## 4. Connect Galaxy to RevenueCat

1. RevenueCat dashboard → add a **Galaxy Store** app with package
   `org.interdependency.ahbg`.
2. Create a Galaxy Seller Portal **service account**; give those credentials
   to RevenueCat so it can validate Samsung purchases.
3. Create the `benchmark_lab` entitlement and the `ahbg_benchmark_lab`
   product/offering (see `REVENUECAT_PROVISIONING.md`).

## 5. Closed beta + purchase verification

1. Samsung **Closed Beta** supports in-app purchases and has no fixed
   14-day/12-person production gate.
2. Verify the full path on-device:
   install → observe/plan/act/build → persist/reload →
   purchase `benchmark_lab` → entitlement unlocks → restore → repeat.

## 6. Review → publish → Devpost

1. Submit for Galaxy review.
2. Once live, use the public Galaxy Store listing URL as the Devpost entry
   URL (a beta link does not count; the app must be publicly downloadable in
   the US).
3. Galaxy optimization notes (Best App for Galaxy category, 20% of score):
   foldable/multi-window support and Samsung-specific features are the
   highest-value follow-ups; exclusivity is a bonus, not required.

## hmmm

- Commercial Seller Status approval time is the schedule risk; it is external
  and started first for that reason.
- The live Galaxy listing URL, Seller Portal service-account credentials, and
  RevenueCat Galaxy app id cannot be produced from this repository.
