import flet as ft
from flet_yandex_ads.fullscreen_ad import FullscreenAd


@ft.control("AppOpenAd")
class AppOpenAd(ft.Service, FullscreenAd):
    """
    Displays a full-screen Yandex app open ad.

    Loads automatically when the service is added to the page. Each
    instance is one-shot — create a new instance for the next ad.

    Raises:
        FletUnsupportedPlatformException: When used on a web and/or
            non-mobile platform.
    """
