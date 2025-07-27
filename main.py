from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from menu_state import StartScreen
from game_state import GameScreen
from finish_state import FinishScreen
from logo_state import LogoScreen
from pause_state import PauseScreen


class FifteenPuzzleApp(App):
    def build(self):
        # Настройки для Android (полноэкранный режим)
        Window.size = (480, 860)
        # Отключаем полноэкранный режим
        Window.fullscreen = False
        # Window.fullscreen = 'auto'  # Или 'auto' для адаптации
        
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(FinishScreen(name="finish"))
        sm.add_widget(LogoScreen(name="logo"))
        sm.add_widget(PauseScreen(name="pause"))
        
        sm.current = "logo"
        
        return sm


if __name__ == "__main__":
    FifteenPuzzleApp().run()
