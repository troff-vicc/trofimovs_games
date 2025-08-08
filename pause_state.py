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
TEXT_COLOR_VALUE = get_color_from_hex('#1F2937')
BUTTON_BLUE = (0.2, 0.6, 0.9, 1)
BUTTON_GRAY = get_color_from_hex('#6B7280')
GRAY_BG = get_color_from_hex('#F9FAFB')

Builder.load_string('''
<PauseScreen>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: root.bg_color
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            id: main_box
            orientation: 'vertical'
            size_hint: 0.9, 0.5
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            padding: dp(30)
            spacing: dp(20)
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(15),]

            Label:
                text: 'Пауза'
                font_size: dp(32)
                bold: True
                size_hint_y: None
                height: dp(50)
                color: 0, 0, 0, 1

            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(110)
                spacing: dp(10)
                padding: dp(15)
                canvas.before:
                    Color:
                        rgba: root.gray_bg
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(10),]

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(40)

                    Label:
                        text: 'Время:'
                        font_size: dp(24)
                        color: root.text_color_label
                        size_hint_x: None
                        width: dp(100)

                    Label:
                        id: time_label
                        text: '00:00'
                        font_size: dp(24)
                        color: root.text_color_value

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(40)

                    Label:
                        text: 'Ходы:'
                        font_size: dp(24)
                        color: root.text_color_label
                        size_hint_x: None
                        width: dp(100)

                    Label:
                        id: move_label
                        text: '45'
                        font_size: dp(24)
                        color: root.text_color_value

            Widget:

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(15)
                size_hint_y: None
                height: dp(120)

                Button:
                    text: 'Продолжить'
                    bold: True
                    font_size: dp(20)
                    background_color: 0, 0, 0, 0
                    color: 1, 1, 1, 1
                    size_hint_y: None
                    height: dp(50)
                    canvas.before:
                        Color:
                            rgba: root.button_blue
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(25),]
                    on_press: root.resume_game()

                Button:
                    text: 'Начать заново'
                    bold: True
                    font_size: dp(20)
                    background_color: 0, 0, 0, 0
                    color: 1, 1, 1, 1
                    size_hint_y: None
                    height: dp(50)
                    canvas.before:
                        Color:
                            rgba: root.button_gray
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(25),]
                    on_press: root.restart_game()
''')


class PauseScreen(Screen):
    bg_color = BG_COLOR
    text_color_label = TEXT_COLOR_LABEL
    text_color_value = TEXT_COLOR_VALUE
    button_blue = BUTTON_BLUE
    button_gray = BUTTON_GRAY
    gray_bg = GRAY_BG

    moves = NumericProperty(0)
    time_now = NumericProperty(0)
    #time_now = Screen.time_current
    
    def on_enter(self, *args):
        seconds = self.manager.time_current
        minutes = seconds // 60
        seconds_remaining = seconds % 60
        self.ids.time_label.text = f"{minutes:02d}:{seconds_remaining:02d}"
        self.ids.move_label.text = f"{self.manager.moves_current}"

    def resume_game(self):
        self.manager.current = "game"

    def restart_game(self):
        self.manager.current = "start"
