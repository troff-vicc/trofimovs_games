import pygame
import utils
from constants import *

class FinishState:
    def __init__(self, screen, change_state):
        self.screen = screen
        self.change_state = change_state  # Функция для смены состояния
        self.logs = utils.Logs()
        self.font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)
        self.small_font = pygame.font.SysFont('Arial', SMALL_FONT_SIZE, bold=True)
        self.button_rect = None
        self.best_game = utils.Logs().record

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.change_state("game") # Переключаемся на игру
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяем, была ли нажата левая кнопка мыши
            if event.button == 1:
                if self.button_rect.collidepoint(event.pos): #находится ли курсор в пределах кнопки
                    self.change_state("game")  # Переключаемся на стартовую страницу


    def update(self):
        pass  # Логика меню (если нужна)

    def draw(self):
        """Отрисовываем стартовый/финишный экран"""
        
        """заливаем фон"""
        self.screen.fill(BLUE)
        
        """надпись 1"""
        letter_size = (WINDOW_SIZE - 2 * BORDER_WIDTH - 6 * TILE_PADDING) // 5
        letters = ["К", "о", "н", "е", "ц"]
        start_x = BORDER_WIDTH + TILE_PADDING
        step = letter_size + TILE_PADDING
        for i, letter in enumerate(letters):
            self.draw_letter(start_x + i * step, 20, letter, letter_size)
        letters = ["и", "г", "р", "ы"]
        start_x = BORDER_WIDTH + TILE_PADDING + letter_size // 2
        for i, letter in enumerate(letters):
            self.draw_letter(start_x + i * step, BORDER_WIDTH + letter_size + TILE_PADDING, letter, letter_size)

        """кнопка ДОМОЙ"""
        button_img = pygame.image.load("resources/back.png")  # PNG с прозрачностью
        # Тень под кнопкой
        button_with_shadow = button_img.get_rect(center=(WINDOW_SIZE // 2 + 5, WINDOW_SIZE // 2 + 2 * BORDER_WIDTH + 5))
        pygame.draw.rect(self.screen, GRAY, button_with_shadow, border_radius=TILE_RADIUS)
        # Прямоугольник кнопки (Белый фон)
        self.button_rect = button_img.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 2 * BORDER_WIDTH))
        pygame.draw.rect(self.screen, BACKGROUND, self.button_rect, border_radius=TILE_RADIUS)
        self.screen.blit(button_img, self.button_rect)

        """надпись 2"""
        surface_text = self.small_font.render(f"Рекорд", True, BLACK)
        self.screen.blit(surface_text, ((WINDOW_SIZE - surface_text.get_width()) // 2,
                                        (WINDOW_SIZE - 2 * BORDER_WIDTH - surface_text.get_height())))
        
        """надпись 3 и иконка"""
        seconds = self.logs.record['time_seconds']
        minutes = seconds // 60
        seconds_remaining = seconds % 60
        surface_text = self.small_font.render(f"{minutes:02d}:{seconds_remaining:02d}", True, BLACK)
        self.screen.blit(surface_text, ((WINDOW_SIZE - surface_text.get_width()) // 2,
                                        (WINDOW_SIZE - BORDER_WIDTH - surface_text.get_height())))
        icon = pygame.image.load("resources/medal.png").convert_alpha()
        icon_rect = icon.get_rect(center=((WINDOW_SIZE - surface_text.get_width() - icon.get_width()) // 2,
                                          (WINDOW_SIZE - BORDER_WIDTH - surface_text.get_height())))
        self.screen.blit(icon, icon_rect)
        pygame.display.flip()

    def draw_letter(self, x, y, text, letter_size=None):
        if letter_size is None:
            letter_size = TILE_SIZE // 2
        # 1. Рисуем тень (смещенную копию)
        shadow_rect = pygame.Rect(
            x + SHADOW_OFFSET,
            y + SHADOW_OFFSET,
            letter_size,
            letter_size
        )
        pygame.draw.rect(self.screen, TILE_SHADOW_COLOR, shadow_rect, border_radius=TILE_RADIUS)
        # 2. Основная плитка
        rect = pygame.Rect(
            x,
            y,
            letter_size,
            letter_size
        )
        pygame.draw.rect(self.screen, BACKGROUND, rect, border_radius=TILE_RADIUS)
        # 3. Блик сверху и слева
        highlight_points = [
            (x, y + TILE_RADIUS),  # Верхний левый угол
            (x + TILE_RADIUS, y),  #
            (x + letter_size - TILE_RADIUS, y),  # Верхний правый
            (x + letter_size, y + TILE_RADIUS),  #
            (x + letter_size-3, y + HIGHLIGHT_SIZE),  # Правый край
            (x + HIGHLIGHT_SIZE, y + HIGHLIGHT_SIZE),  #
            (x + HIGHLIGHT_SIZE, y + letter_size),  # Левый край
            (x, y + letter_size)  # Нижний левый
        ]
        pygame.draw.polygon(self.screen, HIGHLIGHT_COLOR, highlight_points)
        # 4. Текст с эффектом вдавленности
        font_letter = pygame.font.SysFont('Arial', int(letter_size * 0.75), bold=True)
        text_ = font_letter.render(str(text), True, RED)
        text_shadow = font_letter.render(str(text), True, TILE_SHADOW_COLOR)

        text_rect = text_.get_rect(center=rect.center)
        self.screen.blit(text_shadow, (text_rect.x + 1, text_rect.y + 1))  # Тень текста
        self.screen.blit(text_, text_rect)  # Основной текст