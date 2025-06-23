import numpy as np
import time


class Game:
    def __init__(self):
        self.tiles = np.arange(1, 17)  # 1-16 (16 - пустая клетка)
        self.empty_pos = 15 # Индекс пустой клетки
        self.tiles[15] = 0
        self.moves = 0
        self.start_time = int(time.time())
        self.shuffle()
        self.game_over = False
        self.time_now = 0
    
    
    def get_time(self):
        """Получает текущее время"""
        if not self.game_over:
            self.time_now = int(time.time()) - self.start_time
        
        return self.time_now


    def shuffle(self):
        """Перемешивает плитки с гарантией решаемости"""
        np.random.shuffle(self.tiles)
        
        indexO = np.where(self.tiles == 0)
        self.empty_pos = indexO[0][0]
        tiles_o = self.tiles[self.tiles != 0]
        
        inversions = 0
        for i in range(15):
            for j in range(i + 1, 15):
                if tiles_o[i] > tiles_o[j]:
                    inversions += 1
                    
        empty_row = self.empty_pos//4
        if (inversions + empty_row) % 2 == 0:
            i = 2 if self.empty_pos in (0, 1) else 0
            self.tiles[i], self.tiles[i+1] = self.tiles[i+1], self.tiles[i]
    
    
    def move_tile(self, tile_index):
        """Перемещает плитку или целый ряд/столбец к пустой клетке"""
        empty_row, empty_col = self.empty_pos // 4, self.empty_pos % 4
        tile_row, tile_col = tile_index // 4, tile_index % 4
        
        # Проверяем, что плитка в одной строке или столбце с пустой клеткой
        if not (tile_row == empty_row or tile_col == empty_col):
            return False  # Невозможно переместить
        
        # Горизонтальное движение (в строке)
        if tile_row == empty_row:
            row = self.tiles.reshape(4, 4)[empty_row, :]
            
            if tile_col > empty_col:
                row[empty_col:tile_col] = row[empty_col + 1:tile_col + 1]
            else:
                row[tile_col + 1:empty_col + 1] = row[tile_col:empty_col]
            
            row[tile_col] = 0  # Обновляем пустую клетку
            self.tiles.reshape(4, 4)[empty_row, :] = row  # Возвращаем строку обратно
        
        # Вертикальное движение (в столбце)
        elif tile_col == empty_col:
            col = self.tiles.reshape(4, 4)[:, empty_col]
            
            if tile_row > empty_row:
                col[empty_row:tile_row] = col[empty_row + 1:tile_row + 1]
            else:
                col[tile_row + 1:empty_row + 1] = col[tile_row:empty_row]
                
            col[tile_row] = 0  # Обновляем пустую клетку
            self.tiles.reshape(4, 4)[:, empty_col] = col  # Возвращаем столбец обратно
        
        self.moves += int(abs(tile_index - self.empty_pos) if tile_row == empty_row \
            else abs(tile_index - self.empty_pos) // 4)
        self.empty_pos = tile_index
        
        self.is_solved()
        return True
        

    def is_solved(self):
        """Проверка победы"""
        tilesTrue = np.arange(1, 17)
        tilesTrue[15] = 0
        
        if (self.tiles == tilesTrue).all():
            self.game_over = True
            return True
        
        return False