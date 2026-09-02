# AHBG Android surface

Thinnest Android-first application around the canonical runtime. The mobile
layer presents and controls AHBG; it is **not** a second game engine and not a
geometry authority.

## Architecture

```text
Android app (WebView + JS bridge + JSON transport)
        │  observe/plan/act JSON over HTTP
        ▼
ahbg.runtime.server  (ahbg/runtime/server.py)
        │
        ▼
canonical runtime (ahbg/runtime + frozen Grok engine + UCNS geometry)
```

- `MainActivity` hosts the canonical presentation board (`ahbg/presentation`)
  in a WebView and exposes `window.ahbg` to the board.
- `HarnessClient` transports JSON to the runtime bridge; it owns no game state.
- `Entitlements.kt` wraps one RevenueCat entitlement, `benchmark_lab`, and owns
  the Google Play purchase/restore calls used by the presentation bridge.
- Bundled board assets are a pinned copy of `ahbg/presentation` (see
  `sync_presentation.sh` and `PRESENTATION.sha256`).

## Build

```bash
cd ahbg/android
gradle assembleDebug -PruntimeUrl=http://10.0.2.2:8765

# Google Play release artifact: signed AAB
gradle bundleRelease \
  -PruntimeUrl=https://ahbg.interdependentway.org \
  -PrevenueCatApiKey=goog_public_sdk_key \
  -PahbgStoreFile=/secure/ahbg-release.jks -PahbgStorePassword=... \
  -PahbgKeyAlias=... -PahbgKeyPassword=...
```

- `runtimeUrl` defaults to `https://ahbg.interdependentway.org` for release
  builds; debug may point at a local emulator host. Cleartext is allowed only
  for `10.0.2.2`/`localhost` in debug via `network_security_config.xml`.
- `revenueCatApiKey` is the app-specific RevenueCat **Google Play public SDK
  key** (`goog_...`) provisioned at build time and never committed. Missing or
  non-Google keys fail closed to the free tier instead of starting billing.
- Google Play accepts the `bundleRelease` AAB. `assembleRelease` remains useful
  only for local APK diagnostics and is not the publishing artifact.

## Entitlement

One clean entitlement: `benchmark_lab` — advanced scenarios, saved/replayed
run comparison, and adversarial benchmark packs. Basic gameplay and external
harness connectivity remain free. The Android bridge exposes an explicit
purchase control and an explicit restore control; both refresh the same
RevenueCat entitlement state.

## hmmm

- Live billing verification still requires the app to be installed from a Play
  test track with the product, purchase option, RevenueCat mapping, and license
  tester account configured.
- Production publication remains an external Play Console/account gate; see
  `../submission/GOOGLE_PLAY_RUNBOOK.md` and `SUBMISSION_BLOCKERS.md`.
