"""Tests for flet-yandex-ads: control classes, defaults, type names and events."""

import flet as ft
from flet.utils import from_dict

import flet_yandex_ads as fya
from flet_yandex_ads.types import (
    AdErrorEvent,
    AdRequestErrorEvent,
    BannerLoadedEvent,
    BannerSizeType,
    ImpressionEvent,
    RewardEvent,
)


def test_exports():
    """All public names are exported."""
    for name in (
        "AdErrorEvent",
        "AdRequestErrorEvent",
        "AppOpenAd",
        "BannerAd",
        "BannerLoadedEvent",
        "BannerSizeType",
        "BaseAd",
        "FullscreenAd",
        "ImpressionEvent",
        "InterstitialAd",
        "RewardEvent",
        "RewardedAd",
        "YandexAdsService",
    ):
        assert hasattr(fya, name), name


def test_banner_defaults():
    banner = fya.BannerAd(unit_id="demo-banner-yandex")
    assert banner._c == "BannerAd"
    assert banner.unit_id == "demo-banner-yandex"
    assert banner.size_type is BannerSizeType.STICKY
    assert banner.max_height is None


def test_banner_inline_size():
    banner = fya.BannerAd(
        unit_id="b1",
        size_type=BannerSizeType.INLINE,
        max_height=200,
    )
    assert banner.size_type is BannerSizeType.INLINE
    assert banner.size_type.value == "inline"
    assert banner.max_height == 200


def test_banner_event_handlers():
    seen = []
    banner = fya.BannerAd(
        unit_id="b1",
        on_load=lambda e: seen.append("load"),
        on_click=lambda e: seen.append("click"),
        on_impression=lambda e: seen.append("impression"),
    )
    for event in (banner.on_load, banner.on_click, banner.on_impression):
        event(None)
    assert seen == ["load", "click", "impression"]


def test_fullscreen_services():
    inter = fya.InterstitialAd(unit_id="i1")
    assert inter._c == "InterstitialAd"
    assert issubclass(fya.InterstitialAd, ft.Service)
    assert issubclass(fya.InterstitialAd, fya.FullscreenAd)

    rw = fya.RewardedAd(unit_id="r1")
    assert rw._c == "RewardedAd"
    assert rw.on_reward is None

    app_open = fya.AppOpenAd(unit_id="a1")
    assert app_open._c == "AppOpenAd"


def test_fullscreen_event_handlers():
    seen = []
    inter = fya.InterstitialAd(
        unit_id="i1",
        on_load=lambda e: seen.append("load"),
        on_shown=lambda e: seen.append("shown"),
        on_failed_to_show=lambda e: seen.append("failed_to_show"),
        on_dismiss=lambda e: seen.append("dismiss"),
        on_click=lambda e: seen.append("click"),
        on_impression=lambda e: seen.append("impression"),
    )
    for event in (
        inter.on_load,
        inter.on_shown,
        inter.on_failed_to_show,
        inter.on_dismiss,
        inter.on_click,
        inter.on_impression,
    ):
        event(None)
    assert seen == ["load", "shown", "failed_to_show", "dismiss", "click", "impression"]


def test_service_defaults():
    service = fya.YandexAdsService()
    assert service._c == "YandexAdsService"
    assert service.user_consent is None
    assert service.location_tracking is None
    assert service.age_restricted is None
    assert service.logging is False
    assert service.debug_error_indicator is False


def test_service_with_settings():
    service = fya.YandexAdsService(
        user_consent=True,
        location_tracking=False,
        age_restricted=True,
        logging=True,
    )
    assert service.user_consent is True
    assert service.location_tracking is False
    assert service.age_restricted is True
    assert service.logging is True


def test_service_on_initialized():
    seen = []
    service = fya.YandexAdsService(on_initialized=lambda e: seen.append("ok"))
    assert service.on_initialized is not None
    service.on_initialized(None)
    assert seen == ["ok"]


def test_service_on_init_failed():
    from types import SimpleNamespace

    seen = []
    service = fya.YandexAdsService(on_init_failed=lambda e: seen.append(e.data))
    assert service.on_init_failed is not None
    service.on_init_failed(SimpleNamespace(data={"description": "boom"}))
    assert seen == [{"description": "boom"}]


def test_enum_serialization_values():
    """Enum values must match the wire strings read by the Dart side."""
    assert BannerSizeType.STICKY.value == "sticky"
    assert BannerSizeType.INLINE.value == "inline"


def test_event_dataclasses_from_dict():
    """Event dataclasses parse from the snake_case dicts sent by Dart."""
    control = fya.BannerAd(unit_id="b1")

    loaded = from_dict(
        BannerLoadedEvent,
        {"control": control, "name": "load", "width": 320, "height": 50},
    )
    assert loaded.width == 320
    assert loaded.height == 50

    error = from_dict(
        AdRequestErrorEvent,
        {
            "control": control,
            "name": "load_failed",
            "code": 1,
            "description": "no fill",
            "ad_unit_id": "b1",
        },
    )
    assert error.code == 1
    assert error.description == "no fill"

    ad_error = from_dict(
        AdErrorEvent,
        {"control": control, "name": "failed_to_show", "description": "bad state"},
    )
    assert ad_error.description == "bad state"

    impression = from_dict(
        ImpressionEvent,
        {"control": control, "name": "impression", "impression_data": "{...}"},
    )
    assert impression.impression_data == "{...}"

    reward = from_dict(
        RewardEvent,
        {"control": control, "name": "reward", "amount": 5, "type": "coins"},
    )
    assert reward.amount == 5
    assert reward.type == "coins"
