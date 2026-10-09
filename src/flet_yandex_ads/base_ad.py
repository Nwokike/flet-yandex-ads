from dataclasses import dataclass
from typing import Optional

import flet as ft
from flet_yandex_ads.types import AdRequestErrorEvent


@dataclass(kw_only=True)
class BaseAd(ft.BaseControl):
    """
    Base class for all Yandex Mobile Ads controls.

    Defines the shared ad unit ID and the lifecycle event properties that
    every ad format reports.

    Raises:
        FletUnsupportedPlatformException: When used on a web and/or
            non-mobile platform.
    """

    unit_id: str
    """
    Ad unit ID (ad block ID) for this ad, from the Yandex Advertising
    Network partner interface. Looks like ``R-M-XXXXXX-Y``.
    """

    on_load: Optional[ft.ControlEventHandler["BaseAd"]] = None
    """Called when an ad is successfully loaded."""

    on_load_failed: Optional[
        ft.ControlEventHandler[AdRequestErrorEvent["BaseAd"]]
    ] = None
    """
    Called when an ad request fails.

    Carries an :class:`~flet_yandex_ads.AdRequestErrorEvent` with the error
    ``code`` and ``description``.
    """

    on_click: Optional[ft.ControlEventHandler["BaseAd"]] = None
    """Called when the ad is clicked."""

    def before_update(self):
        super().before_update()
        if self.page.web or not self.page.platform.is_mobile():
            raise ft.FletUnsupportedPlatformException(
                f"{self.__class__.__name__} is only supported on "
                f"Mobile (Android and iOS)"
            )
