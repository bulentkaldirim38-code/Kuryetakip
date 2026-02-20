import os
import certifi
# SSL hatasını önlemek için bunu en başa koyuyoruz
os.environ['SSL_CERT_FILE'] = certifi.where()

from kivy.app import App
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.utils import platform
from plyer import gps
import requests
import uuid

class KuryeHaritaApp(App):
    def build(self):
        self.store = JsonStore('user_info.json')
        if not self.store.exists('user'):
            yeni_id = str(uuid.uuid4())[:8]
            self.store.put('user', id=yeni_id)
        
        self.my_id = self.store.get('user')['id']
        self.base_url = "https://canlikonum-b3b18-default-rtdb.europe-west1.firebasedatabase.app"
        
        self.layout = BoxLayout(orientation='vertical')
        # İlk açılışta haritayı geniş tutalım
        self.mapview = MapView(zoom=10, lat=36.7850, lon=34.5250)
        self.markers = {} 
        
        self.status_label = Label(
            text=f"ID: {self.my_id} | Baslatiliyor...", 
            size_hint_y=0.1,
            color=(0, 1, 0, 1)
        )

        self.layout.add_widget(self.mapview)
        self.layout.add_widget(self.status_label)
        return self.layout

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION], self.gps_callback)
        else:
            self.start_gps_system()

        Clock.schedule_interval(self.update_from_firebase, 3)

    def gps_callback(self, permissions, results):
        if any(results):
            self.start_gps_system()
        else:
            self.status_label.text = "Konum izni verilmedi!"

    def start_gps_system(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start(minTime=1000, minDistance=0)
        except Exception as e:
            self.status_label.text = "GPS Baslatilamadi"

    def on_location(self, **kwargs):
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        put_url = f"{self.base_url}/users/{self.my_id}.json"
        try:
            # verify=certifi.where() ekleyerek güvenliği sağladık
            requests.put(put_url, json={"lat": lat, "lon": lon}, timeout=5, verify=certifi.where())
        except:
            pass

    def update_from_firebase(self, dt):
        try:
            r = requests.get(f"{self.base_url}/users.json", timeout=5, verify=certifi.where())
            all_users = r.json()
            
            if not all_users:
                self.status_label.text = "Kurye bulunamadi."
                return

            for uid, data in all_users.items():
                if not isinstance(data, dict): continue
                lat, lon = data.get('lat'), data.get('lon')
                
                if lat and lon:
                    if uid in self.markers:
                        self.markers[uid].lat = lat
                        self.markers[uid].lon = lon
                    else:
                        new_marker = MapMarker(lat=lat, lon=lon)
                        self.mapview.add_widget(new_marker)
                        self.markers[uid] = new_marker
                    
                    if uid == self.my_id:
                        self.mapview.center_on(lat, lon)
                        self.status_label.text = f"ID: {self.my_id} | Konum: {lat:.4f}, {lon:.4f}"
        except Exception as e:
            self.status_label.text = "Baglanti Hatasi (SSL/Internet)"

if __name__ == '__main__':
    KuryeHaritaApp().run()
