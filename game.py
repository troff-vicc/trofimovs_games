import numpy as np


class Game:
    def __init__(self):
        self.tiles = np.arange(1, 17)  # 1-16 (16 - пустая клетка)
        self.empty_pos = 15 # Индекс пустой клетки
        self.tiles[15] = 0
        self.moves = 0
        self.shuffle()


    def shuffle(self):
        """Перемешивает плитки с гарантией решаемости"""
        np.random.shuffle(self.tiles)
        
        indexO = np.where(self.tiles == 0)
        np.delete(self.tiles, indexO)
        self.empty_pos = indexO[0][0]
        
        inversions = 0
        for i in range(15):
            for j in range(i + 1, 15):
                if self.tiles[i] > self.tiles[j]:
                    inversions += 1
                    
        empty_row = 3 - self.empty_pos//4
        if (inversions + empty_row) % 2 == 0:
            i = 0 if self.empty_pos != 0 and self.empty_pos != 1 else 14
            self.tiles[i], self.tiles[i+1] = self.tiles[i+1], self.tiles[i]


    def move_tile(self, tile_index):
        """Пытается переместить плитку, возвращает успешность"""
        if ((abs(tile_index - self.empty_pos) == 1
                and tile_index // 4 == self.empty_pos // 4)
                or abs(tile_index - self.empty_pos) == 4):
            
            (self.tiles[self.empty_pos],
            self.tiles[tile_index]) =  (self.tiles[tile_index],
                                        self.tiles[self.empty_pos])
            self.empty_pos = tile_index
            
            return True
        
        return False
        

    def is_solved(self):
        """Проверка победы"""
        tilesTrue = np.arange(1, 17)
        tilesTrue[15] = 0
        
        if (self.tiles == tilesTrue).all():
            return True
        
        return False