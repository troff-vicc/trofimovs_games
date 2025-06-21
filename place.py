import pygame
from constants import *

class Place:
    
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Пятнашки")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)


    def draw_place(self):
        """Отрисовываем игровое поле"""
        self.screen.fill(BACKGROUND)
        # Рисуем белую рамку вокруг игрового поля
        border_rect = pygame.Rect(
            BORDER_WIDTH,
            BORDER_WIDTH,
            WINDOW_SIZE - 2 * BORDER_WIDTH,
            WINDOW_SIZE - 2 * BORDER_WIDTH
        )
        pygame.draw.rect(self.screen, BACKGROUND, border_rect, BORDER_WIDTH)

        # Рисуем фон игрового поля внутри рамки
        game_field_rect = pygame.Rect(
            BORDER_WIDTH,  # Отступ от рамки
            BORDER_WIDTH,
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
            y = BORDER_WIDTH + TILE_PADDING + row * (TILE_SIZE + TILE_PADDING)
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

    def run(self):
        """Запускает главный игровой цикл"""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    col = mouse_pos[0] // TILE_SIZE
                    row = mouse_pos[1] // TILE_SIZE
                    tile_index = row * 4 + col
                    # двигаем плитку
                    self.game.move_tile(tile_index)

            self.draw_place()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()