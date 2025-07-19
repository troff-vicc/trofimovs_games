from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.animation import Animation, Parallel
import numpy as np
import utils, time

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.moves = 0
        self.empty_pos = (3,3)
        self.tiles = []
        self.build_game_board()
        self.logs = utils.Logs()
        self.start_time = int(time.time())

    def build_game_board(self):
        self.grid = GridLayout(
            cols=4,
            spacing='5dp',
            size_hint=(0.95, 0.95),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.reset_game()
        self.add_widget(self.grid)

    def reset_game(self):
        self.moves = 0
        self.grid.clear_widgets()
        numbers = np.arange(1, 17)  # 1-16 (16 - пустая клетка)
        numbers[15] = 0
        self.shuffle(numbers)

        for i in range(16):
            num = numbers[i]
            if num != 0:
                btn = Button(
                    text=str(num),
                    font_size='36sp',
                    background_normal='',
                    background_color=(0.8, 0.3, 0.4, 1),
                    on_press=self.move_tile
                )
                self.tiles.append(btn)
                self.grid.add_widget(btn)
            else:
                # Добавляем невидимый виджет для сохранения позиции
                empty = Label(size_hint=(1, 1), opacity=0)
                self.tiles.append(empty)
                self.grid.add_widget(empty)

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