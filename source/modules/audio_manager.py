import os
import pygame
from .config.settings import settings


class AudioManager:
    """Singleton responsável por controlar músicas de fundo e volumes."""
    TRACKS = {
        "menu": ["assets/sounds/music_menu.ogg", "assets/sounds/music_menu.mp3", "assets/sounds/music_menu.wav"],
        "game": ["assets/sounds/music_game.ogg", "assets/sounds/music_game.mp3", "assets/sounds/music_game.wav"],
    }

    def __init__(self):
        self.current_track = None

    def _find_track_path(self, track_name):
        for path in self.TRACKS.get(track_name, []):
            if os.path.exists(path):
                return path
        return None

    def play_music(self, track_name):
        
        if self.current_track == track_name and pygame.mixer.music.get_busy():
            return

        path = self._find_track_path(track_name)
        if not path:
            return

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(settings.music_volume)
            pygame.mixer.music.play(-1)  # Loop infinito
            self.current_track = track_name
        except pygame.error as e:
            print(f"Aviso: nao foi possivel tocar {path}: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_track = None

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(max(0.0, min(1.0, float(volume))))


audio_manager = AudioManager()