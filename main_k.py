from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from states_k.menu_state_k import StartScreen
from states_k.game_state_k import GameScreen
from states_k.finish_state_k import FinishScreen
from states_k.logo_state_k import LogoScreen



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
        sm.add_widget(FinishScreen(name="finish"))
        sm.add_widget(FinishScreen(name="finish"))
        sm.add_widget(LogoScreen(name="logo"))
        
        sm.current = "logo"
        
        return sm

if __name__ == "__main__":
    FifteenPuzzleApp().run()