[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html
version = 2.2

# Gereksinimler (Kivy_garden.mapview kurulumu için en güvenli yol)
requirements = python3,kivy==2.3.0,requests,certifi,plyer,kivy-garden,kivy_garden.mapview

orientation = portrait
fullscreen = 0

# İzinler
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE
android.features = android.hardware.location.gps, android.hardware.location.network

# SDK ve NDK Ayarları (GitHub için en stabil versiyonlar)
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.skip_update = False

# Mimari (Hem yeni hem eski telefonlar için)
android.archs = arm64-v8a, armeabi-v7a

android.enable_androidx = True
android.allow_cleartext = True

[buildozer]
log_level = 2
warn_on_root = 1
