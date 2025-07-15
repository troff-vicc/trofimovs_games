from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from states.menu_state_k import StartScreen
from states.game_state_k import GameScreen




class FifteenPuzzleApp(App):
    def build(self):
        # Настройки для Android (полноэкранный режим)
        Window.size = (480, 860)
        # Отключаем полноэкранный режим
        Window.fullscreen = False
        #Window.fullscreen = 'auto'  # Или 'auto' для адаптации

        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))
        return sm

if __name__ == "__main__":
    FifteenPuzzleApp().run()