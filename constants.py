# Цвета
from pygame.examples.aliens import SCORE
from kivy.core.window import Window

BACKGROUND = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (153, 217, 234)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Размеры
WINDOW_SIZE = 600
TILE_RADIUS = 10
BORDER_WIDTH = int(WINDOW_SIZE * 0.05)  # 5% от размера окна
SCORE_TEXT = 10
TILE_PADDING = 2  # Отступ между плитками
TILE_SIZE = (WINDOW_SIZE - 2 * BORDER_WIDTH - (4 + 1)*TILE_PADDING) // 4
FONT_SIZE = TILE_SIZE // 2
SMALL_FONT_SIZE = 20
FONT_SIZE_SP = '40sp'

WINDOW_WIDTH_k = Window.width
BORDER_WIDTH_k = int(WINDOW_WIDTH_k * 0.05)  # 5% от размера окна
#TILE_SIZE_k = int((WINDOW_WIDTH_k - 2 * BORDER_WIDTH_k - (4 + 1)*TILE_PADDING) // 6)
TILE_SIZE_k = 0.2

# Эффекты объемности
TILE_SHADOW_COLOR = (50, 50, 50)  # Цвет тени
HIGHLIGHT_COLOR = (220, 220, 255)  # Цвет блика
SHADOW_OFFSET = 3  # Смещение тени
HIGHLIGHT_SIZE = 2  # Толщина блика

# Прочее
FPS = 60