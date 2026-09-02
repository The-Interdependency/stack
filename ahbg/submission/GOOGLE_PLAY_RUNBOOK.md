# Google Play publication runbook (primary path)

Shipaton entry: published Play Store URL. AHBG targets Android 16 / API 36
with AGP 8.9.1 + Gradle 8.11.1, RevenueCat 10.19.1 (core supports Play by
default), and a signed AAB.

## 0. Code (done)

- `compileSdk`/`targetSdk` 36, AGP 8.9.1, Gradle 8.11.1, `bundleRelease` in CI.
- RevenueCat `purchases:10.19.1` only; ordinary `PurchasesConfiguration` is the
  correct Google Play configuration.
- Package `org.interdependency.ahbg`; product `ahbg_benchmark_lab`; entitlement
  `benchmark_lab`.
- Android presentation exposes explicit **Unlock Benchmark Lab** and **Restore
  purchase** controls. Purchase fetches the current RevenueCat offering and
  buys the package carrying `ahbg_benchmark_lab`; restore calls
  `restorePurchases`. Missing/invalid keys fail closed to free play.

## 1. Play Console

1. Create/select the Play developer account.
   - **hmmm**: if this is a newly created personal account, start the closed
     test immediately — Google currently requires the applicable production
     access testing period before production promotion.
2. Create the app (`org.interdependency.ahbg`) and complete the store listing
   with `STORE_LISTING.md`, `PRIVACY_POLICY.md`, icon, and screenshots.
3. Complete the Play **App content** declarations required for publication:
   - Data safety;
   - public privacy-policy URL;
   - Ads declaration;
   - App access declaration/instructions;
   - Target audience and content;
   - Content rating questionnaire;
   - any additional declaration Play Console marks required for this app.

Do not treat an uploaded AAB or a complete store listing as production-ready
while Play Console still reports required App content tasks.

## 2. Release artifact (Play-native AAB)

Build with the release keystore kept outside Git:

```bash
gradle bundleRelease \
  -PruntimeUrl=https://ahbg.interdependentway.org \
  -PrevenueCatApiKey=goog_public_sdk_key \
  -PahbgStoreFile=/secure/ahbg-release.jks -PahbgStorePassword=... \
  -PahbgKeyAlias=... -PahbgKeyPassword=...
```

CI verifies `bundleRelease` on every change (unsigned when no keystore is
provisioned). Upload the signed AAB as the first internal/closed test release.

## 3. Google Play one-time product

1. Play Console → Monetize → Products → One-time products / In-app products.
2. Create `ahbg_benchmark_lab` ("Benchmark Lab"). Product configuration may
   require an uploaded test build first.
3. Configure and **activate a purchase option** for the product:
   - buy/non-consumable behavior (permanent Benchmark Lab access);
   - regional availability;
   - price;
   - active status.
4. Confirm the product is published/available to the chosen test track before
   expecting RevenueCat or Play Billing to return it.

The product record alone is not the purchase gate; the active purchase option
is what makes the one-time product sellable to an eligible account.

## 4. RevenueCat Google Play connection

1. RevenueCat dashboard → add a **Google Play** app for
   `org.interdependency.ahbg`.
2. Google Cloud Console → create a **service account** for RevenueCat.
3. Enable **Google Play Developer API** and **Google Play Reporting API**
   on the project.
4. Play Console → Users and permissions → invite the service account and
   grant the permissions RevenueCat's current checklist requires.
5. Generate a JSON key for the service account and upload it to RevenueCat.
   **hmmm**: credential activation is an external propagation boundary; do not
   diagnose the app from a newly provisioned credential until RevenueCat/Play
   report the connection healthy.
6. In RevenueCat:
   - create entitlement `benchmark_lab`;
   - import/map product `ahbg_benchmark_lab` to that entitlement;
   - place the product in a package in the **current/default offering**.
7. Copy the app-specific RevenueCat **Google Play public SDK key** (`goog_...`)
   into the build. `rc_...` project identifiers are not Android public SDK
   keys and must not be passed to `Purchases.configure`.

## 5. License testing + sandbox purchase

Before buying anything, configure the purchasing Google account as a Play
**license tester**. Test-track membership alone is not the billing sandbox.

1. Play Console → Settings → License testing → add/select the tester account.
2. Ensure the same Google account is eligible for the internal/closed test and
   accepts the test invitation/opt-in.
3. Install the test release from Google Play using that account.
4. Verify the Play purchase sheet identifies the transaction as a test
   purchase / uses a test payment instrument before proceeding. If it presents
   an ordinary charge, stop and repair the test-account configuration.
5. Verify free tier: basic play and external harness connectivity work.
6. Tap **Unlock Benchmark Lab** → `benchmark_lab` becomes active.
7. Tap **Restore purchase** → the same Play account re-activates the entitlement.
8. Force-stop and relaunch → entitlement remains correct.

## 6. Production

1. Complete the required closed-test/production-access gate if the developer
   account is subject to it.
2. Confirm every required App content declaration is complete and Play Console
   reports no blocking tasks.
3. Apply for production access, promote the release, obtain the public Play
   Store URL.
4. Use that URL as the Devpost entry.

## hmmm

- Play account eligibility, tester-duration requirements, review timing,
  service-account activation, live product availability, and the final public
  listing are external state and must be observed in the live consoles.
- A repository build proves code/artifact readiness; it does not prove a
  sandbox purchase, policy declaration, review approval, or store publication.
