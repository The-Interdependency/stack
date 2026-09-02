# RevenueCat production provisioning — Google Play

The entitlement-check integration exists (`Entitlements.kt` + runtime
`entitlements.py`). Live provisioning needs the RevenueCat dashboard, Play
Console, and Google Cloud. Purchase initiation and explicit restore controls
remain repository work and are called out separately below.

## Dashboard + Play connection

1. Create the production project in RevenueCat.
   - Record the **project id** here once created: `rc_<TO_FILL>`.
   - This project id is not an Android SDK API key.
2. Add a **Google Play** app (`org.interdependency.ahbg`).
3. Google Cloud Console:
   - Create a **service account** for RevenueCat.
   - Enable **Google Play Developer API** and **Google Play Reporting API**.
4. Play Console → Users and permissions:
   - Invite the service account email.
   - Grant the permissions RevenueCat's current checklist requires.
5. Generate a JSON key for the service account and upload it to RevenueCat.
   - **hmmm**: service-account permissions/credentials may take time to
     propagate after provisioning.
6. Create the entitlement `benchmark_lab`.
7. In Play Console, after uploading a test build, create
   `ahbg_benchmark_lab` as a one-time product and create/activate its
   **non-consumable purchase option**, including pricing and regional
   availability.
8. Import/map that Play product in RevenueCat, attach it to `benchmark_lab`,
   and expose it through the default offering.
9. Copy the Google Play app's RevenueCat **public SDK API key** (`goog_...`)
   into the build:

   ```bash
   gradle bundleRelease \
     -PruntimeUrl=https://ahbg.interdependentway.org \
     -PrevenueCatApiKey=<goog_public_sdk_key> \
     -PahbgStoreFile=/secure/ahbg-release.jks -PahbgStorePassword=... \
     -PahbgKeyAlias=... -PahbgKeyPassword=...
   ```

10. RevenueCat `10.19.1` core supports Google Play through the ordinary
    `PurchasesConfiguration`; no Galaxy store module is required.

## Repository billing controls — not complete

Before the live Play billing gate can run, AHBG must expose user-visible
operations that:

1. fetch the current RevenueCat offering/package for `ahbg_benchmark_lab`;
2. initiate the purchase and handle success/cancel/error outcomes; and
3. invoke `Purchases.sharedInstance.restorePurchases`, then refresh the
   entitlement state.

`getCustomerInfo` / `isBenchmarkLabUnlocked()` alone can observe an existing
entitlement but cannot acquire or explicitly restore one.

## Verify (gate items)

Before any billing transaction, configure the purchasing Google account under
Play Console **License testing** and use that same account to accept/install the
test-track build. Test-track membership alone is not a sandbox guarantee.

After the repository billing controls above exist:

- **Free tier**: no purchase → inactive entitlement; Benchmark Lab locked;
  basic play and harness connectivity work.
- **Purchase**: the license-test transaction activates `benchmark_lab` and the
  premium surface unlocks.
- **Restore**: the explicit restore control calls RevenueCat restore and
  re-activates the entitlement for the same store account.
- **Persistence**: entitlement state is re-fetched on launch; after restart the
  unlocked state remains correct.
- **Degraded/offline**: RevenueCat errors/no-network default to the free tier;
  basic AHBG remains usable.

## hmmm

- Actual project id, product configuration, service-account JSON, and `goog_...`
  SDK key require live accounts and cannot be provisioned from this repository.
- The Play sandbox billing verification remains blocked until purchase/restore
  controls are implemented in the Android surface.
