# RevenueCat production provisioning — Google Play

The entitlement-check integration exists (`Entitlements.kt` + runtime
`entitlements.py`). Live provisioning needs the RevenueCat dashboard, Play
Console, and Google Cloud. Purchase initiation, explicit restore controls,
asynchronous WebView refresh, and verified runtime entitlement enforcement
remain repository work and are called out separately below.

## Dashboard + Play connection

1. Create the production project in RevenueCat.
   - Record the **project id** exactly as RevenueCat shows it; v2 project IDs
     use the `proj...` form.
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

## Repository acquisition controls — not complete

Before the live Play billing gate can run, AHBG must expose user-visible
operations that:

1. fetch the current RevenueCat offering/package for `ahbg_benchmark_lab`;
2. initiate the purchase and handle success/cancel/error outcomes; and
3. invoke RevenueCat restore, then refresh the entitlement state.

`getCustomerInfo` / `isBenchmarkLabUnlocked()` alone can observe an existing
entitlement but cannot acquire or explicitly restore one.

## Repository entitlement delivery — not complete

The current store initializes `benchmarkLabUnlocked` to false and refreshes it
asynchronously. The WebView bridge exposes only a synchronous Boolean read.
Therefore a cold start can read `false` before RevenueCat answers and never
learn that the entitlement became active.

Before persistence is called complete:

1. publish an explicit entitlement-state update from the RevenueCat callback to
   the WebView (or provide an equivalent deterministic refresh path);
2. update the premium UI when that state changes without requiring a restart;
3. carry a server-verifiable entitlement claim across the Android/runtime
   boundary; and
4. enforce `benchmark_lab` at the actual premium runtime operations, not only
   at a local label or client-side control.

The client must not be the authority for its own premium claim.

## Production runtime — not complete

`BuildConfig.RUNTIME_URL` names the intended HTTPS host, but the repository does
not thereby prove that the AHBG service is deployed, reachable, or serving the
same runtime contract. Before Play publication, verify the production URL from
a release-equivalent client: board load, session creation, plan/state calls,
entitlement verification, and one denied/allowed premium operation.

## Verify (gate items)

Before any billing transaction, configure the purchasing Google account under
Play Console **License testing** and use that same account to accept/install the
test-track build. Test-track membership alone is not a sandbox guarantee.

After the repository acquisition, entitlement-delivery, and production-runtime
boundaries above exist:

- **Free tier**: no purchase → inactive entitlement; Benchmark Lab locked;
  basic play and harness connectivity work.
- **Purchase**: the license-test transaction activates `benchmark_lab`, the
  asynchronous update reaches the WebView, and the verified runtime premium
  surface unlocks.
- **Restore**: the explicit restore control calls RevenueCat restore and
  re-activates the entitlement for the same store account.
- **Persistence**: entitlement state is re-fetched on launch and the eventual
  asynchronous result updates the page; an early synchronous false cannot
  remain stuck for the session.
- **Enforcement**: a premium runtime operation rejects an unverified/inactive
  claim and accepts a valid active entitlement.
- **Degraded/offline**: RevenueCat errors/no-network default to the free tier;
  basic AHBG remains usable.

## hmmm

- Actual project id, product configuration, service-account JSON, and `goog_...`
  SDK key require live accounts and cannot be provisioned from this repository.
- The Play sandbox billing verification remains blocked until purchase/restore,
  asynchronous entitlement delivery, runtime enforcement, and production
  deployment acceptance are implemented.
