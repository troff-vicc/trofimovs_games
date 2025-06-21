import numpy as np


class Game:
    def __init__(self):
        self.tiles = np.arange(1, 17)  # 1-16 (16 - пустая клетка)
        self.empty_pos = 16 # Индекс пустой клетки
        self.moves = 0
        self.shuffle()

    def shuffle(self):
        """Перемешивает плитки с гарантией решаемости"""


    def move_tile(self, tile_value):
        """Пытается переместить плитку, возвращает успешность"""


    def is_solved(self):
        """Проверка победы"""
