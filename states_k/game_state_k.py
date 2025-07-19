from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.animation import Animation, Parallel
from kivy.graphics import Color, Rectangle, RoundedRectangle
import numpy as np
import utils, time
from constants import *

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moves = 0
        self.empty_pos = (3,3)
        self.tiles = []
        self.build_ui()
        self.logs = utils.Logs()
        self.start_time = int(time.time())

    def build_ui(self):
        kivy_red = (RED[0] / 255, RED[1] / 255, RED[2] / 255, 1)
        kivy_BACKGROUND = (BACKGROUND[0] / 255, BACKGROUND[1] / 255, BACKGROUND[2] / 255, 1)
        kivy_GRAY = (GRAY[0] / 255, GRAY[1] / 255, GRAY[2] / 255, 1)
        self.moves = 0

        # Главный контейнер
        main_layout = FloatLayout()
        # Фон для всего экрана
        with main_layout.canvas.before:
            Color(*kivy_BACKGROUND)
            self.bg_rect = Rectangle(pos=main_layout.pos, size=main_layout.size)

        box_header = BoxLayout(orientation='vertical',
                             size_hint=(1, 0.1),
                             pos_hint={'top': 1},
                             spacing=5)

        grid_layout = GridLayout(
            cols=4,
            spacing='5dp',
            size_hint=(0.8, 0.8),
            pos_hint={"center_x": 0.5, "top": 0.9})
        with grid_layout.canvas.before:
            Color(*kivy_GRAY)
            grid_layout.bg_rect = Rectangle(pos=grid_layout.pos, size=grid_layout.size)

        numbers = np.arange(1, 17)  # 1-16 (16 - пустая клетка)
        numbers[15] = 0
        self.shuffle(numbers)
        for i in range(16):
            num = numbers[i]
            if num != 0:
                btn = Button(
                    text=str(num),
                    color=kivy_red,
                    font_size=FONT_SIZE_SP,
                    bold=True,  # Жирный шрифт
                    background_normal='',
                    background_color=kivy_BACKGROUND,
                    on_press=self.move_tile
                )
                self.tiles.append(btn)
                grid_layout.add_widget(btn)
            else:
                # Добавляем невидимый виджет для сохранения позиции
                empty = Label(size_hint=(1, 1), opacity=0)
                self.tiles.append(empty)
                grid_layout.add_widget(empty)

        main_layout.add_widget(grid_layout)

        self.add_widget(main_layout)
        # Привязка изменения размера фона
        main_layout.bind( pos=lambda o, v: setattr(self.bg_rect, 'pos', o.pos),
            size=lambda o, v: setattr(self.bg_rect, 'size', o.size))
        grid_layout.bind(pos=lambda obj, pos: setattr(grid_layout.bg_rect, 'pos', pos),
                        size=lambda obj, size: setattr(grid_layout.bg_rect, 'size', size))


    def shuffle(self,numbers):
        """Перемешивает плитки с гарантией решаемости"""
        np.random.shuffle(numbers)
        indexO = np.where(numbers == 0)
        empty_pos = indexO[0][0]
        tiles_o = numbers[numbers != 0]

        inversions = 0
        for i in range(15):
            for j in range(i + 1, 15):
                if tiles_o[i] > tiles_o[j]:
                    inversions += 1

        empty_row = empty_pos // 4
        if (inversions + empty_row) % 2 == 0:
            i = 2 if empty_pos in (0, 1) else 0
            numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]

        self.empty_pos = divmod(empty_pos, 4)


    def move_tile(self, instance):
        idx = self.tiles.index(instance)
        row, col = divmod(idx, 4)
        empty_row, empty_col = self.empty_pos

        if (abs(row - empty_row) == 1 and col == empty_col) or (abs(col - empty_col) == 1 and row == empty_row):
            empty_idx = empty_row * 4 + empty_col
            clicked_tile = self.tiles[idx]
            empty_tile = self.tiles[empty_idx]

            # Анимация перемещения
            pos1 = empty_tile.pos.copy()
            pos2 = clicked_tile.pos.copy()
            Animation(pos=pos1, duration=0.15).start(clicked_tile)
            Animation(pos=pos2, duration=0.15).start(empty_tile)
            # Меняем плитки местами в списке
            self.tiles[idx] = empty_tile
            self.tiles[empty_idx] = clicked_tile
            self.empty_pos = (row, col)
            self.moves += 1
            empty_tile.pos = pos2
            clicked_tile.pos = pos1

            # Проверка победы
            if self.check_win():
                self.handle_win()

    def check_win(self):
        for i in range(15):
            if isinstance(self.tiles[i], Button):
                if not self.tiles[i] or int(self.tiles[i].text) != i + 1:
                    return False
        return True

    def handle_win(self):

        self.logs.save_result(self.moves, self.get_time())

        # Показываем Popup с результатом
        popup = Popup(
            title="Победа!",
            size_hint=(0.7, 0.4),
            content=Label(text=f"Вы собрали за {self.moves} ходов!")
        )
        popup.open()

        # Возврат на стартовый экран после закрытия Popup
        popup.bind(on_dismiss=lambda x: setattr(self.manager, "current", "finish"))

    def get_time(self):
        self.time_now = int(time.time()) - self.start_time
        return self.time_now