from typing import Optional

import flet as ft


@ft.control("YandexAdsService")
class YandexAdsService(ft.Service):
    """
    Initializes the Yandex Mobile Ads SDK and configures SDK-wide settings.

    Add one instance to ``page.services`` before any ad control. The SDK
    initializes automatically, with the privacy flags from this service's
    properties applied first (as the SDK requires consent to be set before
    initialization).

    Example:
        ```python
        page.services.append(
            flet_yandex_ads.YandexAdsService(
                user_consent=True,
                logging=True,
            )
        )
        ```

    Raises:
        FletUnsupportedPlatformException: When used on a web and/or
            non-mobile platform.
    """

    user_consent: Optional[bool] = None
    """
    Whether a user from a GDPR country has allowed using their personal
    data for ad targeting. Set before initialization.
    """

    location_tracking: Optional[bool] = None
    """
    Whether using location for ad targeting is allowed. Set before
    initialization.
    """

    age_restricted: Optional[bool] = None
    """
    Whether the user is under the age of consent (COPPA). Android only.
    """

    logging: bool = False
    """Whether the SDK outputs log messages. Defaults to ``False``."""

    debug_error_indicator: bool = False
    """
    Whether the indicator for native ad integration errors is shown.
    Defaults to ``False``.
    """

    on_initialized: Optional[ft.ControlEventHandler["YandexAdsService"]] = None
    """Called when the Mobile Ads SDK finishes initializing."""

    on_init_failed: Optional[ft.ControlEventHandler["YandexAdsService"]] = None
    """
    Called when SDK initialization fails.

    Event handler argument :attr:`~flet.Event.data` contains the error
    description.
    """

    async def initialize(self):
        """
        Initialize the Mobile Ads SDK.

        Initialization runs automatically when the service is added to the
        page; call this to initialize explicitly (safe to call more than
        once).
        """

        await self._invoke_method("initialize")

    async def set_user_consent(self, value: bool):
        """Set the GDPR user consent flag."""

        await self._invoke_method("set_user_consent", {"value": value})

    async def set_location_tracking(self, value: bool):
        """Set the location tracking flag."""

        await self._invoke_method("set_location_tracking", {"value": value})

    async def set_age_restricted(self, value: bool):
        """Set the age-restricted (COPPA) flag. Android only."""

        await self._invoke_method("set_age_restricted", {"value": value})

    async def show_debug_panel(self):
        """Show the Yandex debug panel for network and integration checks."""

        await self._invoke_method("show_debug_panel")

    def before_update(self):
        super().before_update()
        # Android TV is allowed on purpose: the Yandex SDK is an Android SDK
        # and the Flutter plugin renders through the Android platform interface,
        # so ads can be attempted on TV. TV fill rate and remote-control focus
        # are untested territory — that is what the example app is for.
        if self.page.web or (
            not self.page.platform.is_mobile()
            and self.page.platform != ft.PagePlatform.ANDROID_TV
        ):
            raise ft.FletUnsupportedPlatformException(
                f"{self.__class__.__name__} is only supported on "
                f"Mobile (Android, Android TV and iOS)"
            )
