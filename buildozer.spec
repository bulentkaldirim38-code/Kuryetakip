[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html
version = 2.2

# requirements'i güncelleyin
requirements = python3,kivy==2.3.0,cython==0.29.33,requests,certifi,plyer,jnius,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.features = android.hardware.location.gps,android.hardware.location.network

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.skip_update = False

android.archs = arm64-v8a,armeabi-v7a

android.enable_androidx = True
android.allow_cleartext = True

# Kivy garden mapview için
p4a.source_dir = 
p4a.local_recipes = ./recipes
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
