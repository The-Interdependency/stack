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
- `Entitlements.kt` wraps one RevenueCat entitlement, `benchmark_lab`.
- Bundled board assets are a pinned copy of `ahbg/presentation` (see
  `sync_presentation.sh` and `PRESENTATION.sha256`).

## Build

```bash
cd ahbg/android
gradle assembleDebug -PruntimeUrl=http://10.0.2.2:8765

# Google Play release artifact: signed Android App Bundle (AAB)
gradle bundleRelease \
  -PruntimeUrl=https://ahbg.interdependentway.org \
  -PrevenueCatApiKey=<goog_public_sdk_key> \
  -PahbgStoreFile=/secure/ahbg-release.jks -PahbgStorePassword=... \
  -PahbgKeyAlias=... -PahbgKeyPassword=...
```

- `runtimeUrl` defaults to `https://ahbg.interdependentway.org` for release
  builds; debug may point at a local emulator host. Cleartext is allowed only
  for `10.0.2.2`/`localhost` in debug via `network_security_config.xml`.
- `revenueCatApiKey` is the Google Play app's RevenueCat **public SDK key**
  (`goog_...`) provisioned at build time and never committed. A RevenueCat
  `rc_...` project identifier is not the Android SDK key. Without a key the app
  builds and runs on the free tier (`NoopPremiumStore`).

## Entitlement

One clean entitlement: `benchmark_lab` — advanced scenarios, saved/replayed
run comparison, and adversarial benchmark packs. Basic gameplay and external
harness connectivity remain free. The runtime side only checks claims; the
Android side verifies with the RevenueCat SDK.

Current boundary: entitlement lookup is implemented, but purchase initiation
and explicit restore controls are not. See
`../submission/SUBMISSION_BLOCKERS.md`; the Play sandbox billing gate remains
blocked until those user-visible operations are wired and tested.

## hmmm

- Store publication needs a production keystore, Play/RevenueCat provisioning,
  policy declarations, purchase/restore wiring, and live sandbox verification.
- Local emulator uses cleartext HTTP; release uses the production HTTPS runtime
  URL.
