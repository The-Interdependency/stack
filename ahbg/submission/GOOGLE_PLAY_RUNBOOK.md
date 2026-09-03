# Google Play publication runbook (primary path)

Shipaton entry: published Play Store URL. AHBG targets Android 16 / API 36
with AGP 8.9.1 + Gradle 8.11.1, RevenueCat 10.19.1 (core supports Play by
default), and a signed AAB.

## 0. Repository state

- `compileSdk`/`targetSdk` 36, AGP 8.9.1, Gradle 8.11.1, `bundleRelease` in CI.
- RevenueCat `purchases:10.19.1` only (no Galaxy module); ordinary
  `PurchasesConfiguration` is the correct Play configuration.
- Package `org.interdependency.ahbg`; entitlement `benchmark_lab` unchanged.
- Entitlement lookup exists, but the Android/WebView surface currently reads a
  synchronous Boolean while RevenueCat refreshes customer info asynchronously.
- Purchase initiation and explicit restore controls are not yet implemented.
- Verified client-to-runtime entitlement transport and enforcement of the
  premium operations are not yet implemented.
- `BuildConfig.RUNTIME_URL` points at the intended production host, but a source
  constant is not deployment evidence. Production TLS/reachability and the
  AHBG runtime service still require end-to-end acceptance.

Do not call the Play billing or publication gate complete until those repository
boundaries and the live-account boundaries below have been verified.

## 1. Play Console

1. Create/select the Play developer account.
   - **hmmm**: if this is a newly created personal account, start the closed
     test immediately — Google currently requires 12 continuously opted-in
     testers for at least 14 days before production access.
2. Create the app (`org.interdependency.ahbg`) and complete the store listing
   with `STORE_LISTING.md`, `PRIVACY_POLICY.md`, icon, and screenshots.
3. Complete the mandatory **App content** declarations before production,
   including the applicable "none" declaration when the app has no such
   features:
   - Data safety;
   - public privacy-policy URL;
   - ads declaration;
   - app-access declaration/instructions;
   - target audience and content declarations;
   - content-rating questionnaire;
   - Financial features declaration; and
   - Health apps declaration.

## 2. Release artifact (Play-native AAB)

Build with the release keystore kept outside Git and the Google Play app's
RevenueCat public SDK key (`goog_...`):

```bash
gradle bundleRelease \
  -PruntimeUrl=https://ahbg.interdependentway.org \
  -PrevenueCatApiKey=<goog_public_sdk_key> \
  -PahbgStoreFile=/secure/ahbg-release.jks -PahbgStorePassword=... \
  -PahbgKeyAlias=... -PahbgKeyPassword=...
```

CI verifies `bundleRelease` on every change (unsigned when no keystore is
provisioned). Upload the signed AAB as the first internal/closed test release.

## 3. Google Play one-time product

1. Play Console → Monetize → Products → one-time products/in-app products.
2. Create `ahbg_benchmark_lab` for "Benchmark Lab" after a test build is
   uploaded.
3. Create and activate the product's **non-consumable purchase option**.
4. Configure its price and required regional availability, then confirm the
   option is active. A catalog product without an active purchase option is not
   sellable.

## 4. RevenueCat Google Play connection

1. RevenueCat dashboard → add a **Google Play** app for
   `org.interdependency.ahbg`.
2. Google Cloud Console → create a **service account** for RevenueCat.
3. Enable **Google Play Developer API** and **Google Play Reporting API**
   on the project.
4. Play Console → Users and permissions → invite the service account and
   grant the permissions required by RevenueCat's current checklist.
5. Generate a JSON key for the service account and upload it to RevenueCat.
   **hmmm**: RevenueCat notes service credentials can take up to 36 hours to
   activate.
6. In RevenueCat, map product `ahbg_benchmark_lab` → entitlement
   `benchmark_lab` → default offering.
7. Record the RevenueCat project ID exactly as shown by RevenueCat; v2 project
   IDs use the `proj...` form. This is project metadata, not an Android SDK key.
8. Copy the Google Play app's RevenueCat **public SDK API key** (`goog_...`)
   into the Android build.

## 5. Repository billing and entitlement gate

Sandbox verification is **repository-blocked** until all of these are real:

1. fetch the current RevenueCat offering/package and initiate purchase of
   `ahbg_benchmark_lab` from a user-visible control;
2. expose an explicit restore control using RevenueCat restore and handle
   success/cancel/error outcomes;
3. notify/refresh the WebView when asynchronous customer-info refresh changes
   `benchmark_lab`, including on cold start rather than relying on one early
   synchronous read;
4. carry a server-verifiable entitlement claim to the runtime and enforce it at
   the premium operations instead of changing only a local status label; and
5. deploy the production runtime and verify TLS, `board.html`, session creation,
   plan/state calls, entitlement checks, and the premium gate through the exact
   production URL.

Do not replace these with a local Boolean, a documentation assertion, or an
unverified client field.

## 6. Sandbox purchase + restore + persistence verification

Once section 5 exists:

1. Play Console → Settings → License testing: add the Google account that will
   perform the billing test. Test-track membership alone does not make a
   transaction a license-test/sandbox purchase.
2. With that same account, accept the internal/closed test invitation and
   install the Play-delivered test release.
3. Verify free tier: basic play and external harness connectivity work.
4. Fetch the current RevenueCat offering and initiate purchase of
   `ahbg_benchmark_lab`; confirm the verified runtime premium surface unlocks.
5. Invoke the app's explicit restore path; confirm the entitlement re-activates
   for the same store account and the WebView receives the refreshed state.
6. Force-stop and relaunch; confirm asynchronous customer-info refresh restores
   the correct state without requiring a page reload or second app start.
7. Exercise one premium operation and prove the runtime rejects it without a
   valid entitlement and accepts it with the verified entitlement.

## 7. Production

1. Deploy the production AHBG runtime at the exact configured HTTPS URL and run
   the end-to-end health checks in section 5 from a release-equivalent client.
2. Complete the required closed test if the account is subject to it.
3. Complete all App content declarations and resolve every Play Console
   publication blocker.
4. Apply for production access, promote the release, obtain the public Play
   Store URL.
5. Use that URL as the Devpost entry.

## Galaxy (deferred/optional)

Galaxy Store is deferred compatibility, not an active Shipaton dependency.
If re-enabled later, re-add `purchases-store-galaxy` (RevenueCat >= 10.7.0)
and follow the archived Galaxy notes.

## hmmm

The repository can build the AAB and observe an existing RevenueCat entitlement,
but acquisition, asynchronous UI refresh, verified runtime enforcement, and
production-runtime acceptance remain repository work. Play account approval,
live service credentials, policy declarations, and the real billing transaction
remain external.
