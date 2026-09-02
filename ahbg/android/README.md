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

# signed release against the production HTTPS endpoint
gradle assembleRelease \
  -PruntimeUrl=https://ahbg.interdependentway.org \
  -PrevenueCatApiKey=rc_public_key \
  -PahbgStoreFile=/secure/ahbg-release.jks -PahbgStorePassword=... \
  -PahbgKeyAlias=... -PahbgKeyPassword=...
```

- `runtimeUrl` defaults to `https://ahbg.interdependentway.org` for release
  builds; debug may point at a local emulator host. Cleartext is allowed only
  for `10.0.2.2`/`localhost` in debug via `network_security_config.xml`.
- `revenueCatApiKey` is a RevenueCat **public** API key provisioned at build
  time and never committed. Without a key the app builds and runs on the free
  tier (`NoopPremiumStore`).

## Entitlement

One clean entitlement: `benchmark_lab` — advanced scenarios, saved/replayed
run comparison, and adversarial benchmark packs. Basic gameplay and external
harness connectivity remain free. The runtime side only checks claims; the
Android side verifies with the RevenueCat SDK.

## hmmm

- Store publication needs signing, versioning policy, and submission assets —
  outside this pass.
- Local emulator uses cleartext HTTP; a release build must switch the runtime
  URL to HTTPS and disable `usesCleartextTraffic`.
