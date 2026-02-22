[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.1

# Gereksiz ağır paketleri (sqlite3, openssl) çıkardım, derleme hızlanacak
requirements = python3,kivy==2.3.0,cython==0.29.36,pyjnius,requests,certifi,urllib3,plyer,kivy_garden.mapview

orientation = portrait
fullscreen = 0

# Hassas konum izinleri
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE
android.features = android.hardware.location.gps, android.hardware.location.network

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a

android.enable_androidx = True
android.allow_cleartext = True

[buildozer]
log_level = 2
warn_on_root = 1
