[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.2

# Requirements listesi GitHub'ı yormamak için en sade haline getirildi
requirements = python3,kivy==2.3.0,cython==0.29.36,pyjnius,requests,certifi,plyer,kivy_garden.mapview

orientation = portrait
fullscreen = 0

# İzinler ve Özellikler
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE
android.features = android.hardware.location.gps, android.hardware.location.network

# Sunucu yükünü azaltmak için API 31 ve NDK 25b sabitlemesi
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a

android.enable_androidx = True
android.allow_cleartext = True

[buildozer]
log_level = 2
warn_on_root = 1
