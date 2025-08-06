from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.animation import Animation, Parallel
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty, StringProperty
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.clock import Clock
import numpy as np
import utils, time
from constants import *

Builder.load_string("""
<ImageButton>:
    keep_ratio: True
    allow_stretch: True


<GameScreen>:
    game_layout: game_layout
    BoxLayout:
        id: game_layout
        orientation: 'vertical'
        spacing: dp(5)
        canvas.before:
            Color:
                rgba: root.background_color
            Rectangle:
                pos: self.pos
                size: self.size

        # Верхняя панель (10% экрана)
        BoxLayout:
            size_hint_y: 0.1
            size_hint_x: None
            width: min(dp(400), self.parent.width * 0.95)
            pos_hint: {'center_x': 0.5}
            padding: dp(10)
            spacing: dp(10)

            BoxLayout:
                orientation: 'horizontal'
                spacing: dp(20)
                padding: [dp(20), dp(20), dp(20), 0]
                pos_hint: {'center_y': 0.5}  # Центрирование по вертикали
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(15),]

                ImageButton:
                    size_hint: None, None
                    size: dp(40), dp(40)
                    source: 'resources/pause.png'
                    on_press: root.back_button_pressed()
                    pos_hint: {'center_y': 0.5}

                # Пустой виджет для отступа
                Widget:
                    size_hint_x: None
                    width: dp(100)

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(2)
                    pos_hint: {'center_y': 0.5}  # Центрирование блока

                    Label:
                        text: 'Ходы'
                        font_size: dp(12)
                        color: root.text_color
                        height: self.texture_size[1]

                    Label:
                        text: '{}'.format(root.moves)
                        font_size: dp(24)
                        bold: True
                        color: 0, 0, 0, 1
                        height: self.texture_size[1]

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(2)
                    pos_hint: {'center_y': 0.5}  # Центрирование блока

                    Label:
                        text: 'Время'
                        font_size: dp(12)
                        color: root.text_color
                        height: self.texture_size[1]

                    Label:
                        text: root.format_time(root.time_now)
                        font_size: dp(24)
                        bold: True
                        color: 0, 0, 0, 1
                        height: self.texture_size[1]


        # Центральная часть с квадратной сеткой 4x4 (80% экрана)
        FloatLayout:
            size_hint_y: 0.8

            # Фон для GridLayout (закругленный прямоугольник)
            canvas.before:
                Color:
                    rgba: root.background_grid_color
                RoundedRectangle:
                    # Центрируем фон и задаем размер как у GridLayout
                    pos: ((self.width - (min(dp(400), self.parent.width * 0.95) - dp(30))) / 2, (self.parent.height - (min(dp(400), self.parent.width * 0.95) - dp(30))) / 2)
                    size: ((min(dp(400), self.parent.width * 0.95) - dp(30)), (min(dp(400), self.parent.width * 0.95) - dp(30)))
                    radius: [dp(20),]

            GridLayout:
                id: grid
                cols: 4
                rows: 4
                spacing: dp(15)
                size_hint: None, None
                width: min(dp(400), self.parent.width * 0.95) - dp(30)  # Уменьшаем на padding*2
                height: self.width
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                padding: dp(15)  # Внутренние отступы


        # Нижняя часть (10% экрана)
        BoxLayout:
            size_hint_y: 0.1
""")


