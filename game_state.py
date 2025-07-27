from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.animation import Animation, Parallel
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivy.graphics import Color, RoundedRectangle, Rectangle
import numpy as np
import utils, time
from constants import *

Builder.load_string("""
<FlatButton>:
    canvas.before:
        Color:
            rgba: self.shadow_color
        RoundedRectangle:
            pos: self.pos[0]-self.shadow_offset, self.pos[1]-self.shadow_offset
            size: self.size[0]+self.shadow_offset*2, self.size[1]+self.shadow_offset*2
            radius: [self.border_radius + self.shadow_offset,]
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.border_radius,]

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
            padding: dp(10)
            spacing: dp(10)

            Button:
                text: 'Назад'
                size_hint_x: 0.2
                background_color: root.button_color
                background_normal: ''
                color: 1, 1, 1, 1
                font_size: dp(24)
                on_press: root.back_button_pressed()

            Label:
                text: 'Очки: 0'
                halign: 'center'
                valign: 'middle'
                size_hint_x: 0.8
                font_size: dp(32)
                bold: True
                color: 0, 0, 0, 1

        # Центральная часть с квадратной сеткой 4x4 (80% экрана)
        FloatLayout:
            size_hint_y: 0.8

            GridLayout:
                id: grid
                cols: 4
                rows: 4
                spacing: dp(15)
                size_hint: None, None
                width: self.parent.width * 0.95
                height: self.width
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}

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
        on_press= on_press_def,
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


class GameScreen(Screen):
    background_color = get_color_from_hex('#ecf0f1')  # Светло-серый фон
    button_color = get_color_from_hex('#7f8c8d')     # Темно-серый для кнопок

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moves = 0
        self.empty_pos = (3,3)
        self.tiles = []
        self.logs = utils.Logs()
        self.start_time = int(time.time())
        self.create_grid_buttons()

    def create_grid_buttons(self):

        grid = self.ids.grid
        numbers = np.arange(1, 17)  # 1-16 (16 - пустая клетка)
        numbers[15] = 0
        self.shuffle(numbers)

        for i in range(16):
            num = numbers[i]
            if num != 0:
                btn = draw_letter(grid, str(num), lambda x: self.move_tile(x))
                self.tiles.append(btn)
                #grid.add_widget(btn)
            else:
                # Добавляем невидимый виджет для сохранения позиции
                empty = Label(size_hint=(1, 1), opacity=0)
                self.tiles.append(empty)
                grid.add_widget(empty)


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

    def back_button_pressed(self):
        self.manager.current = "pause"  # to-do поменять на menu

    def move_tile(self, instance):
        idx = self.tiles.index(instance)
        row, col = divmod(idx, 4)
        empty_row, empty_col = self.empty_pos

        # Проверяем, что плитка в одной строке или столбце с пустой клеткой
        if not (row == empty_row or col == empty_col):
            return False  # Невозможно переместить

        """def movieOneStep(idx_1, idx_2):
            clicked_tile = self.tiles[idx_1]
            empty_tile = self.tiles[idx_2]

            # Анимация перемещения
            pos1 = empty_tile.pos.copy()
            pos2 = clicked_tile.pos.copy()
            Animation(pos=pos1, duration=0.15).start(clicked_tile)
            Animation(pos=pos2, duration=0.15).start(empty_tile)
            # Меняем плитки местами в списке
            self.tiles[idx_1] = empty_tile
            self.tiles[idx_2] = clicked_tile

            empty_tile.pos = pos2
            clicked_tile.pos = pos1
            print(f'пустая в {idx_1} а кнопка в {idx_2}')
            print(f'позиция пустой {pos2} а кнопка в {pos1}')

        # Горизонтальное движение (в строке)
        if row == empty_row:
            cur_empty = empty_col
            cur_idx = idx
            steps = 0
            if col > empty_col:
                while col > cur_empty:
                    movieOneStep(cur_idx,cur_idx-1)
                    steps +=1
                    cur_empty +=1
                    cur_idx +=1

            else:
                while col < cur_empty:
                    movieOneStep(cur_idx,cur_idx+1)
                    steps +=1
                    cur_empty -=1
                    cur_idx -=1


            self.empty_pos = (row, col)
            self.moves += steps"""

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
            self.game_over = True
            self.logs.save_result(self.moves, self.get_time())
            return True

        return False

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


