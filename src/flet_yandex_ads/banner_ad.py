from typing import Optional

import flet as ft
from flet_yandex_ads.base_ad import BaseAd
from flet_yandex_ads.types import BannerLoadedEvent, BannerSizeType, ImpressionEvent


@ft.control("BannerAd")
class BannerAd(ft.LayoutControl, BaseAd):
    """
    Displays a Yandex banner ad inside the layout.

    Loads automatically when added to the page and reloads on demand via
    :meth:`reload`. The final size is reported in
    :attr:`on_load`.

    Example:
        ```python
        flet_yandex_ads.BannerAd(
            unit_id="R-M-XXXXXX-Y",
            size_type=flet_yandex_ads.BannerSizeType.STICKY,
            on_load=lambda e: print(f"banner {e.width}x{e.height}"),
        )
        ```

    Raises:
        FletUnsupportedPlatformException: When used on a web and/or
            non-mobile platform.
    """

    size_type: BannerSizeType = BannerSizeType.STICKY
    """
    Banner sizing mode: :attr:`~flet_yandex_ads.BannerSizeType.STICKY`
    (default) or :attr:`~flet_yandex_ads.BannerSizeType.INLINE`.
    """

    max_height: Optional[int] = None
    """
    Maximum banner height in dp, for the
    :attr:`~flet_yandex_ads.BannerSizeType.INLINE` size type. Defaults to a
    third of the screen height.
    """

    on_load: Optional[ft.EventHandler[BannerLoadedEvent["BannerAd"]]] = None
    """
    Called when the banner loads.

    Carries a :class:`~flet_yandex_ads.BannerLoadedEvent` with the final
    banner ``width`` and ``height``.
    """

    on_impression: Optional[ft.EventHandler[ImpressionEvent["BannerAd"]]] = None
    """
    Called when an impression occurs.

    Carries an :class:`~flet_yandex_ads.ImpressionEvent` with the ILRD
    impression payload.
    """

    async def reload(self):
        """Load a new ad into this banner."""

        await self._invoke_method("reload")
