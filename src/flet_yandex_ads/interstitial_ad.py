import flet as ft
from flet_yandex_ads.fullscreen_ad import FullscreenAd


@ft.control("InterstitialAd")
class InterstitialAd(ft.Service, FullscreenAd):
    """
    Displays a full-screen Yandex interstitial ad.

    Loads automatically when the service is added to the page. Each
    instance is one-shot — create a new instance for the next ad.

    Example:
        ```python
        inter = flet_yandex_ads.InterstitialAd(unit_id="R-M-XXXXXX-Y")
        page.services.append(inter)
        await inter.show()
        await inter.wait_for_dismiss()
        ```

    Raises:
        FletUnsupportedPlatformException: When used on a web and/or
            non-mobile platform.
    """
