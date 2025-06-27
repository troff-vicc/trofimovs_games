import pygame, time
import utils
from constants import *
import numpy as np


class GameState:
    def __init__(self, screen, change_state):
        self.screen = screen
        self.change_state = change_state
        self.logs = utils.Logs()
        self.font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)
        self.small_font = pygame.font.SysFont('Arial', SMALL_FONT_SIZE, bold=True)
        self.button_rect = None
        self.tiles = np.arange(1, 17)  # 1-16 (16 - пустая клетка)
        self.empty_pos = 15  # Индекс пустой клетки
        self.tiles[15] = 0
        self.moves = 0
        self.start_time = int(time.time())
        self.shuffle()
        self.game_over = False
        self.time_now = 0

    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.change_state("menu")
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяем, была ли нажата левая кнопка мыши
            if event.button == 1:  # 1 - левая кнопка мыши
                # Проверяем, находится ли курсор в пределах кнопки
                if self.button_rect.collidepoint(event.pos):
                    self.change_state("menu")  # Переключаемся на меню
                elif not self.game_over:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Проверяем, что клик внутри игрового поля
                    if (BORDER_WIDTH <= mouse_x < WINDOW_SIZE - BORDER_WIDTH and
                            BORDER_WIDTH <= mouse_y < WINDOW_SIZE - BORDER_WIDTH):

                        # Вычисляем позицию плитки
                        col = (mouse_x - BORDER_WIDTH) // (TILE_SIZE + TILE_PADDING)
                        row = (mouse_y - BORDER_WIDTH - SCORE_TEXT) // (TILE_SIZE + TILE_PADDING)

                        if 0 <= row < 4 and 0 <= col < 4:
                            tile_pos = row * 4 + col
                            self.move_tile(tile_pos)

                    if self.game_over:
                        pygame.display.set_caption("Победа")
                        self.change_state("menu")
    
    def draw(self):
        """Отрисовываем игровое поле"""
        self.screen.fill(BACKGROUND)
        seconds = self.get_time()
        minutes = seconds // 60
        seconds_remaining = seconds % 60

        #текст (справа)
        record_text = self.small_font.render(f"Время: {minutes:02d}:{seconds_remaining:02d}",
                                             True, BLACK)
        score_text = self.small_font.render(f"Ходы: {self.moves}", True, BLACK)
        self.screen.blit(record_text, ((WINDOW_SIZE - BORDER_WIDTH - record_text.get_width() - BORDER_WIDTH - score_text.get_width()),
                                       (SCORE_TEXT + BORDER_WIDTH - record_text.get_height()) // 2))
        self.screen.blit(score_text, ((WINDOW_SIZE - BORDER_WIDTH - score_text.get_width()),
                                      (SCORE_TEXT + BORDER_WIDTH - score_text.get_height()) // 2))

        """кнопка пауза"""
        button_img = pygame.image.load("resources/pause.png")  # PNG с прозрачностью
        self.button_rect = button_img.get_rect(topleft=(BORDER_WIDTH, 0))
        self.screen.blit(button_img, self.button_rect)

        # Рисуем белую рамку вокруг игрового поля
        border_rect = pygame.Rect(
            BORDER_WIDTH,
            BORDER_WIDTH + SCORE_TEXT,
            WINDOW_SIZE - 2 * BORDER_WIDTH,
            WINDOW_SIZE - 2 * BORDER_WIDTH
        )
        pygame.draw.rect(self.screen, BACKGROUND, border_rect, BORDER_WIDTH)
        
        # Рисуем фон игрового поля внутри рамки
        game_field_rect = pygame.Rect(
            BORDER_WIDTH,  # Отступ от рамки
            BORDER_WIDTH + SCORE_TEXT,
            WINDOW_SIZE - 2 * BORDER_WIDTH,
            WINDOW_SIZE - 2 * BORDER_WIDTH
        )
        pygame.draw.rect(self.screen, GRAY, game_field_rect, border_radius=TILE_RADIUS)
        
        # Рисуем плитку в цикле с учетом рамки
        for i in range(16):
            if self.tiles[i] == 0:
                continue
            
            row, col = i // 4, i % 4
            x = BORDER_WIDTH + TILE_PADDING + col * (TILE_SIZE + TILE_PADDING)
            y = BORDER_WIDTH + SCORE_TEXT + TILE_PADDING + row * (TILE_SIZE + TILE_PADDING)
            # 1. Рисуем тень (смещенную копию)
            shadow_rect = pygame.Rect(
                x + SHADOW_OFFSET,
                y + SHADOW_OFFSET,
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(self.screen, TILE_SHADOW_COLOR, shadow_rect,
                             border_radius=TILE_RADIUS)
            # 2. Основная плитка
            rect = pygame.Rect(
                x,
                y,
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(self.screen, BACKGROUND, rect, border_radius=TILE_RADIUS)
            # 3. Блик сверху и слева
            highlight_points = [
                (x, y + TILE_RADIUS),  # Верхний левый угол
                (x + TILE_RADIUS, y),  #
                (x + TILE_SIZE - TILE_RADIUS, y),  # Верхний правый
                (x + TILE_SIZE, y + TILE_RADIUS),  #
                (x + TILE_SIZE, y + HIGHLIGHT_SIZE),  # Правый край
                (x + HIGHLIGHT_SIZE, y + HIGHLIGHT_SIZE),  #
                (x + HIGHLIGHT_SIZE, y + TILE_SIZE),  # Левый край
                (x, y + TILE_SIZE)  # Нижний левый
            ]
            pygame.draw.polygon(self.screen, HIGHLIGHT_COLOR, highlight_points)
            # 4. Текст с эффектом вдавленности
            text = self.font.render(str(self.tiles[i]), True, RED)
            text_shadow = self.font.render(str(self.tiles[i]), True, TILE_SHADOW_COLOR)
            
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text_shadow, (text_rect.x + 1, text_rect.y + 1))  # Тень текста
            self.screen.blit(text, text_rect) # Основной текст
            
        pygame.display.flip()
    
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
        
        empty_row = self.empty_pos // 4
        if (inversions + empty_row) % 2 == 0:
            i = 2 if self.empty_pos in (0, 1) else 0
            self.tiles[i], self.tiles[i + 1] = self.tiles[i + 1], self.tiles[i]
    
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
        
        #self.moves += int(abs(tile_index - self.empty_pos) if tile_row == empty_row \
        #                      else abs(tile_index - self.empty_pos) // 4)
        
        self.moves += 1
        
        self.empty_pos = tile_index
        
        self.is_solved()
        return True
    
    def is_solved(self):
        """Проверка победы"""
        tilesTrue = np.arange(1, 17)
        tilesTrue[15] = 0
        
        if (self.tiles == tilesTrue).all():
            self.game_over = True
            self.logs.save_result(self.moves, self.get_time())
            return True
        
        return False