def draw_letter(layout, letter, on_press_def):
    # to-do необходимо цвета хранить в константах
    kivy_red = (RED[0] / 255, RED[1] / 255, RED[2] / 255, 1)
    kivy_BACKGROUND = (BACKGROUND[0] / 255, BACKGROUND[1] / 255, BACKGROUND[2] / 255, 1)

    # Создаем кнопку с прозрачным фоном
    btn = Button(
        text=letter,
        background_normal='',
        background_color=(0, 0, 0, 0),  # Полная прозрачность
        color=(1, 0, 0, 1),  # Красный текст
        font_size=dp(24),
        bold=True,
        on_press=on_press_def,
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
    return btn


class ImageButton(ButtonBehavior, Image):
    pass


class GameScreen(Screen):
    background_color = get_color_from_hex('#F0FDF5')
    text_color = get_color_from_hex('#6B7280')
    background_grid_color = get_color_from_hex('#DCEEE9')
    moves = NumericProperty(0)
    time_now = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moves = 0
        self.empty_pos = (3, 3)
        self.tiles = []
        self.logs = utils.Logs()
        self.numbers = np.arange(1, 17)
        self.numbers[15] = 0
        self.create_grid_buttons()


    def on_size(self, *args):
        # Обновляем размеры при изменении размера экрана
        grid = self.ids.grid
        grid.width = min(dp(400), self.width * 0.95)
        grid.height = grid.width

    def on_enter(self, *args):
        self.start_counter()


    def create_grid_buttons(self):
        self.ids.grid.clear_widgets()
        grid = self.ids.grid

        self.shuffle()

        for i in range(16):
            num = self.numbers[i]
            if num != 0:
                btn = draw_letter(grid, str(num), lambda x: self.move_tile(x))
                self.tiles.append(btn)
            else:
                # Добавляем невидимый виджет для сохранения позиции
                empty = Label(size_hint=(1, 1), opacity=0)
                self.tiles.append(empty)
                grid.add_widget(empty)

    def shuffle(self):
        """Перемешивает плитки с гарантией решаемости"""
        np.random.shuffle(self.numbers)
        indexO = np.where(self.numbers == 0)
        empty_pos = indexO[0][0]
        tiles_o = self.numbers[self.numbers != 0]

        inversions = 0
        for i in range(15):
            for j in range(i + 1, 15):
                if tiles_o[i] > tiles_o[j]:
                    inversions += 1

        empty_row = empty_pos // 4
        if (inversions + empty_row) % 2 == 0:
            i = 2 if empty_pos in (0, 1) else 0
            self.numbers[i], self.numbers[i + 1] = self.numbers[i + 1], self.numbers[i]

        self.empty_pos = divmod(empty_pos, 4)


    def move_tile(self, instance):
        idx = self.tiles.index(instance)
        row, col = divmod(idx, 4)
        empty_row, empty_col = self.empty_pos

        # Проверяем, что плитка в одной строке или столбце с пустой клеткой
        if not (row == empty_row or col == empty_col):
            return False  # Невозможно переместить

        if row == empty_row:
            row1 = self.numbers.reshape(4, 4)[empty_row, :]

            if col > empty_col:
                row1[empty_col:col] = row1[empty_col + 1:col + 1]
            else:
                row1[col + 1:empty_col + 1] = row1[col:empty_col]

            row1[col] = 0  # Обновляем пустую клетку
            self.numbers.reshape(4, 4)[empty_row, :] = row1
        elif col == empty_col:
            col1 = self.numbers.reshape(4, 4)[:, empty_col]

            if row > empty_row:
                col1[empty_row:row] = col1[empty_row + 1:row + 1]
            else:
                col1[row + 1:empty_row + 1] = col1[row:empty_row]

            col1[row] = 0  # Обновляем пустую клетку
            self.numbers.reshape(4, 4)[:, empty_col] = col1

        if row == empty_row or col == empty_col:
            empty_idx = empty_row * 4 + empty_col

            step = 1 if row == empty_row else 4
            i = (idx - empty_idx) // abs(idx - empty_idx)
            step *= i

            list_idx = [idx_n for idx_n in range(empty_idx, idx + i, step)]
            empty_tile = self.tiles[empty_idx]

            for idx_one in list_idx[1:]:
                tiles_one = self.tiles[idx_one]
                pos1 = empty_tile.pos.copy()
                pos2 = tiles_one.pos.copy()

                Animation(pos=pos1, duration=0.15).start(tiles_one)
                Animation(pos=pos2, duration=0.15).start(empty_tile)

                self.tiles[idx_one] = empty_tile
                self.tiles[empty_idx] = tiles_one

                empty_tile.pos = pos2
                tiles_one.pos = pos1

                empty_idx = idx_one
                self.empty_pos = divmod(idx_one, 4)

            self.moves += 1

            # Проверка победы
            if self.check_win():
                self.handle_win()

    def check_win(self):
        """Проверка победы"""
        tilesTrue = np.arange(1, 17)
        tilesTrue[15] = 0

        tilesCurrent = np.array([], dtype=int)
        for i in range(16):
            if isinstance(self.tiles[i], Button):
                tilesCurrent = np.append(tilesCurrent, int(self.tiles[i].text))
            else:
                tilesCurrent = np.append(tilesCurrent, 0)

        if (tilesCurrent == tilesTrue).all():
            self.logs.save_result(self.moves, self.time_now)
            return True

        return False

    def handle_win(self):

        self.logs.save_result(self.moves, self.time_now)
        self.manager.moves_current = self.moves
        self.manager.time_current = self.time_now
        self.stop_counter()
        self.manager.current = "finish"


    def back_button_pressed(self):
        self.manager.moves_current = self.moves
        self.manager.time_current = self.time_now
        self.stop_counter()
        self.manager.current = "pause"

    def format_time(self, seconds):
        minutes = seconds // 60  # Целочисленное деление вместо math.floor
        seconds = seconds % 60  # Остаток от деления
        return f"{minutes:02d}:{seconds:02d}"

    def start_counter(self, curent_time=0):
        # Запускаем обновление счетчика каждую секунду
        self.clock_event = Clock.schedule_interval(self.update_counter, 1.0)
        if curent_time==0:
            self.start_time = int(time.time())
        else:
            self.start_time = int(time.time()) - int(curent_time)

    def stop_counter(self):
        # Останавливаем обновление счетчика
        if self.clock_event:
            self.clock_event.cancel()
            self.clock_event = None

    def update_counter(self, dt):
        # Эта функция будет вызываться каждую секунду
        self.time_now = int(time.time()) - self.start_time