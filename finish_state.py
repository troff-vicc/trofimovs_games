from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
import utils
from constants import *

BG_COLOR = get_color_from_hex('#F0FDF5')
WHITE = (1, 1, 1, 1)
TEXT_COLOR_LABEL = get_color_from_hex('#4B5563')
TEXT_COLOR_RECORD = get_color_from_hex('#854D0E')
BUTTON_GREEN = get_color_from_hex('#22C55E')
ORANGE_BG = get_color_from_hex('#FDE047')

Builder.load_string('''
<FinishScreen>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: root.bg_color
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            orientation: 'vertical'
            size_hint: 0.9, None
            height: dp(650)  # Увеличил общую высоту для картинки
            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
            spacing: dp(10)

            # Добавленная картинка кубка
            Image:
                source: 'resources/cup.png'
                size_hint: (None, None)
                size: dp(80), dp(80)
                pos_hint: {'center_x': 0.5}
                allow_stretch: True
                keep_ratio: True

            Label:
                text: 'Поздравляем!'
                font_size: dp(32)
                bold: True
                size_hint_y: None
                height: dp(50)
                color: 0, 0, 0, 1

            Label:
                text: 'Вы успешно решили головоломку!'
                font_size: dp(20)
                size_hint_y: None
                height: dp(40)
                color: root.text_color_label
                halign: 'center'
                valign: 'middle'

            BoxLayout:
                id: main_box
                orientation: 'vertical'
                size_hint_y: None
                height: dp(200)
                padding: [dp(30), dp(30), dp(30), dp(20)]
                spacing: dp(20)
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(15),]

                # Блок времени
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(40)
                    spacing: dp(10)

                    Label:
                        text: 'Время:'
                        font_size: dp(24)
                        color: root.text_color_label
                        size_hint_x: None
                        width: dp(100)
                        halign: 'left'
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: time_label
                        text: '00:00'
                        font_size: dp(24)
                        bold: True
                        color: root.button_green
                        halign: 'right'
                        valign: 'middle'
                        text_size: self.size
                        padding_x: dp(10)

                # Блок ходов
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(40)
                    spacing: dp(10)

                    Label:
                        text: 'Ходы:'
                        font_size: dp(24)
                        color: root.text_color_label
                        size_hint_x: None
                        width: dp(100)
                        halign: 'left'
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: move_label
                        text: '45'
                        font_size: dp(24)
                        bold: True
                        color: root.button_green
                        halign: 'right'
                        valign: 'middle'
                        text_size: self.size
                        padding_x: dp(10)

                Label:
                    id: record_label
                    text: 'Новый рекорд!'
                    font_size: dp(24)
                    size_hint_y: None
                    height: dp(40)
                    color: root.text_color_record
                    canvas.before:
                        Color:
                            rgba: root.orange_bg
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(20),]
                    halign: 'center'
                    valign: 'middle'
                    padding: [dp(10), 0]

            Button:
                text: 'Играть снова'
                bold: True
                font_size: dp(20)
                background_color: 0, 0, 0, 0
                color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(50)
                canvas.before:
                    Color:
                        rgba: root.button_green
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(25),]
                on_press: root.restart_game()
''')

class FinishScreen(Screen):
    bg_color = BG_COLOR
    text_color_label = TEXT_COLOR_LABEL
    text_color_record = TEXT_COLOR_RECORD
    button_green = BUTTON_GREEN
    orange_bg = ORANGE_BG

    moves = NumericProperty(0)
    time_now = NumericProperty(0)

    def on_enter(self, *args):
        seconds = self.manager.time_current
        moves_current = self.manager.moves_current
        """moves_current = 0
        seconds = 10000"""
        minutes = seconds // 60
        seconds_remaining = seconds % 60
        self.ids.time_label.text = f"{minutes:02d}:{seconds_remaining:02d}"
        self.ids.move_label.text = f"{moves_current}"
        record_time = utils.Logs().record['time_seconds']
        if seconds>record_time:
            minutes_r = record_time // 60
            seconds_remaining_r = record_time % 60
            self.ids.record_label.text = f"Рекорд {minutes_r:02d}:{seconds_remaining_r:02d}"


    def restart_game(self):
        self.manager.current = "start"
