import os
import json
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
from kivy.network.urlrequest import UrlRequest

# Android ve Masaüstü için Dosya Yolu Ayarı
if platform == 'android':
    from android.storage import app_storage_path
    data_dir = app_storage_path()
    from android.permissions import request_permissions, Permission, check_permission
    from plyer import gps
else:
    data_dir = os.getcwd()

class KuryeHaritaApp(App):
    def build(self):
        # Firebase URL (Sonunda '/' olmadığına ve '.app' ile bittiğine emin ol)
        self.base_url = "https://canlikonum-b3b18-default-rtdb.europe-west1.firebasedatabase.app"
        self.id_file = os.path.join(data_dir, "user_name.txt")
        self.my_id = None
        self.is_approved = False 
        
        self.main_layout = FloatLayout()
        self.mapview = MapView(zoom=10, lat=38.96, lon=35.24)
        self.main_layout.add_widget(self.mapview)
        
        self.scroll_view = ScrollView(size_hint=(0.4, 0.45), pos_hint={'top': 0.98, 'right': 0.98})
        self.user_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.user_list_layout.bind(minimum_height=self.user_list_layout.setter('height'))
        self.scroll_view.add_widget(self.user_list_layout)
        self.main_layout.add_widget(self.scroll_view)

        self.status_label = Label(
            text="Bağlantı bekleniyor...", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.01},
            color=(1, 0, 0, 1), bold=True
        )
        self.main_layout.add_widget(self.status_label)
        
        self.markers = {}
        self.user_coords = {}
        return self.main_layout

    def on_start(self):
        # Eğer isim sorma kutusu gelmiyorsa aşağıdaki satırı geçici olarak aktif edebilirsin:
        # if os.path.exists(self.id_file): os.remove(self.id_file)

        if os.path.exists(self.id_file):
            with open(self.id_file, "r") as f:
                self.my_id = f.read().strip()
            self.check_approval_status()
            Clock.schedule_interval(self.get_data, 5)
        else:
            self.show_login_popup()

    def show_login_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Kurye Adınızı Giriniz:"))
        self.name_input = TextInput(text='', multiline=False, hint_text="Örn: Bulent")
        content.add_widget(self.name_input)
        btn = Button(text="Kaydol ve Onay Bekle", size_hint_y=None, height=100, background_color=(0, 0.7, 0, 1))
        content.add_widget(btn)
        self.popup = Popup(title='Giriş Yap', content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        btn.bind(on_release=self.register_user)
        self.popup.open()

    def register_user(self, instance):
        name = self.name_input.text.strip()
        if name:
            self.my_id = name
            with open(self.id_file, "w") as f:
                f.write(self.my_id)
            
            # Firebase'e ilk kayıt (Approved: False)
            params = json.dumps({'lat': 38.96, 'lon': 35.24, 'approved': False})
            UrlRequest(f"{self.base_url}/users/{self.my_id}.json", 
                       req_body=params, method='PUT', 
                       on_success=self.on_register_success)
            
            self.popup.dismiss()
            self.check_approval_status()
            Clock.schedule_interval(self.get_data, 5)

    def on_register_success(self, request, result):
        print("Kullanıcı Firebase'e başarıyla eklendi.")

    def check_approval_status(self, *args):
        if self.my_id:
            UrlRequest(f"{self.base_url}/users/{self.my_id}/approved.json", 
                       on_success=self.on_approval_check)

    def on_approval_check(self, request, result):
        if result is True:
            if not self.is_approved:
                self.is_approved = True
                self.status_label.text = f"ONAYLI: {self.my_id}"
                self.status_label.color = (0, 0.7, 0, 1)
                self.setup_gps()
        else:
            self.is_approved = False
            self.status_label.text = "ADMİN ONAYI BEKLENİYOR..."
            Clock.schedule_once(self.check_approval_status, 10)

    def setup_gps(self):
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
            gps.start(minTime=2000, minDistance=5)
        except: pass

    def my_location_callback(self, **kwargs):
        if self.is_approved and self.my_id:
            lat, lon = kwargs.get('lat'), kwargs.get('lon')
            params = json.dumps({'lat': lat, 'lon': lon, 'approved': True})
            UrlRequest(f"{self.base_url}/users/{self.my_id}.json", req_body=params, method='PUT')

    def get_data(self, dt):
        UrlRequest(f"{self.base_url}/users.json", on_success=self.on_data_success)

    def on_data_success(self, request, result):
        if result and isinstance(result, dict):
            self.user_list_layout.clear_widgets()
            for uid, data in result.items():
                if isinstance(data, dict) and data.get('approved') is True:
                    btn = Button(text=f"[b]{uid}[/b]", markup=True, size_hint_y=None, height=70)
                    btn.bind(on_release=lambda x, u=uid: self.mapview.center_on(result[u]['lat'], result[u]['lon']))
                    self.user_list_layout.add_widget(btn)
                    
                    lt, ln = data.get('lat'), data.get('lon')
                    if uid in self.markers:
                        self.markers[uid].lat, self.markers[uid].lon = lt, ln
                    else:
                        m = MapMarker(lat=lt, lon=ln)
                        self.mapview.add_widget(m)
                        self.markers[uid] = m

if __name__ == '__main__':
    KuryeHaritaApp().run()
