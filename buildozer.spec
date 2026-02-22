[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.0

requirements = python3,kivy==2.3.0,kivy_garden.mapview,requests,certifi,urllib3,plyer

orientation = portrait
fullscreen = 0

# İzinler
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE
android.features = android.hardware.location.gps

android.api = 33
android.minapi = 21
# Modern cihazlar için 64-bit mimari
android.archs = arm64-v8a

android.enable_androidx = True
android.allow_cleartext = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
