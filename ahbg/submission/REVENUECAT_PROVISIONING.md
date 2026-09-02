# RevenueCat production provisioning — Google Play

The client integration is complete (`Entitlements.kt` + runtime
`entitlements.py`). Live provisioning needs the RevenueCat dashboard, Play
Console, and Google Cloud; the following steps are the exact remaining
external work.

## Dashboard + Play connection

1. Create the production project in RevenueCat.
   - Record the **RevenueCat project id** here once created: `rc_<TO_FILL>`.
   - This `rc_...` identifier is project metadata, **not** the Android SDK key.
2. Add a **Google Play** app (`org.interdependency.ahbg`).
3. Google Cloud Console:
   - Create a **service account** for RevenueCat.
   - Enable **Google Play Developer API** and **Google Play Reporting API**.
4. Play Console → Users and permissions:
   - Invite the service account email.
   - Grant the permissions RevenueCat's current checklist requires.
5. Generate a JSON key for the service account and upload it to RevenueCat.
   - **hmmm**: credential activation is external propagation; wait for the
     dashboard connection to report healthy before diagnosing the app.
6. Create the entitlement `benchmark_lab`.
7. After the Play one-time product and active non-consumable purchase option
   exist, import/map `ahbg_benchmark_lab` to `benchmark_lab`.
8. Put that product in a package in the **current/default offering**. The app
   deliberately fetches the current offering and selects the package whose
   product id is exactly `ahbg_benchmark_lab`; a product outside that offering
   fails closed instead of starting the wrong purchase.
9. Copy the app-specific RevenueCat **Google Play public SDK key** (`goog_...`)
   into the build:

   ```bash
   gradle bundleRelease \
     -PruntimeUrl=https://ahbg.interdependentway.org \
     -PrevenueCatApiKey=goog_public_sdk_key \
     -PahbgStoreFile=/secure/ahbg-release.jks -PahbgStorePassword=... \
     -PahbgKeyAlias=... -PahbgKeyPassword=...
   ```

10. SDK: RevenueCat `10.19.1` core supports Google Play by default through the
    ordinary `PurchasesConfiguration`; no store module is required.

## Verify (gate items)

Before the purchase gate, use the same Google account for the Play test track
and **License testing**. Confirm Play identifies the transaction as a test
purchase before accepting it.

- **Free tier**: no key / no purchase → `NoopPremiumStore` or inactive
  entitlement; Benchmark Lab locked; basic play and harness connectivity work.
- **Invalid key**: non-`goog_` key → free tier with a visible configuration
  message; the app does not call `Purchases.configure` with a project id.
- **Purchase**: tap **Unlock Benchmark Lab**; the app fetches the current
  offering, purchases `ahbg_benchmark_lab`, and requires active
  `benchmark_lab` before reporting unlock.
- **Restore**: tap **Restore purchase**; the app calls
  `Purchases.sharedInstance.restorePurchases` and refreshes the entitlement.
- **Persistence**: entitlement state is fetched on launch; after a restart the
  unlocked state must remain correct.
- **Degraded/offline**: RevenueCat errors default to the free tier; the app
  remains usable.

## hmmm

- Actual project id, service-account JSON, Google Play public SDK key, product
  availability, current offering, and license-tester state cannot be
  provisioned or proven from this repository.
- The live sandbox purchase/restore test is the terminal evidence for billing;
  source compilation alone is not that test.
