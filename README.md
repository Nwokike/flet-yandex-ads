# flet-yandex-ads

Display [Yandex Mobile Ads](https://ads.yandex.com/) in [Flet](https://flet.dev) apps.

A 1:1 wrapping of the official [`yandex_mobileads`](https://pub.dev/packages/yandex_mobileads) Flutter plugin as a Flet extension, following the same architecture as [`flet-ads`](https://pypi.org/project/flet-ads/).

**What it does for you:** the Yandex Advertising Network is a large demand source in its own right — and it can also mediate AdMob, AppLovin, Mintegral, Pangle, Unity and a dozen more networks behind one integration. Adding it to your app diversifies your revenue away from any single ad network, with strong fill in the CIS, Central Europe, and Asia.

## Installation

```bash
uv add flet-yandex-ads
```

The native code comes transitively from the `yandex_mobileads` plugin — nothing to install manually.

## Test it before you integrate it

Every release builds an unsigned **test APK** (split per ABI) of the example
app, with Yandex demo ad units baked in — download, sideload, and every ad
format is live immediately, no account needed:

**Download the latest test APK:**
[**yandexadsexample-arm64-v8a.apk** (latest release)](https://github.com/Nwokike/flet-yandex-ads/releases/latest/download/yandexadsexample-arm64-v8a.apk)

(Also available: `armeabi-v7a` for older phones, `x86_64` for emulators —
see the [latest release](https://github.com/Nwokike/flet-yandex-ads/releases/latest).)

The demo ad units (`demo-banner-yandex` etc.) serve real test ads. Swap them
for your own ad block IDs (`R-M-XXXXXX-Y`) from the
[partner interface](https://partner.yandex.com/) for production.

## Quick start

```python
import flet as ft
import flet_yandex_ads as fya

def main(page: ft.Page):
    # 1. Initialize the SDK (once, before any ad control)
    page.services.append(fya.YandexAdsService(user_consent=True))

    # 2. Sticky banner — lives in the layout
    page.add(fya.BannerAd(unit_id="demo-banner-yandex"))

    # 3. Interstitial ad — full-screen, loads then shows
    inter = fya.InterstitialAd(unit_id="demo-interstitial-yandex")
    page.services.append(inter)

ft.run(main)
```

The demo ad unit IDs above work out of the box — no registration needed for testing. Get your own ad block IDs (`R-M-XXXXXX-Y`) from the [partner interface](https://partner.yandex.com/) for production.

## Controls

### `YandexAdsService` (ft.Service)

Initializes the SDK and configures SDK-wide settings. Add one instance to `page.services`.

| Property | Type | Default | Description |
|---|---|---|---|
| `user_consent` | `Optional[bool]` | `None` | GDPR consent flag, applied before init |
| `location_tracking` | `Optional[bool]` | `None` | Location targeting flag, applied before init |
| `age_restricted` | `Optional[bool]` | `None` | COPPA age-restricted flag (Android only) |
| `logging` | `bool` | `False` | SDK log output |
| `debug_error_indicator` | `bool` | `False` | Native-ad integration error indicator |

Methods: `initialize()`, `set_user_consent(value)`, `set_location_tracking(value)`, `set_age_restricted(value)`, `show_debug_panel()`.

### `BannerAd` (ft.LayoutControl)

Banner ad rendered inline. Loads automatically; `reload()` loads a new ad.

| Property | Type | Default | Description |
|---|---|---|---|
| `unit_id` | `str` | required | Ad block ID (`R-M-XXXXXX-Y`) |
| `size_type` | `BannerSizeType` | `STICKY` | `STICKY` or `INLINE` |
| `max_height` | `Optional[int]` | `None` | Max height (dp) for `INLINE` |

Events: `on_load` (carries final `width`/`height`), `on_load_failed`, `on_click`, `on_impression` (carries the ILRD impression payload).

Methods: `reload()`.

### `InterstitialAd` / `RewardedAd` / `AppOpenAd` (ft.Service)

Full-screen ads. Load automatically when added to the page; one-shot per instance.

Events: `on_load`, `on_load_failed`, `on_shown`, `on_failed_to_show`, `on_dismiss`, `on_click`, `on_impression` — plus `on_reward` for `RewardedAd`.

Methods: `load()`, `show()`, `wait_for_dismiss()` (returns the `RewardEvent` for `RewardedAd`), `cancel_loading()`, `destroy()`.

```python
rw = fya.RewardedAd(unit_id="demo-rewarded-yandex")
page.services.append(rw)
await rw.show()
reward = await rw.wait_for_dismiss()   # RewardEvent(amount=..., type=...) or None
```

## Build-time configuration

Yandex needs no manifest keys or Info.plist entries for basic operation — the SDK injects its permissions automatically. Mediation adapters are added to the generated Flutter app's Gradle config; see the [plugin docs](https://ads.yandex.com/helpcenter/en/dev/flutter/) for the maven repositories and `com.yandex.android:mobileads-mediation` dependency.

## Writing your own event handlers

Handlers come in two flavors, and the annotation matters:

```python
# Plain handler — receives the Event; payload (if any) is in e.data
BannerAd(unit_id="R-M-XXXXXX-Y", on_click=lambda e: print(e.data))

# Typed handler — receives the dataclass with its fields
BannerAd(
    unit_id="R-M-XXXXXX-Y",
    on_load=lambda e: print(f"{e.width}x{e.height}"),
)
```

Typed handlers must be declared with `ft.EventHandler[SomeEvent]`, **not**
`ft.ControlEventHandler[SomeEvent]`. `ControlEventHandler[X]` wraps `X` in
`Event[...]`, so Flet's resolver returns `Event[X]`, drops the generic when
building the event, and your handler receives a plain `Event` with no fields —
`e.width` raises `AttributeError`. (The official `flet-ads` 1.0.4 has this bug
in its `on_paid` handler; we deliberately deviate from it.)

Available typed events: `BannerLoadedEvent` (width, height),
`AdRequestErrorEvent` (code, description, ad_unit_id), `AdErrorEvent`
(description), `ImpressionEvent` (impression_data — the ILRD payload),
`RewardEvent` (amount, type).

## Limitations

- **Android + iOS only.** AdMob and all other Flutter ad plugins are mobile-only; Android TV (CTV) is supported only by Yandex's native Android SDK, not the Flutter plugin.
- Native and InStream ad formats are not exposed by the Flutter plugin (banner, interstitial, rewarded and app-open are).

## Example

A complete app (sticky + inline banner, interstitial, rewarded, app open, with event logging) is in [`examples/flet_yandex_ads_example/`](examples/flet_yandex_ads_example/) and runs out of the box with demo ad units.

## License

MIT
