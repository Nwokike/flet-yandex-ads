## flet-yandex-ads v0.1.0

**Yandex Mobile Ads for Flet apps.** A 1:1 wrapping of the official `yandex_mobileads` Flutter plugin in the same architecture as `flet-ads`. Use Yandex as your ad demand source — or as the mediation layer that also serves AdMob, AppLovin, Mintegral, Pangle, Unity and more behind one integration.

### Install

```bash
uv add flet-yandex-ads
```

### What's inside

- **`YandexAdsService`** — one service on `page.services`; applies privacy flags (GDPR consent, location tracking, COPPA age flag) *before* SDK initialization, as the SDK requires. Fires `on_initialized` / `on_init_failed` so the UI never hangs silently.
- **`BannerAd`** — sticky or inline banner, loads on mount, `reload()` for refresh.
- **`InterstitialAd`** / **`RewardedAd`** / **`AppOpenAd`** — full-screen, one-shot each; `wait_for_dismiss()` on rewarded returns the reward.
- Typed events (`BannerLoadedEvent`, `AdRequestErrorEvent`, `AdErrorEvent`, `ImpressionEvent` with ILRD payload, `RewardEvent`) via `ft.EventHandler`.

### Test APKs (this release)

The example app, built with Yandex demo ad units — sideload and every format is live, no account needed:

| Variant | File | For |
| :--- | :--- | :--- |
| ARM64 | `yandexadsexample-arm64-v8a.apk` | Most phones & TV boxes |
| ARMv7 | `yandexadsexample-armeabi-v7a.apk` | Older 32-bit devices |
| x86_64 | `yandexadsexample-x86_64.apk` | Emulators, Chromebooks |

**Android TV:** installs and runs like any Android APK — ads are attempted on TV too (the SDK is an Android SDK). Fill rate on TV is untested territory; the in-app activity terminal logs every event so you can see what happens.

### Fixes in this build

- Typed event handlers use `ft.EventHandler` — `ControlEventHandler` double-wraps the payload, which made handlers receive a bare `Event` and crash on `e.width`/`e.code`. flet-ads 1.0.4 carries this same bug in its `on_paid`; we don't.
- SDK init failures are surfaced (`on_init_failed`) instead of hanging the status forever.
- Banner platform-view mount deadlock fixed — the banner now rebuilds after `load()` so the ad request actually fires.
- `flet run` on desktop no longer crashes: the example gates mobile-only controls and shows a notice instead.

### Notes

- 20/20 tests pass (`uv run pytest`).
- Desktop/Web are not supported (by design, like every mobile ad SDK).
- Known limitation: the Flutter plugin exposes four formats; native/InStream are native-SDK only.
