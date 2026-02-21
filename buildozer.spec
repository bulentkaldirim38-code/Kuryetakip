[app]

# (str) Uygulama başlığı
title = Kurye Takip

# (str) Paket adı ve alanı
package.name = kuryetakip
package.domain = org.takip

# (str) Kaynak kod dizini
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (str) Uygulama versiyonu (Hata alırsanız bunu artırın)
version = 1.2

# (list) Uygulama gereksinimleri
# openssl ve certifi Firebase bağlantısı için eklendi.
requirements = python3, kivy==2.3.0, mapview, requests, certifi, urllib3, plyer, android, openssl

# (str) Oryantasyon
orientation = portrait

# (list) Gerekli Android izinleri
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE

# (int) Hedef Android API
android.api = 33
android.minapi = 21

# (str) NDK Sürümü (GitHub Actions için boş bırakmak daha güvenlidir)
# android.ndk = 25b

# (list) Mimari (Hata riskini azaltmak için en yaygın olanlar)
android.archs = arm64-v8a, armeabi-v7a

# (bool) AndroidX desteği
android.enable_androidx = True

# (bool) HTTPS/SSL dışı trafiğe izin ver
android.allow_cleartext = True

# (list) Özellikler
android.features = android.hardware.location.gps

[buildozer]

# (int) Log seviyesi (Hata ayıklama için 2 kalsın)
log_level = 2

# (int) Root uyarısı
warn_on_root = 1

# (str) Build dizinleri
build_dir = ./.buildozer
bin_dir = ./bin
