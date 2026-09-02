# Google Play publication runbook (primary path)

Shipaton entry: published Play Store URL. AHBG targets Android 16 / API 36
with AGP 8.9.1 + Gradle 8.11.1, RevenueCat 10.19.1 (core supports Play by
default), and a signed AAB.

## 0. Code (done)

- `compileSdk`/`targetSdk` 36, AGP 8.9.1, Gradle 8.11.1, `bundleRelease` in CI.
- RevenueCat `purchases:10.19.1` only (no Galaxy module); ordinary
  `PurchasesConfiguration` is the correct Play configuration.
- Package `org.interdependency.ahbg`; entitlement `benchmark_lab` unchanged.

## 1. Play Console

1. Create/select the Play developer account.
   - **hmmm**: if this is a newly created personal account, start the closed
     test immediately — Google currently requires 12 continuously opted-in
     testers for at least 14 days before production access.
2. Create the app (`org.interdependency.ahbg`) and complete the store listing
   with `STORE_LISTING.md`, `PRIVACY_POLICY.md`, icon, and screenshots.

## 2. Release artifact (Play-native AAB)

Build with the release keystore kept outside Git:

```bash
gradle bundleRelease \
  -PruntimeUrl=https://ahbg.interdependentway.org \
  -PrevenueCatApiKey=<rc_public_sdk_key> \
  -PahbgStoreFile=/secure/ahbg-release.jks -PahbgStorePassword=... \
  -PahbgKeyAlias=... -PahbgKeyPassword=...
```

CI verifies `bundleRelease` on every change (unsigned when no keystore is
provisioned). Upload the signed AAB as the first internal/closed test release.

## 3. Google Play in-app product

1. Play Console → Monetize → Products → In-app products.
2. Create `ahbg_benchmark_lab` (non-consumable, one-time purchase,
   "Benchmark Lab"). Product configuration requires an uploaded test build
   first, so upload the test release before this step.

## 4. RevenueCat Google Play connection

1. RevenueCat dashboard → add a **Google Play** app for
   `org.interdependency.ahbg`.
2. Google Cloud Console → create a **service account** for RevenueCat.
3. Enable **Google Play Developer API** and **Google Play Reporting API**
   on the project.
4. Play Console → Users and permissions → invite the service account and
   grant the required permissions (Financial data / View app information /
   Manage orders etc. per RevenueCat's current checklist).
5. Generate a JSON key for the service account and upload it to RevenueCat.
   **hmmm**: RevenueCat notes service credentials can take up to 36 hours to
   activate.
6. In RevenueCat, map product `ahbg_benchmark_lab` → entitlement
   `benchmark_lab` → default offering.
7. Copy the RevenueCat **public SDK API key** into the build (`rc_...` or
   `goog_...` public key).

## 5. Sandbox purchase + restore + persistence verification

On the Play test track:

1. Install the signed AAB test release.
2. Verify free tier: basic play and external harness connectivity work.
3. Sandbox purchase `ahbg_benchmark_lab` → `benchmark_lab` unlocks.
4. Restore purchases → entitlement re-activates on the same account.
5. Force-stop and relaunch → entitlement remains correct (persistence).

## 6. Production

1. Complete the 12 testers × 14 days closed test if a new personal account.
2. Apply for production access, promote the release, obtain the public Play
   Store URL.
3. Use that URL as the Devpost entry.

## Galaxy (deferred/optional)

Galaxy Store is deferred compatibility, not an active Shipaton dependency.
If re-enabled later, re-add `purchases-store-galaxy` (RevenueCat >= 10.7.0)
and follow the archived Galaxy notes.
