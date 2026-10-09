from typing import Optional

import flet as ft
from flet.utils import from_dict
from flet_yandex_ads.fullscreen_ad import FullscreenAd
from flet_yandex_ads.types import RewardEvent


@ft.control("RewardedAd")
class RewardedAd(ft.Service, FullscreenAd):
    """
    Displays a full-screen Yandex rewarded ad.

    Loads automatically when the service is added to the page. Each
    instance is one-shot — create a new instance for the next ad.

    Example:
        ```python
        def on_reward(e):
            print(f"+{e.amount} {e.type}")

        rw = flet_yandex_ads.RewardedAd(unit_id="R-M-XXXXXX-Y", on_reward=on_reward)
        page.services.append(rw)
        await rw.show()
        await rw.wait_for_dismiss()
        ```

    Raises:
        FletUnsupportedPlatformException: When used on a web and/or
            non-mobile platform.
    """

    on_reward: Optional[ft.EventHandler[RewardEvent["RewardedAd"]]] = None
    """
    Called when the user earns a reward.

    Carries a :class:`~flet_yandex_ads.RewardEvent` with the reward
    ``amount`` and ``type``.
    """

    async def wait_for_dismiss(self) -> Optional[RewardEvent]:
        """
        Wait until the ad is dismissed and return the reward the user
        earned, or ``None`` if the ad was not watched to the end.

        Must be called after :meth:`show`.
        """

        result = await self._invoke_method("wait_for_dismiss")
        if result is None:
            return None
        return from_dict(RewardEvent, {"control": self, "name": "reward", **result})
