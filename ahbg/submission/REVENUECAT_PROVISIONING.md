# RevenueCat production provisioning

The client integration is complete (`Entitlements.kt` + runtime
`entitlements.py`). Live provisioning needs the RevenueCat dashboard and the
store consoles; the following steps are the exact remaining external work.

## Dashboard

1. Create the production project in RevenueCat.
   - Record the **project id** here once created: `rc_<TO_FILL>`.
2. Add the Android app (`org.interdependency.ahbg`). For the Galaxy-first
   path add a **Galaxy Store** app; add the Play app later if shipping Play.
   - Galaxy: create a Galaxy Seller Portal **service account** and give those
     credentials to RevenueCat so it can validate Samsung purchases.
   - Play (later): attach the Play public key.
3. Create the entitlement `benchmark_lab` (non-consumable).
4. Create the product `ahbg_benchmark_lab` (one-time purchase, "Benchmark
   Lab"), attach it to the entitlement, and mirror it as a Samsung IAP item
   with the same id in Seller Portal.
5. Create an offering (default) containing that product; optionally add a
   trial offering `ahbg_benchmark_lab_trial` if a trial is desired.
6. Copy the **public SDK API key** (`appl_...` or `goog_...` public key) into
   the build:
   ```bash
   gradle assembleRelease \
     -PruntimeUrl=https://ahbg.interdependentway.org \
     -PrevenueCatApiKey=rc_public_key \
     -PahbgStoreFile=/secure/ahbg-release.jks \
     -PahbgStorePassword=... -PahbgKeyAlias=... -PahbgKeyPassword=...
   ```
7. SDK: RevenueCat `10.19.1` + `purchases-store-galaxy` (this PR); Galaxy
   IAP requires RevenueCat >= 10.7.0 and the store module.

## Verify (gate items)

- **Free tier**: no key / no purchase → `NoopPremiumStore` or inactive
  entitlement; Benchmark Lab locked; basic play and harness connectivity work.
- **Purchase**: sandbox purchase activates `benchmark_lab` → premium surface
  unlocks in-app.
- **Trial** (if configured): trial start/expiry maps to the same entitlement.
- **Restore**: `Purchases.sharedInstance.restorePurchases` re-activates the
  entitlement on the same store account. (Add the restore button wiring to
  `MainActivity` before release if the store review flow requires an explicit
  restore control — currently restore uses the store-standard flow.)
- **Persistence**: entitlement state is re-fetched on launch; free tier
  persists until purchase.
- **Degraded/offline**: RevenueCat errors and no-network states default to
  the free tier (`isBenchmarkLabUnlocked() == false`); the app remains usable.

## hmmm

- Actual project id, product ids, and public SDK key cannot be provisioned
  from this repository; they must be created in the live RevenueCat dashboard.
- Store sandbox purchases require the Play Console app to be uploaded first.
