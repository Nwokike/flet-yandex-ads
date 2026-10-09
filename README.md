# flet-yandex-ads

[![pypi](https://img.shields.io/pypi/v/flet-yandex-ads.svg)](https://pypi.python.org/pypi/flet-yandex-ads)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-yandex-ads)
[![license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Nwokike/flet-yandex-ads/blob/main/LICENSE)

Display Yandex Mobile Ads in [Flet](https://flet.dev) apps.

A 1:1 wrapping of the official [yandex_mobileads](https://pub.dev/packages/yandex_mobileads) Flutter plugin, in the same architecture as [flet-ads](https://pypi.org/project/flet-ads/). Yandex is a large demand source on its own, and it can mediate AdMob, AppLovin, Mintegral, Pangle, Unity and more behind one integration.

## Test it without an account

Every release builds an unsigned test APK of the example app with Yandex demo ad units — no signup needed:

### Android Architecture Build Splits

| Variant | Download | Notes |
| :--- | :---: | :--- |
| 📱 **ARM64** (most phones/TVs) | [**yandexadsexample-arm64-v8a.apk**](https://github.com/Nwokike/flet-yandex-ads/releases/latest/download/yandexadsexample-arm64-v8a.apk) | Modern 64-bit Android devices — grab this one unless you know otherwise |
| 📱 **ARMv7** (older phones/TV boxes) | [**yandexadsexample-armeabi-v7a.apk**](https://github.com/Nwokike/flet-yandex-ads/releases/latest/download/yandexadsexample-armeabi-v7a.apk) | Legacy 32-bit Android devices |
| 💻 **x86_64** (emulators/ChromeOS) | [**yandexadsexample-x86_64.apk**](https://github.com/Nwokike/flet-yandex-ads/releases/latest/download/yandexadsexample-x86_64.apk) | Android emulators & Chromebooks |

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Android TV | Web |
|----------|---------|-------|-------|-----|---------|------------|-----|
| Supported|    ❌    |   ❌   |   ❌   |  ✅  |    ✅    |     ✅     |  ❌  |

**Android TV is tested and working.** All four ad formats (sticky banner, inline
banner, interstitial, rewarded) serve on TV and fullscreen ads can be closed
with the remote. App-open ads also serve, though closing them is slightly less
convenient than the rest. TV fill rate is device/region-dependent — the demo
units in the test APK fill, but real fill depends on Yandex's TV demand in
your users' regions.

Desktop and Web are unsupported **upstream**: the `yandex_mobileads` Flutter
plugin only implements Android and iOS, and throws `UnsupportedError` on
other platforms. The extension's platform guard turns that crash into a clean
message.

## Usage

```bash
uv add flet-yandex-ads
```

```python
import flet as ft
import flet_yandex_ads as fya

def main(page: ft.Page):
    page.services.append(fya.YandexAdsService(user_consent=True))
    page.add(fya.BannerAd(unit_id="demo-banner-yandex"))

ft.run(main)
```

The demo ad units (`demo-banner-yandex`, `demo-interstitial-yandex`, `demo-rewarded-yandex`, `demo-appopenad-yandex`) work out of the box. Replace them with your own ad block IDs (`R-M-XXXXXX-Y`) from the [partner interface](https://partner.yandex.com/) for production.

## Controls

| Control | Base | Purpose |
|---|---|---|
| `YandexAdsService` | `ft.Service` | SDK init + privacy flags (consent applied before init, as the SDK requires) |
| `BannerAd` | `ft.LayoutControl` | Sticky or inline banner, loads automatically, `reload()` |
| `InterstitialAd` | `ft.Service` | Full-screen, one-shot per instance |
| `RewardedAd` | `ft.Service` | Full-screen; `wait_for_dismiss()` returns the reward |
| `AppOpenAd` | `ft.Service` | Full-screen, one-shot per instance |

Full-screen ads load when the service is added to the page. Each is one-shot — create a new instance per ad and call `destroy()` afterwards.

### Event handlers

```python
BannerAd(
    unit_id="R-M-XXXXXX-Y",
    on_load=lambda e: print(f"{e.width}x{e.height}"),       # typed
    on_load_failed=lambda e: print(e.code, e.description),  # typed
    on_click=lambda e: print("clicked"),                    # plain
)
```

Typed handlers must use `ft.EventHandler[SomeEvent]`, **not** `ft.ControlEventHandler[SomeEvent]` — `ControlEventHandler[X]` double-wraps `X` in `Event[...]`, so Flet builds a plain `Event` and `e.width` raises `AttributeError`. (flet-ads 1.0.4 has this bug in its `on_paid`.)

Typed events: `BannerLoadedEvent` (width, height), `AdRequestErrorEvent` (code, description, ad_unit_id), `AdErrorEvent` (description), `ImpressionEvent` (impression_data — ILRD), `RewardEvent` (amount, type).

## Configuration

No manifest keys or Info.plist entries are needed for basic operation. Mediation adapters are added to the generated Flutter app's Gradle config — see the [plugin docs](https://ads.yandex.com/helpcenter/en/dev/flutter/).

## Limitations

- The Flutter plugin exposes four formats: banner, interstitial, rewarded, app open. Native and InStream ads exist only in Yandex's native SDKs.
- Ads don't render on desktop or web (by design — same as every mobile ad SDK).

## Example

A complete app (sticky + inline banner, interstitial, rewarded, app open, with an activity-terminal log view) is in [`examples/flet_yandex_ads_example/`](examples/flet_yandex_ads_example/).

## License

MIT
