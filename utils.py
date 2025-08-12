import json
from datetime import datetime
import os


class LogsError:
    LOGS_FILE = 'logsError.json'  # или 'data/logs.json', если вы используете папку data
    
    @staticmethod
    def _ensure_file_exists():
        if not os.path.exists(LogsError.LOGS_FILE):
            with open(LogsError.LOGS_FILE, 'w') as f:
                json.dump([], f)
    
    @staticmethod
    def add_log(error_type, message, screen=None):
        """Добавляет запись в лог"""
        LogsError._ensure_file_exists()
        
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': error_type,
            'message': message,
            'screen': screen
        }
        
        try:
            with open(LogsError.LOGS_FILE, 'r+') as f:
                logs = json.load(f)
                logs.append(log_entry)
                f.seek(0)
                json.dump(logs, f, indent=4)
        except Exception as e:
            print(f"Failed to write log: {e}")
    
    @staticmethod
    def get_logs(limit=None):
        """Возвращает список логов, опционально с ограничением по количеству"""
        LogsError._ensure_file_exists()
        
        try:
            with open(LogsError.LOGS_FILE, 'r') as f:
                logs = json.load(f)
                if limit is not None and isinstance(limit, int):
                    return logs[-limit:]
                return logs
        except Exception as e:
            print(f"Failed to read logs: {e}")
            return []
    
    @staticmethod
    def clear_logs():
        """Очищает файл логов"""
        try:
            with open(LogsError.LOGS_FILE, 'w') as f:
                json.dump([], f)
        except Exception as e:
            print(f"Failed to clear logs: {e}")

class Logs:
    def __init__(self):
        self.filename = "logs.json"
        self.record = self.get_record()
    
    def save_result(self, moves, time_seconds):
        try:
            # Пытаемся загрузить существующие данные
            with open(self.filename, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"games": []}  # Если файла нет или он пуст, создаём новую структуру
        
        # Добавляем новую запись
        new_game = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "moves": moves,
            "time_seconds": time_seconds
        }
        data["games"].append(new_game)
        
        # Сохраняем обновлённые данные
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)
    
    def load_results(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
            return data["games"]
        except (FileNotFoundError, json.JSONDecodeError):
            return [{
                "date": 0,
                "moves": 0,
                "time_seconds": 0
            }]
    
    def get_record(self):
        games = self.load_results()
        
        if not games:
            return None  # Если нет игр в логах
        
        best_game = min(
            games,
            key=lambda game: game["time_seconds"]
        )
        
        return best_game


if __name__ == '__main__':
    log = Logs()
    