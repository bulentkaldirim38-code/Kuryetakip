import os
import certifi
import random
from kivy.app import App
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.utils import platform
from plyer import gps
import requests

# SSL Sertifikası - Hem Pydroid hem APK için kritik
os.environ['SSL_CERT_FILE'] = certifi.where()

class KuryeHaritaApp(App):
    def build(self):
        self.base_url = "https://canlikonum-b3b18-default-rtdb.europe-west1.firebasedatabase.app"
        self.my_id = f"Kurye_{random.randint(1000, 9999)}"
        
        self.main_layout = FloatLayout()
        
        # Harita Odaklama (Türkiye Geneli)
        self.mapview = MapView(zoom=6, lat=38.96, lon=35.24)
        self.markers = {}
        self.user_data = {}
        
        # Sağ Üst Köşe - Spinner (Kurye Listesi)
        self.user_spinner = Spinner(
            text='Kurye Seç',
            values=('Bekleniyor...',),
            size_hint=(0.35, 0.07),
            pos_hint={'top': 0.98, 'right': 0.98},
            background_color=(0.1, 0.5, 0.8, 1)
        )
        self.user_spinner.bind(text=self.on_spinner_select)
        
        # Alt Durum Çubuğu
        self.status_label = Label(
            text="Sistem Hazırlanıyor...",
            size_hint=(1, 0.05),
            pos_hint={'x': 0, 'y': 0.01},
            color=(1, 1, 1, 1)
        )

        self.main_layout.add_widget(self.mapview)
        self.main_layout.add_widget(self.user_spinner)
        self.main_layout.add_widget(self.status_label)
        
        return self.main_layout

    def on_start(self):
        # Hata veren izin kısmını try-except içine alıyoruz ve basit tutuyoruz
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                # Callback mekanizması olmadan sadece izinleri talep ediyoruz
                request_permissions([
                    Permission.ACCESS_FINE_LOCATION, 
                    Permission.ACCESS_COARSE_LOCATION
                ])
            except Exception as e:
                print(f"Izin Hatasi: {e}")

        # GPS'i 1 saniye sonra başlat (Hata payını düşürmek için)
        Clock.schedule_once(lambda dt: self.init_gps(), 1)
        # Firebase döngüsü
        Clock.schedule_interval(self.get_data, 3)

    def init_gps(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start(minTime=1000, minDistance=1)
            self.status_label.text = f"ID: {self.my_id} | GPS Aktif"
        except Exception as e:
            self.status_label.text = "GPS Erişimi Yok"

    def on_location(self, **kwargs):
        lat, lon = kwargs.get('lat'), kwargs.get('lon')
        self.status_label.text = f"Konumum: {lat:.4f}, {lon:.4f}"
        
        try:
            requests.put(f"{self.base_url}/users/{self.my_id}.json", 
                         json={'lat': lat, 'lon': lon}, verify=certifi.where(), timeout=5)
        except:
            pass

    def get_data(self, dt):
        try:
            res = requests.get(f"{self.base_url}/users.json", verify=certifi.where(), timeout=5)
            data = res.json()
            if data:
                self.user_data = data
                user_list = []
                for uid, coords in data.items():
                    if not isinstance(coords, dict): continue
                    lt, ln = coords.get('lat'), coords.get('lon')
                    user_list.append(uid)
                    
                    if uid in self.markers:
                        self.markers[uid].lat, self.markers[uid].lon = lt, ln
                    else:
                        m = MapMarker(lat=lt, lon=ln)
                        self.mapview.add_widget(m)
                        self.markers[uid] = m
                self.user_spinner.values = sorted(user_list)
        except:
            pass

    def on_spinner_select(self, spinner, text):
        if text in self.user_data:
            target = self.user_data[text]
            self.mapview.center_on(target.get('lat'), target.get('lon'))
            self.mapview.zoom = 15

if __name__ == '__main__':
    KuryeHaritaApp().run()
