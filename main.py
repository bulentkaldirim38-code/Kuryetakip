import os
import json
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

class KuryeHaritaApp(App):
    def build(self):
        # 1. Firebase URL (Sonunda / olmamasına dikkat edin)
        self.base_url = "https://canlikonum-b3b18-default-rtdb.europe-west1.firebasedatabase.app"
        
        # 2. Güvenli Dosya Yolu (Pydroid ve APK için en garantisi)
        self.data_dir = self.user_data_dir
        self.id_file = os.path.join(self.data_dir, "user_name.txt")
        
        self.my_id = None
        self.is_approved = False 
        
        self.main_layout = FloatLayout()
        self.mapview = MapView(zoom=10, lat=38.96, lon=35.24)
        self.main_layout.add_widget(self.mapview)
        
        # Kullanıcı Listesi
        self.scroll_view = ScrollView(size_hint=(0.4, 0.45), pos_hint={'top': 0.98, 'right': 0.98})
        self.user_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.user_list_layout.bind(minimum_height=self.user_list_layout.setter('height'))
        self.scroll_view.add_widget(self.user_list_layout)
        self.main_layout.add_widget(self.scroll_view)

        # Durum Çubuğu (Hataları buradan göreceğiz)
        self.status_label = Label(
            text="Başlatılıyor...", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.01},
            color=(1, 1, 1, 1), bold=True
        )
        self.main_layout.add_widget(self.status_label)
        
        self.markers = {}
        return self.main_layout

    def on_start(self):
        # Her zaman veri çekmeye başla
        Clock.schedule_interval(self.get_data, 5)
        
        # Dosya ve İsim Kontrolü
        if os.path.exists(self.id_file):
            with open(self.id_file, "r") as f:
                self.my_id = f.read().strip()
            
            if self.my_id:
                self.status_label.text = f"Giriş: {self.my_id}"
                self.check_approval_status()
            else:
                self.show_login_popup()
        else:
            self.show_login_popup()

    def show_login_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Kurye Adınızı Giriniz:"))
        self.name_input = TextInput(text='', multiline=False, hint_text="Örn: bulent")
        content.add_widget(self.name_input)
        
        btn = Button(text="Kaydol ve Onay Bekle", size_hint_y=None, height=100)
        content.add_widget(btn)
        
        self.popup = Popup(title='Giriş Yap', content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        btn.bind(on_release=self.register_user)
        self.popup.open()

    def register_user(self, instance):
        name = self.name_input.text.strip().lower()
        if name:
            self.my_id = name
            try:
                # Dosyayı oluştur ve ismi yaz
                with open(self.id_file, "w") as f:
                    f.write(self.my_id)
                
                # Firebase'e gönder
                params = json.dumps({'lat': 0, 'lon': 0, 'approved': False})
                UrlRequest(
                    f"{self.base_url}/users/{self.my_id}.json", 
                    req_body=params, 
                    method='PUT',
                    on_success=self.on_register_success,
                    on_error=self.on_net_error,
                    on_failure=self.on_net_error
                )
                self.popup.dismiss()
            except Exception as e:
                self.status_label.text = f"Dosya Yazılamadı: {e}"

    def on_register_success(self, req, res):
        self.status_label.text = "Kayıt Başarılı. Onay Bekleniyor..."
        self.check_approval_status()

    def check_approval_status(self, *args):
        if self.my_id:
            UrlRequest(
                f"{self.base_url}/users/{self.my_id}/approved.json", 
                on_success=self.on_approval_check,
                on_error=self.on_net_error
            )

    def on_approval_check(self, request, result):
        if result is True:
            self.is_approved = True
            self.status_label.text = f"AKTİF: {self.my_id.upper()}"
            self.status_label.color = (0, 1, 0, 1)
            self.setup_gps() # Onay gelince GPS'e geç
        else:
            self.status_label.text = "ADMİN ONAYI BEKLENİYOR..."
            Clock.schedule_once(self.check_approval_status, 10)

    def setup_gps(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission, check_permission
            perms = [Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION]
            if all([check_permission(p) for p in perms]):
                self.start_gps_logic()
            else:
                request_permissions(perms, self.permission_callback)
        else:
            self.start_gps_logic()

    def permission_callback(self, permissions, results):
        if all(results):
            self.start_gps_logic()
        else:
            self.status_label.text = "Konum İzni Reddedildi!"

    def start_gps_logic(self):
        try:
            from plyer import gps
            gps.configure(on_location=self.my_location_callback)
            gps.start(minTime=2000, minDistance=1)
            self.status_label.text = "Takip Başlatıldı"
        except Exception as e:
            self.status_label.text = "GPS Başlatılamadı!"

    def my_location_callback(self, **kwargs):
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        if self.is_approved and self.my_id and lat:
            params = json.dumps({'lat': lat, 'lon': lon, 'approved': True})
            UrlRequest(
                f"{self.base_url}/users/{self.my_id}.json", 
                req_body=params, 
                method='PUT'
            )

    def on_net_error(self, req, error):
        self.status_label.text = f"Bağlantı Hatası: {error}"

    def get_data(self, dt):
        UrlRequest(f"{self.base_url}/users.json", on_success=self.on_data_success)

    def on_data_success(self, request, result):
        if not result or not isinstance(result, dict): return
        self.user_list_layout.clear_widgets()
        for uid, data in result.items():
            if isinstance(data, dict) and data.get('approved'):
                lat, lon = data.get('lat'), data.get('lon')
                if lat and lat != 0:
                    btn = Button(text=f"{uid.upper()}", size_hint_y=None, height=60)
                    btn.bind(on_release=lambda x, u=uid, la=lat, lo=lon: self.mapview.center_on(la, lo))
                    self.user_list_layout.add_widget(btn)
                    
                    if uid in self.markers:
                        self.markers[uid].lat, self.markers[uid].lon = lat, lon
                    else:
                        m = MapMarker(lat=lat, lon=lon)
                        self.mapview.add_widget(m)
                        self.markers[uid] = m

if __name__ == '__main__':
    KuryeHaritaApp().run()
