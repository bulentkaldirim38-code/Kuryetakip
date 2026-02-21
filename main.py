import os
import certifi
import random
from kivy.app import App
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
import requests

os.environ['SSL_CERT_FILE'] = certifi.where()

class KuryeHaritaApp(App):
    def build(self):
        self.base_url = "https://canlikonum-b3b18-default-rtdb.europe-west1.firebasedatabase.app"
        self.my_id = "Kurye_299" 
        
        self.main_layout = FloatLayout()
        
        # 1. Harita
        self.mapview = MapView(zoom=10, lat=38.96, lon=35.24)
        self.main_layout.add_widget(self.mapview)
        
        # 2. Sağ Üst Liste
        self.scroll_view = ScrollView(
            size_hint=(0.4, 0.45),
            pos_hint={'top': 0.98, 'right': 0.98}
        )
        self.user_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.user_list_layout.bind(minimum_height=self.user_list_layout.setter('height'))
        self.scroll_view.add_widget(self.user_list_layout)
        self.main_layout.add_widget(self.scroll_view)

        self.status_label = Label(
            text="Hazır", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.01},
            color=(0, 0, 0, 1), bold=True
        )
        self.main_layout.add_widget(self.status_label)
        
        self.markers = {}
        self.user_coords = {}
        
        Clock.schedule_interval(self.get_data, 5)
        return self.main_layout

    def user_click_action(self, instance):
        name = instance.text.replace("[b][color=#000000]", "").replace("[/color][/b]", "")
        
        if name in self.user_coords:
            coords = self.user_coords[name]
            # ZIPLAMA BURADA: center_on metodunu doğrudan MapView üzerinden çağırıyoruz
            self.mapview.zoom = 15
            self.mapview.center_on(coords['lat'], coords['lon'])
            
            self.status_label.text = f"{name}: Eski konuma zıplandı, yenileniyor..."
            
            # 1 saniye sonra Firebase'den çek ve tekrar zıpla
            Clock.schedule_once(lambda dt: self.refresh_and_jump(name), 1)

    def refresh_and_jump(self, name):
        try:
            res = requests.get(f"{self.base_url}/users/{name}.json", verify=certifi.where(), timeout=5)
            new_data = res.json()
            if new_data:
                # Yeni koordinatlara zıpla
                self.mapview.center_on(new_data['lat'], new_data['lon'])
                self.status_label.text = f"{name}: Güncel konuma zıplandı."
        except:
            self.status_label.text = "Güncelleme sırasında hata!"

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
                    
                    # Markerları haritada güncelle
                    lt, ln = coords.get('lat'), coords.get('lon')
                    if uid in self.markers:
                        self.markers[uid].lat, self.markers[uid].lon = lt, ln
                    else:
                        m = MapMarker(lat=lt, lon=ln)
                        self.mapview.add_widget(m)
                        self.markers[uid] = m
        except: pass

if __name__ == '__main__':
    KuryeHaritaApp().run()
