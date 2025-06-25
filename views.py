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
        self.curent_view = 'start'

    def draw_view(self):
        if self.curent_view == 'start':
            self.draw_start()
        else:
            self.draw_place()


    def draw_place(self):
        """Отрисовываем игровое поле"""
        self.screen.fill(BACKGROUND)
        seconds = self.game.get_time()
        minutes = seconds // 60
        seconds_remaining = seconds % 60
        record_text = self.small_font.render(f"Время: {minutes:02d}:{seconds_remaining:02d}", True, BLACK)
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
        """Отрисовываем стартовый/финишный экран"""

        """заливаем фон"""
        self.screen.fill(GRAY)

        """надпись 1"""
        surface_text = self.font.render(f"Новая игра", True, BLACK)
        self.screen.blit(surface_text, ((WINDOW_SIZE - surface_text.get_width()) // 2, BORDER_WIDTH))

        """кнопка"""
        button_img = pygame.image.load("playbutton.png")  # PNG с прозрачностью
        button_rect = button_img.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))  # Прямоугольник кнопки
        self.screen.blit(button_img, button_rect)

        """надпись 2"""
        surface_text = self.small_font.render(f"Рекорд", True, BLACK)
        self.screen.blit(surface_text, ((WINDOW_SIZE - surface_text.get_width()) // 2,
                                        (WINDOW_SIZE - 2*BORDER_WIDTH - surface_text.get_height())))

        """надпись 3 и иконка"""
        seconds = self.logs.record['time_seconds']
        minutes = seconds // 60
        seconds_remaining = seconds % 60
        surface_text = self.small_font.render(f"{minutes:02d}:{seconds_remaining:02d}", True, BLACK)
        self.screen.blit(surface_text, ((WINDOW_SIZE - surface_text.get_width()) // 2,
                                        (WINDOW_SIZE - BORDER_WIDTH - surface_text.get_height())))
        icon = pygame.image.load("medal.png").convert_alpha()
        icon_rect = icon.get_rect(center=((WINDOW_SIZE - surface_text.get_width()- icon.get_width()) // 2 ,
                                        (WINDOW_SIZE - BORDER_WIDTH - surface_text.get_height())))
        self.screen.blit(icon, icon_rect)

    def event_listen(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.curent_view == 'start':
                self.curent_view = 'place'
            else:
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
                        self.curent_view = 'start'


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