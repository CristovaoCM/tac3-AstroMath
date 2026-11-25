import json
import os

SETTINGS_PATH = "source/data/settings.json"


class Settings:
    """Singleton que gerencia e persiste configurações do jogo."""
    def __init__(self):
        self.volume = 0.7
        self.music_volume = 0.5
        self.fullscreen = True
        self.show_fps = False
        self.selected_level = "fase_1.json"
        self.load()

    def load(self):
        if os.path.exists(SETTINGS_PATH):
            try:
                with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.volume = float(data.get("volume", 0.7))
                self.music_volume = float(data.get("music_volume", 0.5))
                self.fullscreen = bool(data.get("fullscreen", True))
                self.show_fps = bool(data.get("show_fps", False))
                self.selected_level = data.get("selected_level", "fase_1.json")
            except Exception:
                pass

    def save(self):
        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        data = {
            "volume": round(self.volume, 2),
            "music_volume": round(self.music_volume, 2),
            "fullscreen": self.fullscreen,
            "show_fps": self.show_fps,
            "selected_level": self.selected_level,
        }
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


settings = Settings()