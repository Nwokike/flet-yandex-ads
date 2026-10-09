import asyncio
import contextlib
import datetime

import flet as ft
import flet_yandex_ads as fya

# Yandex demo ad unit IDs — replace with your own ad block IDs (R-M-XXXXXX-Y)
# from the Yandex Advertising Network partner interface for production.
DEMO_AD_UNIT_IDS = {
    ft.PagePlatform.ANDROID: {
        "banner": "demo-banner-yandex",
        "interstitial": "demo-interstitial-yandex",
        "rewarded": "demo-rewarded-yandex",
        "app_open": "demo-appopenad-yandex",
    },
    ft.PagePlatform.IOS: {
        "banner": "demo-banner-yandex",
        "interstitial": "demo-interstitial-yandex",
        "rewarded": "demo-rewarded-yandex",
        "app_open": "demo-appopenad-yandex",
    },
}

# Activity terminal — house pattern (Courier New, #A6E22E on #0D0D0D).
TERMINAL_BG = "#0D0D0D"
TERMINAL_TEXT = "#A6E22E"


def main(page: ft.Page):
    page.appbar = ft.AppBar(adaptive=True, title="Yandex Mobile Ads Example")
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 16

    mobile = not page.web and page.platform.is_mobile()
    unit_ids = DEMO_AD_UNIT_IDS.get(page.platform, DEMO_AD_UNIT_IDS[ft.PagePlatform.ANDROID])

    log_text = ft.Text(
        value="",
        font_family="Courier New",
        size=12,
        color=TERMINAL_TEXT,
        selectable=True,
    )
    log_col = ft.Column(controls=[log_text], scroll=ft.ScrollMode.AUTO, expand=True)
    log_terminal = ft.Container(
        content=log_col,
        bgcolor=TERMINAL_BG,
        padding=12,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),
        border_radius=8,
        height=320,
    )

    def log_line(message: str):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        log_text.value = (
            f"{log_text.value}\n[{ts}] {message}" if log_text.value else f"[{ts}] {message}"
        )
        page.update(log_text)

        async def _scroll_to_end():
            await asyncio.sleep(0.05)
            with contextlib.suppress(Exception):
                await log_col.scroll_to(offset=-1)  # offset=-1: jump to newest

        page.run_task(_scroll_to_end)

    if mobile:
        log_line("SDK initializing...")

        # SDK service — applies privacy flags, then initializes.
        page.services.append(
            fya.YandexAdsService(
                user_consent=True,
                logging=True,
                on_initialized=lambda e: log_line("SDK initialized"),
                on_init_failed=lambda e: log_line(f"SDK init FAILED: {e.data}"),
            )
        )

        sticky_banner = fya.BannerAd(
            unit_id=unit_ids["banner"],
            size_type=fya.BannerSizeType.STICKY,
            on_load=lambda e: log_line(f"Sticky banner loaded ({e.width}x{e.height})"),
            on_load_failed=lambda e: log_line(
                f"Sticky banner failed: {e.code} {e.description}"
            ),
            on_click=lambda e: log_line("Sticky banner clicked"),
            on_impression=lambda e: log_line("Sticky banner impression"),
        )

        inline_banner = fya.BannerAd(
            unit_id=unit_ids["banner"],
            size_type=fya.BannerSizeType.INLINE,
            max_height=200,
            on_load=lambda e: log_line(f"Inline banner loaded ({e.width}x{e.height})"),
            on_load_failed=lambda e: log_line(
                f"Inline banner failed: {e.code} {e.description}"
            ),
        )
    else:
        log_line("Yandex Ads are Android/iOS only.")
        log_line("This view verifies UI + logging on this platform.")
        log_line("Build the APK to test live ads:")
        log_line("  uv run flet build apk --split-per-abi")
        sticky_banner = None
        inline_banner = None

    # Full-screen ads: load on button press, show as soon as loaded.
    # Each ad is one-shot — the service is destroyed and removed on dismiss.

    def _make_dismiss_handler(ad, name: str):
        async def _on_dismiss(e):
            log_line(f"{name} dismissed")
            await ad.destroy()
            if ad in page.services:
                page.services.remove(ad)
                page.update()

        return _on_dismiss

    def show_interstitial(e: ft.Event):
        async def on_load(ev):
            log_line("Interstitial loaded - showing")
            await inter.show()

        inter = fya.InterstitialAd(
            unit_id=unit_ids["interstitial"],
            on_load=on_load,
            on_load_failed=lambda ev: log_line(
                f"Interstitial failed: {ev.code} {ev.description}"
            ),
            on_shown=lambda ev: log_line("Interstitial shown"),
            on_impression=lambda ev: log_line("Interstitial impression"),
        )
        inter.on_dismiss = _make_dismiss_handler(inter, "Interstitial")
        page.services.append(inter)
        log_line("Interstitial loading...")

    def show_rewarded(e: ft.Event):
        async def on_load(ev):
            log_line("Rewarded loaded - showing")
            await rw.show()

        rw = fya.RewardedAd(
            unit_id=unit_ids["rewarded"],
            on_load=on_load,
            on_load_failed=lambda ev: log_line(
                f"Rewarded failed: {ev.code} {ev.description}"
            ),
            on_reward=lambda ev: log_line(f"Reward event: +{ev.amount} {ev.type}"),
        )
        rw.on_dismiss = _make_dismiss_handler(rw, "Rewarded")
        page.services.append(rw)
        log_line("Rewarded loading...")

    def show_app_open(e: ft.Event):
        async def on_load(ev):
            log_line("App open loaded - showing")
            await app_open.show()

        app_open = fya.AppOpenAd(
            unit_id=unit_ids["app_open"],
            on_load=on_load,
            on_load_failed=lambda ev: log_line(
                f"App open failed: {ev.code} {ev.description}"
            ),
            on_shown=lambda ev: log_line("App open shown"),
        )
        app_open.on_dismiss = _make_dismiss_handler(app_open, "App open")
        page.services.append(app_open)
        log_line("App open loading...")

    async def reload_banners():
        if sticky_banner is None:
            return
        log_line("Reloading banners...")
        await sticky_banner.reload()
        await inline_banner.reload()

    banner_slots = (
        [ft.Text("Banners", weight=ft.FontWeight.BOLD), sticky_banner, inline_banner]
        if mobile
        else [
            ft.Text("Banners", weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(
                    "Banner slots appear on Android/iOS only.",
                    color=ft.Colors.GREY_500,
                    size=12,
                ),
                padding=12,
                border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),
                border_radius=8,
            ),
        ]
    )

    page.add(
        ft.Column(
            controls=[
                ft.OutlinedButton(
                    content="Show InterstitialAd",
                    on_click=show_interstitial,
                    disabled=not mobile,
                ),
                ft.OutlinedButton(
                    content="Show RewardedAd", on_click=show_rewarded, disabled=not mobile
                ),
                ft.OutlinedButton(
                    content="Show AppOpenAd", on_click=show_app_open, disabled=not mobile
                ),
                ft.OutlinedButton(
                    content="Reload banners",
                    on_click=lambda e: page.run_task(reload_banners),
                    disabled=not mobile,
                ),
                ft.Divider(),
                *banner_slots,
                ft.Divider(),
                ft.Text("Event log", weight=ft.FontWeight.BOLD),
                log_terminal,
            ],
            spacing=8,
        )
    )


if __name__ == "__main__":
    ft.run(main)
