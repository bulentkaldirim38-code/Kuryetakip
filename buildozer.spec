[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Kritik kütüphaneler: openssl ve certifi Firebase için şarttır
requirements = python3,kivy==2.3.0,kivy_garden.mapview,requests,plyer,urllib3,certifi,openssl,android

orientation = portrait
fullscreen = 0

# Gerekli izinler
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# Hata riskini azaltmak için sadece arm64-v8a bırakıldı
android.archs = arm64-v8a

android.enable_androidx = True
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
# (int) Minimum Android API
android.minapi = 21

# (list) Desteklenen mimariler (Modern telefonlar için arm64-v8a şart)
android.archs = arm64-v8a, armeabi-v7a

# (bool) AndroidX desteği (Yeni kütüphaneler için gerekli)
android.enable_androidx = True

# (list) Uygulama ikonları (Varsayılanı kullanmak için boş bırakılabilir)
#icon.filename = %(source.dir)s/data/icon.png

# (str) Log seviyesi (2 = her şeyi göster, hata ayıklama için en iyisi)
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
