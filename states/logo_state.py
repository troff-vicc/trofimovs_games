import pygame
import time
from constants import *

class LogoState:
    def __init__(self, screen, change_state):
        self.screen = screen
        self.change_state = change_state  # Функция для смены состояния
        self.start_time = time.time()


    def handle_events(self, event):
        # Проверяем, прошло ли 5 секунд
        if time.time() - self.start_time > 5:
            self.change_state("menu") # Переключаемся на меню


    def draw(self):
        
        """заливаем фон"""
        self.screen.fill(BLUE)

        """Показываем заставку"""
        logo = pygame.image.load("resources/logo.png").convert_alpha()
        logo = pygame.transform.scale(logo, (400, 300))  # Масштабирование
        logo_rect = logo.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        self.screen.blit(logo, logo_rect)
        """надпись"""
        my_font = pygame.font.SysFont('Arial', SMALL_FONT_SIZE, bold=True)
        surface_text = my_font.render(f"trofimov studio", True, BLACK)
        self.screen.blit(surface_text, ((WINDOW_SIZE - surface_text.get_width()) // 2,
                                        (WINDOW_SIZE - 2 * BORDER_WIDTH - surface_text.get_height())))
        pygame.display.flip()