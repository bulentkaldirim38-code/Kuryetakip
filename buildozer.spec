[app]

# (str) Uygulamanın adı
title = Kurye Takip

# (str) Paket adı (boşluk ve özel karakter içermemeli)
package.name = kuryetakip

# (str) Paket domaini
package.domain = org.takip

# (str) Kaynak kodlarının olduğu dizin
source.dir = .

# (list) Dahil edilecek dosya uzantıları
source.include_exts = py,png,jpg,kv,atlas

# (str) Uygulama versiyonu
version = 1.0

# (list) Uygulamanın çalışması için gereken kütüphaneler (KRİTİK BÖLÜM)
# openssl ve certifi olmazsa Firebase bağlantısı APK'da çalışmaz!
requirements = python3,kivy,kivy_garden.mapview,requests,plyer,urllib3,certifi,openssl,android

# (str) Ekran yönü (portrait, landscape veya all)
orientation = portrait

# (bool) Tam ekran modu
fullscreen = 0

# (list) Android İzinleri (GPS ve İnternet için şart)
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, ACCESS_NETWORK_STATE

# (int) Hedef Android API (Genelde 31 veya 33 idealdir)
android.api = 33

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

# (int) Log seviyesi
log_level = 2

# (int) Root olarak çalıştırma uyarısı (Colab'da kullanırken 1 olmalı)
warn_on_root = 1

# (str) Build dizini
build_dir = ./.buildozer

# (str) Bin dizini (APK buraya çıkacak)
bin_dir = ./bin
