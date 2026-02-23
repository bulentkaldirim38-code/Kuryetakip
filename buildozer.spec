[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html
version = 2.2

# [span_1](start_span)mapview'in çalışması için sqlite3 ve openssl eklenmesi zorunludur[span_1](end_span)
requirements = python3,kivy==2.3.0,requests,certifi,plyer,sqlite3,openssl,kivy_garden.mapview

orientation = portrait
fullscreen = 0

# İzinler
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE
android.features = android.hardware.location.gps, android.hardware.location.network

# SDK ve NDK (API 33, Google Play uyumluluğu için önerilir)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.skip_update = False

# Mimari
android.archs = arm64-v8a, armeabi-v7a

android.enable_androidx = True
android.allow_cleartext = True

[buildozer]
log_level = 2
warn_on_root = 1
