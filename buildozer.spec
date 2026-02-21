[app]
title = Kurye Canli Takip
package.name = kuryetakip
package.domain = org.canlikonum
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.1

# Gereksinimlerden 'android' ve 'plyer' GPS için şart
requirements = python3, kivy==2.3.0, mapview, requests, certifi, urllib3, plyer, android

orientation = portrait
fullscreen = 0

# İZİNLER: ACCESS_FINE_LOCATION en hassas konum için gereklidir
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE

# GPS Donanım Özelliği
android.features = android.hardware.location.gps

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.enable_androidx = True
android.allow_cleartext = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
