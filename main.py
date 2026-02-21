import os
import certifi
import requests
import random
import sys
from kivy.app import App
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.utils import platform

# --- HATA YAKALAMA VE DOSYA YOLU AYARI ---
if platform == 'android':
    from android.storage import app_storage_path
    data_dir = app_storage_path()
else:
    data_dir = os.getcwd()

report_path = os.path.join(data_dir, "HATA_RAPORU.txt")
sys.stderr = open(report_path, "w") # Hataları dosyaya yazar

# SSL ve Android İzinleri
if platform == 'android':
    from android.permissions import request_permissions, Permission, check_permission
    from plyer import gps

os.environ['SSL_CERT_FILE'] = certifi.where()

class KuryeHaritaApp(App):
    def build(self):
        self.base_url = "https://canlikonum-b3b18-default-rtdb.europe-west1.firebasedatabase.app"
        # İsim dosyasını güvenli yere kaydet
        self.id_file = os.path.join(data_dir, "user_name.txt")
        self.my_id = None
        
        self.main_layout = FloatLayout()
        self.mapview = MapView(zoom=10, lat=38.96, lon=35.24)
        self.main_layout.add_widget(self.mapview)
        
        self.scroll_view = ScrollView(size_hint=(0.4, 0.45), pos_hint={'top': 0.98, 'right': 0.98})
        self.user_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.user_list_layout.bind(minimum_height=self.user_list_layout.setter('height'))
        self.scroll_view.add_widget(self.user_list_layout)
        self.main_layout.add_widget(self.scroll_view)

        self.status_label = Label(
            text="Giriş bekleniyor...", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.01},
            color=(0, 0, 0, 1), bold=True
        )
        self.main_layout.add_widget(self.status_label)
        
        self.markers = {}
        self.user_coords = {}
        return self.main_layout

    def on_start(self):
        if os.path.exists(self.id_file):
            with open(self.id_file, "r") as f:
                self.my_id = f.read().strip()
            self.setup_app_logic()
        else:
            self.show_login_popup()

    def show_login_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Kurye Adınızı Giriniz:"))
        self.name_input = TextInput(text='', multiline=False, hint_text="Örn: Ahmet_299")
        content.add_widget(self.name_input)
        btn = Button(text="Tamam", size_hint_y=None, height=100, background_color=(0, 0.7, 0, 1))
        content.add_widget(btn)
        self.popup = Popup(title='Giriş Yap', content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        btn.bind(on_release=self.save_name_and_start)
        self.popup.open()

    def save_name_and_start(self, instance):
        name = self.name_input.text.strip()
        if name:
            self.my_id = name
            with open(self.id_file, "w") as f:
                f.write(self.my_id)
            self.popup.dismiss()
            self.setup_app_logic()

    def setup_app_logic(self):
        self.status_label.text = f"Hoş geldin, {self.my_id}"
        Clock.schedule_interval(self.get_data, 5)
        if platform == 'android':
            permissions = [Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION]
            if all([check_permission(p) for p in permissions]):
                self.start_gps_logic()
            else:
                request_permissions(permissions, self.permission_callback)
        else:
            self.my_location_callback(lat=38.96, lon=35.24)

    def permission_callback(self, permissions, results):
        if all(results): self.start_gps_logic()

    def start_gps_logic(self):
        try:
            gps.configure(on_location=self.my_location_callback)
            gps.start(minTime=1000, minDistance=1)
        except: pass

    def my_location_callback(self, **kwargs):
        lat, lon = kwargs.get('lat'), kwargs.get('lon')
        if self.my_id and lat and lon:
            try:
                requests.put(f"{self.base_url}/users/{self.my_id}.json",
                             json={'lat': lat, 'lon': lon}, verify=certifi.where(), timeout=5)
            except Exception as e:
                print(f"Hata: {e}") # Bu hata HATA_RAPORU.txt'ye gider

    def user_click_action(self, instance):
        name = instance.text.replace("[b][color=#000000]", "").replace("[/color][/b]", "")
        if name in self.user_coords:
            coords = self.user_coords[name]
            self.mapview.center_on(coords['lat'], coords['lon'])
            self.mapview.zoom = 15
            Clock.schedule_once(lambda dt: self.refresh_and_jump(name), 1)

    def refresh_and_jump(self, name):
        try:
            res = requests.get(f"{self.base_url}/users/{name}.json", verify=certifi.where(), timeout=5)
            new_data = res.json()
            if new_data:
                self.mapview.center_on(new_data['lat'], new_data['lon'])
        except: pass

    def get_data(self, dt):
        try:
            res = requests.get(f"{self.base_url}/users.json", verify=certifi.where(), timeout=5)
            data = res.json()
            if data:
                self.user_coords = data
                self.user_list_layout.clear_widgets()
                for uid, coords in data.items():
                    if not isinstance(coords, dict): continue
                    is_me = (uid == self.my_id)
                    btn = Button(
                        text=f"[b][color=#000000]{uid}[/color][/b]",
                        markup=True, size_hint_y=None, height=60,
                        background_normal='',
                        background_color=(0, 0.9, 0, 1) if is_me else (0.9, 0.9, 0.9, 1)
                    )
                    btn.bind(on_release=self.user_click_action)
                    self.user_list_layout.add_widget(btn)
                    
                    lt, ln = coords.get('lat'), coords.get('lon')
                    if uid in self.markers:
                        self.markers[uid].lat, self.markers[uid].lon = lt, ln
                    else:
                        m = MapMarker(lat=lt, lon=ln)
                        self.mapview.add_widget(m)
                        self.markers[uid] = m
        except: pass

    def on_stop(self):
        sys.stderr.close() # Uygulama kapanınca log dosyasını kapat

if __name__ == '__main__':
    KuryeHaritaApp().run()
