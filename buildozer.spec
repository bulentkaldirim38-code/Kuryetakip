[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,json
version = 2.2

requirements = python3,kivy==2.3.0,kivy_garden.mapview,requests,certifi,plyer,pyjnius

orientation = portrait
fullscreen = 0

# Wi-Fi ve Baz istasyonu için COARSE_LOCATION ve NETWORK izinleri şarttır
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,FOREGROUND_SERVICE,POST_NOTIFICATIONS

android.api = 33
android.minapi = 21
android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a
android.enable_androidx = True
