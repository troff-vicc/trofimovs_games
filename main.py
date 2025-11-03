from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from settings_manager import SettingsManager
from menu_state import StartScreen
from game_state import GameScreen
from finish_state import FinishScreen
from pause_state import PauseScreen


class FifteenPuzzleApp(App):
    def build(self):

        Window.fullscreen = 'auto'  # для адаптации

        sm = ScreenManager()
        sm.settings = SettingsManager()

        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(FinishScreen(name="finish"))
        sm.add_widget(PauseScreen(name="pause"))
        sm.current = "start"


        return sm

    def on_pause(self):
        # Пробрасываем событие в текущий экран
        current_screen = self.root.current_screen
        if hasattr(current_screen, 'on_pause'):
            return current_screen.on_pause()
        return True

    def on_resume(self):
        current_screen = self.root.current_screen
        if hasattr(current_screen, 'on_resume'):
            current_screen.on_resume()

if __name__ == "__main__":
    FifteenPuzzleApp().run()
