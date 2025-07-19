import time

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.clock import Clock
from constants import *


class LogoScreen(Screen):
    record = NumericProperty(0)  # Для автоматического обновления Label


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
        Clock.schedule_once(self.switch_screen, 3)

    def build_ui(self):
        kivy_blue = (BLUE[0] / 255, BLUE[1] / 255, BLUE[2] / 255, 1)
        # Главный контейнер
        main_layout = FloatLayout()

        # Фон для всего экрана
        with main_layout.canvas.before:
            Color(*kivy_blue)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)
        
        layout = BoxLayout(
            orientation='vertical',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.4, 0.4)
                           )
        
        image = Image(source='resources/logo.png', allow_stretch=True, keep_ratio=True)
        label = Label(text=f"trofimovStudio", font_size='20sp', color=BLACK, bold=True)
        
        layout.add_widget(image)
        layout.add_widget(label)
        
        main_layout.add_widget(layout)
        
        self.add_widget(main_layout)
        
        main_layout.bind(
            pos=lambda o, v: setattr(self.bg_rect, 'pos', o.pos),
            size=lambda o, v: setattr(self.bg_rect, 'size', o.size)
        )
        
    def switch_screen(self, dt):
        self.manager.current = 'start'
        
        
        
        