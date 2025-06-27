import pygame
import utils
from constants import *

class MenuState:
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
            if event.button == 1:  # 1 - левая кнопка мыши
                # Проверяем, находится ли курсор в пределах кнопки
                if self.button_rect.collidepoint(event.pos):
                    self.change_state("game")  # Переключаемся на игру

    def update(self):
        pass  # Логика меню (если нужна)

    def draw(self):
        """Отрисовываем стартовый/финишный экран"""
        
        """заливаем фон"""
        self.screen.fill(GRAY)
        
        """надпись 1"""
        surface_text = self.font.render(f"Новая игра", True, BLACK)
        self.screen.blit(surface_text, ((WINDOW_SIZE - surface_text.get_width()) // 2, BORDER_WIDTH))
        
        """кнопка"""
        button_img = pygame.image.load("resources/playbutton.png")  # PNG с прозрачностью
        self.button_rect = button_img.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))  # Прямоугольник кнопки
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