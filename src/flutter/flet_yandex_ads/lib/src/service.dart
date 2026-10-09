import 'package:flet/flet.dart';
import 'package:yandex_mobileads/mobile_ads.dart';

/// Service that initializes the Yandex Mobile Ads SDK and applies SDK-wide
/// settings.
///
/// Privacy flags (user consent, location tracking, age restricted) are read
/// from the control properties and applied *before* initialization, as the
/// SDK requires consent to be set before it initializes.
class YandexAdsService extends FletService {
  YandexAdsService({required super.control});

  bool _initialized = false;

  @override
  void init() {
    super.init();
    control.addInvokeMethodListener(_invokeMethod);
    initializeSdk();
  }

  /// Applies the privacy flags from the control properties.
  Future<void> _applyPrivacyFlags() async {
    final userConsent = control.getBool("user_consent");
    if (userConsent != null) {
      await YandexAds.setUserConsent(userConsent);
    }

    final locationTracking = control.getBool("location_tracking");
    if (locationTracking != null) {
      await YandexAds.setLocationTracking(locationTracking);
    }

    final ageRestricted = control.getBool("age_restricted");
    if (ageRestricted != null) {
      await YandexAds.setAgeRestricted(ageRestricted);
    }

    if (control.getBool("logging", false)!) {
      await YandexAds.setLogging(true);
    }

    if (control.getBool("debug_error_indicator", false)!) {
      await YandexAds.setDebugErrorIndicator(true);
    }
  }

  /// Initializes the SDK (idempotent — the plugin itself guards against
  /// double initialization).
  ///
  /// The success flag is set only after initialize() returns: if it fails,
  /// the flag is reset so a retry can happen, and the failure is surfaced
  /// via the `init_failed` event. (The plugin caches its init future, so
  /// without this the service could hang forever on a poisoned future.)
  Future<void> initializeSdk() async {
    if (_initialized) return;
    try {
      await _applyPrivacyFlags();
      await YandexAds.initialize();
      _initialized = true;
      control.triggerEvent("initialized");
    } catch (e) {
      _initialized = false;
      control.triggerEvent("init_failed", {"description": e.toString()});
    }
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "initialize":
        _initialized = false;
        await initializeSdk();
        return null;

      case "set_user_consent":
        await YandexAds.setUserConsent(args["value"] as bool);
        return null;

      case "set_location_tracking":
        await YandexAds.setLocationTracking(args["value"] as bool);
        return null;

      case "set_age_restricted":
        await YandexAds.setAgeRestricted(args["value"] as bool);
        return null;

      case "show_debug_panel":
        await YandexAds.showDebugPanel();
        return null;

      default:
        throw Exception("Unknown YandexAdsService method: $name");
    }
  }

  @override
  void dispose() {
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
