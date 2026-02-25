# cython: language_level=3
import os
import certifi
import json
import urllib.parse
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock, mainthread
from kivy.utils import platform
from kivy.network.urlrequest import UrlRequest

# SSL Sertifikası - Firebase için kritik
os.environ['SSL_CERT_FILE'] = certifi.where()

try:
    from kivy_garden.mapview import MapView, MapMarker
except ImportError:
    MapView = None

class KuryeHaritaApp(App):
    def build(self):
        self.base_url = "https://canlikonum-b3b18-default-rtdb.europe-west1.firebasedatabase.app"
        self.id_file = os.path.join(self.user_data_dir, "user_name.txt")
        self.my_id = None
        self.is_approved = False 
        self.markers = {}
        self.last_lat = None
        self.last_lon = None

        self.main_layout = FloatLayout()
        self.mapview = MapView(zoom=10, lat=38.96, lon=35.24)
        self.main_layout.add_widget(self.mapview)
        
        self.scroll_view = ScrollView(size_hint=(0.4, 0.45), pos_hint={'top': 0.98, 'right': 0.98})
        self.user_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.user_list_layout.bind(minimum_height=self.user_list_layout.setter('height'))
        self.scroll_view.add_widget(self.user_list_layout)
        self.main_layout.add_widget(self.scroll_view)

        self.status_label = Label(
            text="Başlatılıyor...", size_hint=(1, 0.12), 
            pos_hint={'x': 0, 'y': 0},
            color=(1, 1, 1, 1), bold=True,
            outline_width=2, outline_color=(0,0,0,1)
        )
        self.main_layout.add_widget(self.status_label)
        return self.main_layout

    def on_start(self):
        Clock.schedule_interval(self.get_data, 5)
        if os.path.exists(self.id_file):
            with open(self.id_file, "r") as f:
                self.my_id = f.read().strip()
            if self.my_id: self.check_approval_status()
            else: self.show_login_popup()
        else: self.show_login_popup()

    def check_approval_status(self, *args):
        if self.my_id:
            safe_id = urllib.parse.quote(self.my_id)
            UrlRequest(f"{self.base_url}/users/{safe_id}/approved.json", on_success=self.on_approval_check)

    def on_approval_check(self, request, result):
        if result is True:
            self.is_approved = True
            self.status_label.text = "Onaylı: Hibrit Konum Aranıyor..."
            # GPS'i başlatırken aynı zamanda Ağ üzerinden hızlı konum alalım
            self.get_network_location() 
            self.setup_gps()
        else:
            self.status_label.text = "Onay Bekleniyor..."
            Clock.schedule_once(self.check_approval_status, 10)

    def get_network_location(self):
        """GPS uydusu beklenirken Wi-Fi/Baz istasyonu (IP tabanlı) hızlı konum alır"""
        UrlRequest("http://ip-api.com/json", on_success=self.on_network_ok)

    def on_network_ok(self, req, res):
        # Eğer GPS henüz veri üretmediyse, Wi-Fi konumunu kullan
        if self.last_lat is None:
            lat, lon = res.get('lat'), res.get('lon')
            self.status_label.text = "Wi-Fi/Ağ Konumu Alındı"
            self.send_to_firebase(lat, lon)

    def setup_gps(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.ACCESS_FINE_LOCATION, 
                Permission.ACCESS_COARSE_LOCATION,
                Permission.ACCESS_BACKGROUND_LOCATION
            ], self.start_gps_logic)
        else:
            self.start_gps_logic()

    def start_gps_logic(self, *args):
        try:
            from plyer import gps
            # Hem GPS hem Network provider'ı kullanması için konfigüre edilir
            gps.configure(on_location=self.my_location_callback)
            gps.start(minTime=1000, minDistance=0)
        except Exception as e:
            self.status_label.text = f"GPS Başlatılamadı: {e}"

    @mainthread
    def my_location_callback(self, **kwargs):
        self.last_lat, self.last_lon = kwargs.get('lat'), kwargs.get('lon')
        self.status_label.text = f"GPS Konumu: {self.last_lat}, {self.last_lon}"
        self.send_to_firebase(self.last_lat, self.last_lon)

    def send_to_firebase(self, lat, lon):
        if self.is_approved and self.my_id and lat:
            params = json.dumps({'lat': lat, 'lon': lon, 'approved': True})
            headers = {'Content-type': 'application/json'}
            safe_id = urllib.parse.quote(self.my_id)
            UrlRequest(f"{self.base_url}/users/{safe_id}.json", req_body=params, req_headers=headers, method='PUT')

    def get_data(self, dt):
        UrlRequest(f"{self.base_url}/users.json", on_success=self.on_data_success)

    @mainthread
    def on_data_success(self, request, result):
        if not result or not isinstance(result, dict): return
        self.user_list_layout.clear_widgets()
        for uid, data in result.items():
            if isinstance(data, dict) and data.get('approved'):
                lat, lon = data.get('lat'), data.get('lon')
                if lat:
                    btn = Button(text=uid.upper(), size_hint_y=None, height=60)
                    btn.bind(on_release=lambda x, la=lat, lo=lon: self.mapview.center_on(la, lo))
                    self.user_list_layout.add_widget(btn)
                    if uid in self.markers:
                        self.markers[uid].lat, self.markers[uid].lon = lat, lon
                    else:
                        m = MapMarker(lat=lat, lon=lon)
                        self.mapview.add_widget(m)
                        self.markers[uid] = m

    def show_login_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Kurye Adı:"))
        self.name_input = TextInput(multiline=False)
        content.add_widget(self.name_input)
        btn = Button(text="Kaydet", size_hint_y=None, height=100)
        content.add_widget(btn)
        self.popup = Popup(title='Giriş', content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        btn.bind(on_release=self.register_user)
        self.popup.open()

    def register_user(self, instance):
        name = self.name_input.text.strip().lower()
        if name:
            self.my_id = name
            with open(self.id_file, "w") as f: f.write(self.my_id)
            self.popup.dismiss()
            self.check_approval_status()

if __name__ == '__main__':
    KuryeHaritaApp().run()
