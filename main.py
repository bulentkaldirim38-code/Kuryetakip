import os
import certifi # SSL için şart
from kivy.app import App
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from plyer import gps
import requests

# SSL sertifikasını Android'e tanıtıyoruz
os.environ['SSL_CERT_FILE'] = certifi.where()

class KuryeHaritaApp(App):
    def build(self):
        self.base_url = "https://canlikonum-b3b18-default-rtdb.europe-west1.firebasedatabase.app"
        self.my_id = "kurye_1" 
        
        self.layout = BoxLayout(orientation='vertical')
        # İlk açılışta boşluk olmaması için Türkiye üzerine odaklıyoruz
        self.mapview = MapView(zoom=10, lat=36.8, lon=34.6)
        self.markers = {}
        
        self.status_label = Label(text="Sistem Hazırlanıyor...", size_hint_y=0.1)
        
        self.layout.add_widget(self.mapview)
        self.layout.add_widget(self.status_label)
        return self.layout

    def on_start(self):
        # Android İzinleri
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.ACCESS_FINE_LOCATION, 
                                 Permission.ACCESS_COARSE_LOCATION, 
                                 Permission.INTERNET]) # İnternet iznini buradan da istiyoruz
        
        try:
            gps.configure(on_location=self.on_location)
            gps.start(minTime=1000, minDistance=1)
        except:
            self.status_label.text = "GPS Başlatılamadı"

        Clock.schedule_interval(self.get_data_from_firebase, 5)

    def on_location(self, **kwargs):
        lat, lon = kwargs.get('lat'), kwargs.get('lon')
        self.status_label.text = f"Konumum: {lat:.4f}, {lon:.4f}"
        
        try:
            # verify=certifi.where() ekleyerek güvenli bağlantıyı zorluyoruz
            requests.put(f"{self.base_url}/users/{self.my_id}.json", 
                         json={'lat': lat, 'lon': lon}, 
                         timeout=5, 
                         verify=certifi.where())
        except Exception as e:
            self.status_label.text = "Veri gönderilemedi!"

    def get_data_from_firebase(self, dt):
        try:
            res = requests.get(f"{self.base_url}/users.json", timeout=5, verify=certifi.where())
            data = res.json()
            if data:
                for uid, coords in data.items():
                    if not isinstance(coords, dict): continue
                    lat, lon = coords.get('lat'), coords.get('lon')
                    if lat and lon:
                        if uid in self.markers:
                            self.markers[uid].lat = lat
                            self.markers[uid].lon = lon
                        else:
                            new_marker = MapMarker(lat=lat, lon=lon)
                            self.mapview.add_widget(new_marker)
                            self.markers[uid] = new_marker
        except:
            self.status_label.text = "Bağlantı Hatası!"

if __name__ == '__main__':
    KuryeHaritaApp().run()
