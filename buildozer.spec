[app]

# (str) Title of your application
title = Kurye Takip

# (str) Package name
package.name = kuryetakip

# (str) Package domain (needed for android packaging)
package.domain = org.takip

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 1.0

# (list) Application requirements
# ÖNEMLİ: Manuel konum ve SSL bağlantısı için certifi, openssl ve plyer şarttır.
requirements = python3,kivy==2.3.0,kivy_garden.mapview,requests,certifi,openssl,urllib3,plyer,android

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# Konum ve internet erişimi için gerekli izinler
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android NDK directory (if empty, it will be automatically downloaded)
android.ndk_path = 

# (str) Android SDK directory (if empty, it will be automatically downloaded)
android.sdk_path = 

# (list) Android architectures to build for
# Hata payını azaltmak ve derlemeyi hızlandırmak için sadece modern 64-bit mimari
android.archs = arm64-v8a

# (bool) Use --dir for source activation
android.enable_androidx = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# Sadece tek bir mimariyi (arm64-v8a) bırakmak disk alanı hatalarını önler.

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifacts
build_dir = ./.buildozer

# (str) Path to bin directory
bin_dir = ./bin
