import pygame

# Цвета
BACKGROUND = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Размеры
WINDOW_SIZE = 600
TILE_RADIUS = 10
BORDER_WIDTH = int(WINDOW_SIZE * 0.05)  # 2% от размера окна
TILE_PADDING = 2  # Отступ между плитками
TILE_SIZE = (WINDOW_SIZE - 2 * BORDER_WIDTH - (4 + 1)*TILE_PADDING) // 4
FONT_SIZE = TILE_SIZE // 2

# Прочее
FPS = 60

class Place:
    
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Пятнашки")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)


    def draw_place(self):
        """Отрисовывает игровое поле"""
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
            WINDOW_SIZE - 2* BORDER_WIDTH,
            WINDOW_SIZE - 2 * BORDER_WIDTH
        )
        pygame.draw.rect(self.screen, GRAY, game_field_rect, border_radius=TILE_RADIUS)

        # Рисуем плитку в цикле с учетом рамки
        for i in range(16):
            if self.game.tiles[i] == 16:
                continue

            row, col = i // 4, i % 4
            x = BORDER_WIDTH + TILE_PADDING + col * (TILE_SIZE + TILE_PADDING)
            y = BORDER_WIDTH + TILE_PADDING + row * (TILE_SIZE + TILE_PADDING)

            rect = pygame.Rect(
                x,
                y,
                TILE_SIZE,
                TILE_SIZE
            )
            #rect = pygame.Rect(col * TILE_SIZE + tile_offset, row * TILE_SIZE + tile_offset,
             #                  TILE_SIZE, TILE_SIZE)

            pygame.draw.rect(self.screen, BACKGROUND, rect, border_radius=TILE_RADIUS)
            pygame.draw.rect(self.screen, GRAY, rect, 2, border_radius=TILE_RADIUS)

            text = self.font.render(str(self.game.tiles[i]), True, RED)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

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