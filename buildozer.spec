[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# SSL ve Harita için gerekli tüm kütüphaneler buraya eklendi
requirements = python3,kivy==2.3.0,kivy_garden.mapview,requests,certifi,openssl,urllib3,plyer,android

orientation = portrait
fullscreen = 0

# Gerekli tüm Android izinleri
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b

# Tek mimari seçimi (Hata payını azaltır)
android.archs = arm64-v8a
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
