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


def main(page: ft.Page):
    page.appbar = ft.AppBar(adaptive=True, title="Yandex Mobile Ads Example")
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 16

    unit_ids = DEMO_AD_UNIT_IDS[page.platform]
    log = ft.Text("SDK initializing...", selectable=True)

    def log_line(message: str):
        log.value = f"{log.value}\n{message}"
        page.update(log)

    # 1. SDK service — applies privacy flags, then initializes.
    page.services.append(
        fya.YandexAdsService(
            user_consent=True,
            logging=True,
        )
    )

    # 2. Sticky banner — loads automatically.
    sticky_banner = fya.BannerAd(
        unit_id=unit_ids["banner"],
        size_type=fya.BannerSizeType.STICKY,
        on_load=lambda e: log_line(f"Sticky banner loaded ({e.width}x{e.height})"),
        on_load_failed=lambda e: log_line(f"Banner failed: {e.code} {e.description}"),
        on_click=lambda e: log_line("Banner clicked"),
        on_impression=lambda e: log_line("Banner impression"),
    )

    # 3. Inline banner with a max height.
    inline_banner = fya.BannerAd(
        unit_id=unit_ids["banner"],
        size_type=fya.BannerSizeType.INLINE,
        max_height=200,
        on_load=lambda e: log_line(f"Inline banner loaded ({e.width}x{e.height})"),
    )

    # 4. Interstitial — loads when added, shown then awaited.
    def show_interstitial(e: ft.Event):
        inter = fya.InterstitialAd(
            unit_id=unit_ids["interstitial"],
            on_load=lambda ev: log_line("Interstitial loaded"),
            on_load_failed=lambda ev: log_line(
                f"Interstitial failed: {ev.code} {ev.description}"
            ),
            on_shown=lambda ev: log_line("Interstitial shown"),
            on_impression=lambda ev: log_line("Interstitial impression"),
            on_dismiss=lambda ev: log_line("Interstitial dismissed"),
        )
        page.services.append(inter)

    # 5. Rewarded — wait_for_dismiss returns the reward.
    def show_rewarded(e: ft.Event):
        rw = fya.RewardedAd(
            unit_id=unit_ids["rewarded"],
            on_load=lambda ev: log_line("Rewarded loaded"),
            on_reward=lambda ev: log_line(f"Reward event: +{ev.amount} {ev.type}"),
        )
        page.services.append(rw)

    # 6. App open ad.
    def show_app_open(e: ft.Event):
        app_open = fya.AppOpenAd(
            unit_id=unit_ids["app_open"],
            on_load=lambda ev: log_line("App open loaded"),
            on_dismiss=lambda ev: log_line("App open dismissed"),
        )
        page.services.append(app_open)

    page.add(
        ft.Column(
            controls=[
                ft.OutlinedButton(content="Show InterstitialAd", on_click=show_interstitial),
                ft.OutlinedButton(content="Show RewardedAd", on_click=show_rewarded),
                ft.OutlinedButton(content="Show AppOpenAd", on_click=show_app_open),
                ft.Divider(),
                sticky_banner,
                inline_banner,
                ft.Divider(),
                log,
            ],
            spacing=12,
        )
    )


if __name__ == "__main__":
    ft.run(main)
