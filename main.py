from game import Game
from place import Place

if __name__ == "__main__":
    game_logic = Game()      # Создаем логику игры
    game_display = Place(game_logic)  # Передаем логику в отрисовку
    game_display.run()       # Запускаем игровой цикл