[app]

# Uygulama Bilgileri
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.6

# Gereksinimler (Firebase ve Harita için kritik)
requirements = python3, kivy==2.3.0, mapview, requests, certifi, urllib3, plyer, android, openssl

# Ekran ve Görünüm
orientation = portrait
fullscreen = 0

# İzinler (Hassas konum izni eklendi)
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE
android.features = android.hardware.location.gps

# Android SDK / NDK Ayarları
android.api = 33
android.minapi = 21
android.ndk_api = 21

# Mimariler (Hız ve uyumluluk için modern cihaz mimarisi)
android.archs = arm64-v8a

# Ekstra Android Ayarları
android.enable_androidx = True
android.allow_cleartext = True

[buildozer]

# Log seviyesi (Hataları görmek için 2)
log_level = 2
warn_on_root = 1

# Klasör yolları
build_dir = ./.buildozer
bin_dir = ./bin
