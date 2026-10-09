from dataclasses import dataclass
from typing import Optional

import flet as ft
from flet_yandex_ads.base_ad import BaseAd
from flet_yandex_ads.types import AdErrorEvent, ImpressionEvent


@dataclass(kw_only=True)
class FullscreenAd(BaseAd):
    """
    Base class for full-screen ad controls (interstitial, rewarded,
    app open).

    Loads automatically when the service is added to the page. Each ad is
    one-shot: after it is dismissed, create a new instance.
    """

    on_shown: Optional[ft.ControlEventHandler["FullscreenAd"]] = None
    """Called when the ad is shown."""

    on_failed_to_show: Optional[ft.EventHandler[AdErrorEvent["FullscreenAd"]]] = None
    """
    Called when the ad fails to show.

    Carries an :class:`~flet_yandex_ads.AdErrorEvent` with the error
    ``description``.
    """

    on_dismiss: Optional[ft.ControlEventHandler["FullscreenAd"]] = None
    """Called when the ad is dismissed."""

    on_impression: Optional[ft.EventHandler[ImpressionEvent["FullscreenAd"]]] = None
    """
    Called when an impression occurs.

    Carries an :class:`~flet_yandex_ads.ImpressionEvent` with the ILRD
    impression payload.
    """

    async def load(self):
        """
        Load an ad.

        Loading starts automatically when the service is added to the page;
        call this to reload after a failure.
        """

        await self._invoke_method("load")

    async def show(self):
        """Show the loaded ad on top of the application."""

        await self._invoke_method("show")

    async def wait_for_dismiss(self):
        """
        Wait until the ad is dismissed.

        Must be called after :meth:`show`; returns when the ad closes.
        """

        await self._invoke_method("wait_for_dismiss")

    async def cancel_loading(self):
        """Cancel a pending load."""

        await self._invoke_method("cancel_loading")

    async def destroy(self):
        """Destroy the ad and free its resources."""

        await self._invoke_method("destroy")
