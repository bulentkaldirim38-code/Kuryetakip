[app]

# (str) Uygulama başlığı
title = Kurye Takip

# (str) Paket adı
package.name = kuryetakip

# (str) Paket alanı
package.domain = org.takip

# (str) main.py dosyasının bulunduğu dizin
source.dir = .

# (list) Dahil edilecek dosya uzantıları
source.include_exts = py,png,jpg,kv,atlas

# (str) Uygulama versiyonu
version = 1.0

# (list) Uygulama gereksinimleri
# NOT: 'mapview' ve 'certifi' Firebase/Harita bağlantısı için kritiktir.
requirements = python3, kivy==2.3.0, mapview, requests, certifi, urllib3, plyer, android

# (str) Desteklenen yön (portrait = dikey)
orientation = portrait

# (bool) Tam ekran modu
fullscreen = 0

# (list) Gerekli Android izinleri
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE

# (int) Hedef Android API (Modern cihazlar için 33 idealdir)
android.api = 33

# (int) Minimum Desteklenen API
android.minapi = 21

# (str) Android NDK sürümü
android.ndk = 25b

# (list) Desteklenen mimariler (Hata riskini azaltmak için arm64-v8a yeterlidir)
android.archs = arm64-v8a

# (bool) AndroidX desteği (Harita kütüphanesi için True olmalı)
android.enable_androidx = True

# (bool) Güvenli olmayan ağ trafiğine izin ver (Firebase bağlantı sorunlarını önler)
android.allow_cleartext = True

# (list) Servisler (Arka planda konum göndermek istersen ileride burası kullanılacak)
# services = KuryeServis:service.py

[buildozer]

# (int) Log seviyesi (2 = debug, tüm hataları detaylı gösterir)
log_level = 2

# (int) Root olarak çalıştırma uyarısı
warn_on_root = 1

# (str) Build dosyalarının saklanacağı dizin
build_dir = ./.buildozer

# (str) APK'nın çıkacağı dizin
bin_dir = ./bin
