from dataclasses import dataclass
from enum import Enum
from typing import Optional

import flet as ft

__all__ = [
    "AdErrorEvent",
    "AdRequestErrorEvent",
    "BannerLoadedEvent",
    "BannerSizeType",
    "ImpressionEvent",
    "RewardEvent",
]


class BannerSizeType(Enum):
    """Banner ad sizing modes, mirroring the ``BannerAdSize`` API of the
    ``yandex_mobileads`` Flutter plugin."""

    STICKY = "sticky"
    """Sticky banner: stretches to the width of its container, height
    determined by the network."""

    INLINE = "inline"
    """Inline banner: stretches to the width of its container up to
    :attr:`max_height`."""


@dataclass
class BannerLoadedEvent(ft.Event[ft.EventControlType]):
    """Event data fired when a banner ad loads, with its final size."""

    width: int = 0
    """The loaded banner width in density-independent pixels."""

    height: int = 0
    """The loaded banner height in density-independent pixels."""


@dataclass
class AdRequestErrorEvent(ft.Event[ft.EventControlType]):
    """Event data for a failed ad load, mirroring ``AdRequestError``."""

    code: int = 0
    """The error code."""

    description: str = ""
    """The error description."""

    ad_unit_id: Optional[str] = None
    """The ad unit ID that failed, when reported."""


@dataclass
class AdErrorEvent(ft.Event[ft.EventControlType]):
    """Event data for a failed ad display, mirroring ``AdError``."""

    description: str = ""
    """The error description."""


@dataclass
class ImpressionEvent(ft.Event[ft.EventControlType]):
    """Event data for an ad impression, carrying the ILRD payload."""

    impression_data: str = ""
    """Impression-level revenue data as a JSON string (ILRD)."""


@dataclass
class RewardEvent(ft.Event[ft.EventControlType]):
    """Event data for a rewarded ad reward, mirroring ``Reward``."""

    amount: int = 0
    """The reward amount."""

    type: str = ""
    """The reward type."""
