import pygame

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Размеры
WINDOW_SIZE = 600
BUTTON_SIZE = WINDOW_SIZE // 4
FONT_SIZE = BUTTON_SIZE // 2

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
        self.screen.fill(WHITE)
        for i in range(16):
            if self.game.tiles[i] == 16:
                continue

            row, col = i // 4, i % 4
            rect = pygame.Rect(col * BUTTON_SIZE, row * BUTTON_SIZE,
                               BUTTON_SIZE, BUTTON_SIZE)

            pygame.draw.rect(self.screen, WHITE, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)

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
                    col = mouse_pos[0] // BUTTON_SIZE
                    row = mouse_pos[1] // BUTTON_SIZE
                    tile_index = row * 4 + col
                    # двигаем плитку
                    self.game.move_tile(tile_index)

            self.draw_place()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()