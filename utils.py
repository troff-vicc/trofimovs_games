import json
from datetime import datetime


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
            return []
    
    def get_record(self):
        games = self.load_results()
        
        if not games:
            return None  # Если нет игр в логах
        
        best_game = min(
            games,
            key=lambda game: game["moves"] * game["time_seconds"]
        )
        
        return best_game


if __name__ == '__main__':
    log = Logs()
    lo