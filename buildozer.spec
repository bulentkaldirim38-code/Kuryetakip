[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# ÖNEMLİ: Yeni eklenen Spinner ve SSL desteği için bu liste tam olmalı
requirements = python3,kivy==2.3.0,kivy_garden.mapview,requests,certifi,openssl,urllib3,plyer,android

orientation = portrait
fullscreen = 0

# İzinler (ACCESS_NETWORK_STATE eklendi)
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b

# Sadece 64-bit mimari (Hata riskini en aza indirir)
android.archs = arm64-v8a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
