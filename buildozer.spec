[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.5

requirements = python3, kivy==2.3.0, mapview, requests, certifi, urllib3, plyer, android, openssl

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE
android.features = android.hardware.location.gps

android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True
android.allow_cleartext = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
