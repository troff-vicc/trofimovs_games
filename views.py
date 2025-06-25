import pygame
from constants import *
import logs
from game import Game

current_window = 0

class Place:
    def __init__(self):
        self.game = Game()
        self.logs = logs.Logs()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + SCORE_TEXT))
        pygame.display.set_caption("Пятнашки")
        self.font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)
        self.small_font = pygame.font.SysFont('Arial', SMALL_FONT_SIZE, bold=True)

    def draw_view(self):
        curent_view = 2
        if curent_view == 1:
            self.draw_place()
        else:
            self.draw_start()


    def draw_place(self):
        """Отрисовываем игровое поле"""
        self.screen.fill(BACKGROUND)

        record_text = self.small_font.render(f"Время: {self.game.get_time()}", True, BLACK)
        self.screen.blit(record_text, (BORDER_WIDTH,
                                       (SCORE_TEXT + BORDER_WIDTH - record_text.get_height())//2))

        # Второй текст (справа)
        score_text = self.small_font.render(f"Ходы: {self.game.moves}", True, BLACK)
        self.screen.blit(score_text, (WINDOW_SIZE//2,
                                      (SCORE_TEXT + BORDER_WIDTH - record_text.get_height())//2))

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
            if self.game.tiles[i] == 0:
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
            text = self.font.render(str(self.game.tiles[i]), True, RED)
            text_shadow = self.font.render(str(self.game.tiles[i]), True, TILE_SHADOW_COLOR)

            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text_shadow, (text_rect.x + 1, text_rect.y + 1))  # Тень текста
            self.screen.blit(text, text_rect)  # Основной текст

    def draw_start(self):
        """Отрисовываем экран со статистикой"""
        self.screen.fill(GRAY)

        # Рисуем фон
        game_field_rect = pygame.Rect(
            0,
            0,
            WINDOW_SIZE,
            WINDOW_SIZE
        )
        pygame.draw.rect(self.screen, GRAY, game_field_rect, border_radius=TILE_RADIUS)

        record_text = self.small_font.render(f"Статистика игры:", True, BLACK)
        self.screen.blit(record_text, ((WINDOW_SIZE - record_text.get_width()) // 2,
                                       (SCORE_TEXT + BORDER_WIDTH - record_text.get_height()) // 2))


    def event_listen(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.game.game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Проверяем, что клик внутри игрового поля
                if (BORDER_WIDTH <= mouse_x < WINDOW_SIZE - BORDER_WIDTH and
                        BORDER_WIDTH <= mouse_y < WINDOW_SIZE - BORDER_WIDTH):

                    # Вычисляем позицию плитки
                    col = (mouse_x - BORDER_WIDTH) // (TILE_SIZE + TILE_PADDING)
                    row = (mouse_y - BORDER_WIDTH - SCORE_TEXT) // (TILE_SIZE + TILE_PADDING)

                    if 0 <= row < 4 and 0 <= col < 4:
                        tile_pos = row * 4 + col
                        self.game.move_tile(tile_pos)

                if self.game.game_over:
                    pygame.display.set_caption("Победа")
                    self.logs.save_result(self.game.moves, self.game.get_time())


def run():
    """Запускает главный игровой цикл"""
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    place = Place()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            place.event_listen(event)
        place.draw_view()
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()