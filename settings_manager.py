import json
import os


class SettingsManager:
    SETTINGS_FILE = 'game_settings.json'

    def __init__(self):
        self.sound_enabled = True
        self.vibration_enabled = True
        self.load_settings()

    def load_settings(self):
        """Загрузка настроек из файла"""
        default_settings = {
            'sound_enabled': True,
            'vibration_enabled': True
        }

        try:
            if os.path.exists(self.SETTINGS_FILE):
                with open(self.SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
                    self.sound_enabled = settings.get('sound_enabled', True)
                    self.vibration_enabled = settings.get('vibration_enabled', True)
            else:
                self.save_settings()
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.save_settings()

    def save_settings(self):
        """Сохранение настроек в файл"""
        settings = {
            'sound_enabled': self.sound_enabled,
            'vibration_enabled': self.vibration_enabled
        }

        try:
            with open(self.SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def toggle_sound(self):
        """Переключение звука"""
        self.sound_enabled = not self.sound_enabled
        self.save_settings()
        return self.sound_enabled

    def toggle_vibration(self):
        """Переключение вибрации"""
        self.vibration_enabled = not self.vibration_enabled
        self.save_settings()
        return self.vibration_enabled