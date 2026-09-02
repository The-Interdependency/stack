# RevenueCat production provisioning — Google Play

The client integration is complete (`Entitlements.kt` + runtime
`entitlements.py`). Live provisioning needs the RevenueCat dashboard, Play
Console, and Google Cloud; the following steps are the exact remaining
external work.

## Dashboard + Play connection

1. Create the production project in RevenueCat.
   - Record the **project id** here once created: `rc_<TO_FILL>`.
2. Add a **Google Play** app (`org.interdependency.ahbg`).
3. Google Cloud Console:
   - Create a **service account** for RevenueCat.
   - Enable **Google Play Developer API** and **Google Play Reporting API**.
4. Play Console → Users and permissions:
   - Invite the service account email.
   - Grant the permissions RevenueCat's current checklist requires (financial
     data, view app information, manage orders, etc.).
5. Generate a JSON key for the service account and upload it to RevenueCat.
   - **hmmm**: RevenueCat notes Play service credentials can take up to 36
     hours to activate.
6. Create the entitlement `benchmark_lab` (non-consumable).
7. Create the product `ahbg_benchmark_lab` (one-time purchase, "Benchmark
   Lab") — first create the matching Play in-app product after uploading a
   test build — then attach it to the entitlement in a default offering.
   Optionally add `ahbg_benchmark_lab_trial` if a trial is desired.
8. Copy the RevenueCat **public SDK API key** into the build:

   ```bash
   gradle bundleRelease \
     -PruntimeUrl=https://ahbg.interdependentway.org \
     -PrevenueCatApiKey=<rc_public_sdk_key> \
     -PahbgStoreFile=/secure/ahbg-release.jks -PahbgStorePassword=... \
     -PahbgKeyAlias=... -PahbgKeyPassword=...
   ```

9. SDK: RevenueCat `10.19.1` core supports Google Play by default through the
   ordinary `PurchasesConfiguration`; no store module is required.

## Verify (gate items)

- **Free tier**: no key / no purchase → `NoopPremiumStore` or inactive
  entitlement; Benchmark Lab locked; basic play and harness connectivity work.
- **Purchase**: Play sandbox purchase activates `benchmark_lab` → premium
  surface unlocks in-app.
- **Trial** (if configured): trial start/expiry maps to the same entitlement.
- **Restore**: `Purchases.sharedInstance.restorePurchases` re-activates the
  entitlement on the same account. (Add the restore button wiring to
  `MainActivity` before release if review requires an explicit restore
  control — currently restore uses the store-standard flow.)
- **Persistence**: entitlement state is re-fetched on launch; after a restart
  the unlocked state must remain correct.
- **Degraded/offline**: RevenueCat errors and no-network states default to the
  free tier (`isBenchmarkLabUnlocked() == false`); the app remains usable.

## hmmm

- Actual project id, product ids, service-account JSON, and public SDK key
  cannot be provisioned from this repository.
- Play sandbox purchases require the app uploaded to a Play test track first.
