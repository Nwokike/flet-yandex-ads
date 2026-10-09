import 'package:flet/flet.dart';
import 'package:yandex_mobileads/mobile_ads.dart';

/// Flet service loading and showing a Yandex app open ad.
///
/// Loading starts when the service is added to the page. Each ad is
/// one-shot — create a new instance for the next ad.
class AppOpenAdService extends FletService {
  AppOpenAdService({required super.control});

  final _loader = AppOpenAdLoader();
  AppOpenAd? _ad;

  @override
  void init() {
    super.init();
    control.addInvokeMethodListener(_invokeMethod);
    _load();
  }

  String get _unitId => control.getString("unit_id", "")!;

  Future<void> _load() async {
    await YandexAds.initialize();
    try {
      final ad = await _loader.loadAd(adRequest: AdRequest(adUnitId: _unitId));
      _ad = ad;
      control.triggerEvent("load");
    } on AdRequestError catch (e) {
      control.triggerEvent("load_failed", {
        "code": e.code,
        "description": e.description,
        "ad_unit_id": e.adUnitId,
      });
    }
  }

  void _attachListener(AppOpenAd ad) {
    ad.setAdEventListener(
        eventListener: AppOpenAdEventListener(
      onAdShown: () => control.triggerEvent("shown"),
      onAdFailedToShow: (error) =>
          control.triggerEvent("failed_to_show", {"description": error.description}),
      onAdDismissed: () => control.triggerEvent("dismiss"),
      onAdClicked: () => control.triggerEvent("click"),
      onAdImpression: (data) =>
          control.triggerEvent("impression", {"impression_data": data.getRawData()}),
    ));
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "load":
        await _load();
        return null;

      case "show":
        final ad = _ad;
        if (ad == null) return null;
        _attachListener(ad);
        await ad.show();
        return null;

      case "wait_for_dismiss":
        final ad = _ad;
        await ad?.waitForDismiss();
        ad?.destroy();
        _ad = null;
        return null;

      case "cancel_loading":
        _loader.cancelLoading();
        return null;

      case "destroy":
        _ad?.destroy();
        _loader.destroy();
        _ad = null;
        return null;

      default:
        throw Exception("Unknown AppOpenAd method: $name");
    }
  }

  @override
  void dispose() {
    control.removeInvokeMethodListener(_invokeMethod);
    _ad?.destroy();
    _loader.destroy();
    super.dispose();
  }
}
