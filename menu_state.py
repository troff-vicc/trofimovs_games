from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty
import utils
from constants import *


class StartScreen(Screen):
    record = NumericProperty(0)  # Для автоматического обновления Label


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logs = utils.Logs()
        self.load_record()
        self.build_ui()

    def build_ui(self):
        kivy_blue = (BLUE[0] / 255, BLUE[1] / 255, BLUE[2] / 255, 1)
        kivy_red = (RED[0] / 255, RED[1] / 255, RED[2] / 255, 1)
        kivy_BACKGROUND = (BACKGROUND[0] / 255, BACKGROUND[1] / 255, BACKGROUND[2] / 255, 1)
        # Главный контейнер
        main_layout = FloatLayout()

        # Фон для всего экрана
        with main_layout.canvas.before:
            Color(*kivy_blue)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)

        def draw_letter(layout, letter):
            # Создаем кнопку с прозрачным фоном
            btn = Button(
                text=letter,
                background_normal='',
                background_color=(0, 0, 0, 0),  # Полная прозрачность
                color=kivy_red,
                font_size=FONT_SIZE_SP,
                bold=True,  # Жирный шрифт
                size_hint=(1, 1)
            )

            # Очищаем canvas перед рисованием
            btn.canvas.before.clear()

            # Рисуем тень и кнопку
            with btn.canvas.before:
                # 1. Тень (смещенный прямоугольник)
                Color(0, 0, 0, 0.3)  # Черный с прозрачностью 30%
                RoundedRectangle(
                    pos=(btn.x + 3, btn.y - 5),  # Смещение тени
                    size=btn.size,
                    radius=[20, ]
                )

                # 2. Основная кнопка
                Color(*kivy_BACKGROUND)
                btn.rect = RoundedRectangle(
                    pos=btn.pos,
                    size=btn.size,
                    radius=[20, ]
                )

            # Функция для обновления графики при изменении размера/позиции
            def update_graphics(instance, _):
                instance.canvas.before.clear()
                with instance.canvas.before:
                    # Тень
                    Color(0, 0, 0, 0.3)
                    RoundedRectangle(
                        pos=(instance.x + 3, instance.y - 5),
                        size=instance.size,
                        radius=[20, ]
                    )
                    # Кнопка
                    Color(*kivy_BACKGROUND)
                    instance.rect = RoundedRectangle(
                        pos=instance.pos,
                        size=instance.size,
                        radius=[20, ]
                    )

            btn.bind(pos=update_graphics, size=update_graphics)
            layout.add_widget(btn)


        # Создаем горизонтальный layout 1
        h_layout = BoxLayout(orientation='horizontal', size_hint=(0.9, 0.11),
                             pos_hint={'center_x': 0.5, 'top': 0.9},
                             spacing=5)
        letters = ["Н", "о", "в", "а", "я"]
        for i, letter in enumerate(letters):
            draw_letter(h_layout, letter)
        main_layout.add_widget(h_layout)

        # Создаем горизонтальный layout 2
        h_layout = BoxLayout(orientation='horizontal', size_hint=(0.7, 0.11),
                             pos_hint={'center_x': 0.5, 'top': 0.75},
                             spacing=5)
        letters = ["и", "г", "р", "а"]
        for i, letter in enumerate(letters):
            draw_letter(h_layout, letter)
        main_layout.add_widget(h_layout)

        # Кнопка запуска
        start_btn = Button(
            size_hint=(0.65, 0.2),
            pos_hint={'center_x': 0.5, 'y': 0.3},
            background_normal='resources/playbutton.png',
            background_down='resources/playbutton.png',  # Та же картинка при нажатии
            border=(0, 0, 0, 0)  # Убираем границы кнопки
        )
        start_btn.bind(on_press=self.switch_to_game)
        main_layout.add_widget(start_btn)

        # Создаем горизонтальный layout 4
        h_layout = BoxLayout(orientation='horizontal',
                             size_hint=(0.3, 0.2),
                             pos_hint={'center_x': 0.4, 'top': 0.25},
                             spacing=5)
        # а в нем вертикальный
        v_layout = BoxLayout(orientation='vertical',
                             size_hint=(0.7, 0.35),
                             pos_hint={'center_x': 0.25, 'top': 0.6},
                             spacing=5
        )
        # Добавляем медаль
        medal = Image(source='resources/medal.png', allow_stretch=True, keep_ratio=True, size_hint=(0.9, 0.9))
        h_layout.add_widget(medal)
        # Добавляем надпись с рекордом
        record_label = Label( text=f"Рекорд", font_size='20sp', color=BLACK, bold=True)
        # Добавляем надпись со временем
        time_label = Label(text=f"{self.on_record()}", font_size='20sp', color=BLACK, bold=True)
        v_layout.add_widget(record_label)
        v_layout.add_widget(time_label)
        h_layout.add_widget(v_layout)

        main_layout.add_widget(h_layout)

        self.add_widget(main_layout)

        # Привязка изменения размера фона
        main_layout.bind(
            pos=lambda o, v: setattr(self.bg_rect, 'pos', o.pos),
            size=lambda o, v: setattr(self.bg_rect, 'size', o.size)
        )



    def load_record(self):
        self.record = self.logs.record['time_seconds']

    def switch_to_game(self, instance):
        self.manager.current = "game"

    def on_record(self, *args):
        seconds = self.logs.record['time_seconds']
        minutes = seconds // 60
        seconds_remaining = seconds % 60
        return f"{minutes:02d}:{seconds_remaining:02d}"
