import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:yandex_mobileads/mobile_ads.dart';

/// Flet control rendering a Yandex banner ad via the ``AdWidget`` of the
/// ``yandex_mobileads`` plugin.
///
/// The banner width follows the layout width; the size type (sticky or
/// inline) and the inline max height come from the control properties.
class BannerAdControl extends StatefulWidget {
  final Control control;

  const BannerAdControl({super.key, required this.control});

  @override
  State<BannerAdControl> createState() => _BannerAdControlState();
}

class _BannerAdControlState extends State<BannerAdControl> with FletStoreMixin {
  BannerAd? _bannerAd;
  StreamSubscription<BannerAdLoadState>? _loadStateSubscription;
  StreamSubscription<BannerAdEvent>? _eventsSubscription;

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
    _createBanner();
  }

  String get _unitId => widget.control.getString("unit_id", "")!;

  void _createBanner() {
    final screenWidth = MediaQuery.of(context).size.width.round();
    final screenHeight = MediaQuery.of(context).size.height.round();
    final isSticky = widget.control.getString("size_type", "sticky") != "inline";

    final BannerAdSize adSize = isSticky
        ? BannerAdSize.sticky(width: screenWidth)
        : BannerAdSize.inline(
            width: screenWidth,
            maxHeight: widget.control.getInt("max_height", screenHeight ~/ 3)!,
          );

    final banner = BannerAd(adSize: adSize);

    _loadStateSubscription = banner.loadStateStream.listen((state) {
      if (state is BannerAdLoadStateLoaded) {
        widget.control.triggerEvent("load", {
          "width": state.width,
          "height": state.height,
        });
      } else if (state is BannerAdLoadStateError) {
        widget.control.triggerEvent("load_failed", {
          "code": state.error.code,
          "description": state.error.description,
          "ad_unit_id": _unitId,
        });
      }
    });

    _eventsSubscription = banner.events.listen((event) {
      if (event is BannerAdClickedEvent) {
        widget.control.triggerEvent("click");
      } else if (event is BannerAdImpressionEvent) {
        widget.control.triggerEvent("impression", {
          "impression_data": event.impressionData.getRawData(),
        });
      }
    });

    _bannerAd = banner;
    _loadBanner(banner);
  }

  Future<void> _loadBanner(BannerAd banner) async {
    // Make sure the SDK is initialized before the first load; the call is
    // idempotent and normally already done by YandexAdsService.
    await YandexAds.initialize();
    banner.load(AdRequest(adUnitId: _unitId));
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "reload":
        final banner = _bannerAd;
        if (banner != null) {
          await _loadBanner(banner);
        }
        return null;
      default:
        throw Exception("Unknown BannerAd method: $name");
    }
  }

  @override
  void dispose() {
    widget.control.removeInvokeMethodListener(_invokeMethod);
    _loadStateSubscription?.cancel();
    _eventsSubscription?.cancel();
    _bannerAd?.destroy();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final banner = _bannerAd;
    if (banner == null) return const SizedBox.shrink();
    return LayoutControl(
      control: widget.control,
      child: AdWidget(bannerAd: banner),
    );
  }
}
