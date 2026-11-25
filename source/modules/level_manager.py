import json
import os

LEVELS_DIR = "source/data/levels"

DEFAULT_LEVEL = {
    "nome": "Fase 1 - Soma Basica",
    "operacoes": ["+"],
    "min_valor": 1,
    "max_valor": 9,
    "vel_min": 40.0,
    "vel_max": 75.0,
    "intervalo_spawn": 3.5,
    "vidas": 3,
    "meta_pontos": 10,
}


class LevelManager:
    """Gerencia a criação, listagem e carregamento de fases em JSON."""
    def __init__(self):
        os.makedirs(LEVELS_DIR, exist_ok=True)
        self._ensure_default_level()

    def _ensure_default_level(self):
        default_path = os.path.join(LEVELS_DIR, "fase_1.json")
        if not os.path.exists(default_path):
            self.save_level("fase_1.json", DEFAULT_LEVEL)

    def list_levels(self):
        self._ensure_default_level()
        arquivos = [f for f in os.listdir(LEVELS_DIR) if f.endswith(".json")]
        arquivos.sort()
        return arquivos

    def load_level(self, filename):
        path = os.path.join(LEVELS_DIR, filename)
        if not os.path.exists(path):
            return DEFAULT_LEVEL.copy()
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_level(self, filename, data):
        if not filename.endswith(".json"):
            filename += ".json"
        path = os.path.join(LEVELS_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return filename


level_manager = LevelManager()