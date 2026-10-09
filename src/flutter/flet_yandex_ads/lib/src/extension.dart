import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';

import 'app_open_ad.dart';
import 'banner_ad.dart';
import 'interstitial_ad.dart';
import 'rewarded_ad.dart';
import 'service.dart';

class Extension extends FletExtension {
  @override
  void ensureInitialized() {
    // SDK initialization is driven by the YandexAdsService control, which
    // carries the privacy flags. No initialization happens here.
  }

  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "YandexAdsService":
        return YandexAdsService(control: control);
      case "InterstitialAd":
        return InterstitialAdService(control: control);
      case "RewardedAd":
        return RewardedAdService(control: control);
      case "AppOpenAd":
        return AppOpenAdService(control: control);
      default:
        return null;
    }
  }

  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "BannerAd":
        return BannerAdControl(control: control);
      default:
        return null;
    }
  }
}
