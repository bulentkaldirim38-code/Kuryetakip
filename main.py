import os
import certifi
import random
from kivy.app import App
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.vboxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from plyer import gps
import requests

os.environ['SSL_CERT_FILE'] = certifi.where()

class KuryeHaritaApp(App):
    def build(self):
        self.base_url = "https://canlikonum-b3b18-default-rtdb.europe-west1.firebasedatabase.app"
        # Her cihaz için sabit ama rastgele bir ID (Uygulama silinene kadar değişmez önerilir)
        self.my_id = f"Kurye_{random.randint(100, 999)}"
        
        self.main_layout = FloatLayout()
        
        # 1. Harita
        self.mapview = MapView(zoom=10, lat=38.96, lon=35.24)
        self.markers = {}
        self.user_coords = {}

        # 2. Sağ Üst Kullanıcı Listesi (Scroll edilebilir alt alta butonlar)
        self.scroll_view = ScrollView(
            size_hint=(0.3, 0.4),
            pos_hint={'top': 0.98, 'right': 0.98}
        )
        self.user_list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.user_list_layout.bind(minimum_height=self.user_list_layout.setter('height'))
        self.scroll_view.add_widget(self.user_list_layout)

        # 3. Alt Durum Çubuğu
        self.status_label = Label(
            text=f"ID'niz: {self.my_id} | Listeden isminize basarak konum gönderin",
            size_hint=(1, 0.05),
            pos_hint={'x': 0, 'y': 0},
            color=(1, 1, 1, 1)
        )

        self.main_layout.add_widget(self.mapview)
        self.main_layout.add_widget(self.scroll_view)
        self.main_layout.add_widget(self.status_label)
        
        # Firebase'den diğerlerini çekme döngüsü (Otomatik devam eder)
        Clock.schedule_interval(self.get_data, 5)
        
        return self.main_layout

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION])

    def user_click_action(self, instance):
        user_name = instance.text
        
        if user_name == self.my_id:
            # EĞER KENDİ İSMİNE BASTIYSA: GPS AL VE GÖNDER
            self.status_label.text = "GPS Alınıyor..."
            try:
                gps.configure(on_location=self.my_location_callback)
                gps.start(minTime=100, minDistance=0) # Tek seferlik hızlı veri
                Clock.schedule_once(lambda dt: gps.stop(), 5) # 5 sn sonra GPS kapat (pil dostu)
            except Exception as e:
                self.status_label.text = "GPS Hatası!"
        else:
            # BAŞKASINA BASTIYSA: SON KONUMUNA ZIPLA
            if user_name in self.user_coords:
                lat = self.user_coords[user_name]['lat']
                lon = self.user_coords[user_name]['lon']
                self.mapview.center_on(lat, lon)
                self.mapview.zoom = 15
                self.status_label.text = f"{user_name} konumuna odaklanıldı."

    def my_location_callback(self, **kwargs):
        lat, lon = kwargs.get('lat'), kwargs.get('lon')
        self.status_label.text = f"Konum Gönderildi: {lat:.4f}, {lon:.4f}"
        self.mapview.center_on(lat, lon)
        
        # Firebase'e Manuel Gönderim
        try:
            requests.put(f"{self.base_url}/users/{self.my_id}.json", 
                         json={'lat': lat, 'lon': lon}, verify=certifi.where(), timeout=5)
        except:
            self.status_label.text = "Firebase Yazma Hatası!"

    def get_data(self, dt):
        try:
            res = requests.get(f"{self.base_url}/users.json", verify=certifi.where(), timeout=5)
            data = res.json()
            if data:
                self.user_coords = data
                self.user_list_layout.clear_widgets() # Listeyi temizle ve yeniden oluştur
                
                for uid, coords in data.items():
                    if not isinstance(coords, dict): continue
                    
                    # 1. Buton Listesine Ekle
                    btn = Button(text=uid, size_hint_y=None, height=40, 
                                 background_color=(0.2, 0.2, 0.2, 0.8) if uid != self.my_id else (0, 0.7, 0, 1))
                    btn.bind(on_release=self.user_click_action)
                    self.user_list_layout.add_widget(btn)
                    
                    # 2. Haritada Marker Güncelle
                    lt, ln = coords.get('lat'), coords.get('lon')
                    if uid in self.markers:
                        self.markers[uid].lat, self.markers[uid].lon = lt, ln
                    else:
                        m = MapMarker(lat=lt, lon=ln)
                        self.mapview.add_widget(m)
                        self.markers[uid] = m
        except:
            self.status_label.text = "Veri Çekme Hatası!"

if __name__ == '__main__':
    KuryeHaritaApp().run()
