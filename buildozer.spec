[app]
title = Kurye Takip
package.name = kuryetakip
package.domain = org.takip
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Gereksinimler (Firebase ve Harita için gerekli olanlar)
requirements = python3,kivy==2.3.0,kivy_garden.mapview,requests,plyer,urllib3,certifi,openssl,android

orientation = portrait
fullscreen = 0

# İzinler
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# Sadece modern telefon mimarisi (Derlemeyi hızlandırır ve hatayı azaltır)
android.archs = arm64-v8a

android.enable_androidx = True

[buildozer]
# log_level BURADA SADECE BİR KEZ TANIMLANMALIDIR
log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
