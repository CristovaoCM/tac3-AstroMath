import pygame
from .base_state import BaseState
from ..ui.panel import panel
from ..config.settings import settings
from ..display import display
from ..audio_manager import audio_manager


class SettingsState(BaseState):
    def __init__(self, engine):
        super().__init__(engine)
        self.selected = 0
        self.font_title = pygame.font.Font("assets/fonts/FreeSans.ttf", 40)
        self.font_item = pygame.font.Font("assets/fonts/FreeSans.ttf", 26)
        self.font_small = pygame.font.Font("assets/fonts/FreeSans.ttf", 18)
        self.som_teste = None
        try:
            self.som_teste = pygame.mixer.Sound("assets/sounds/1up.wav")
        except Exception:
            pass

    def _aplicar_tela(self):
        flags = (pygame.SCALED | pygame.FULLSCREEN) if settings.fullscreen else pygame.SCALED
        display.screen = pygame.display.set_mode(display.size, flags, display=0, vsync=1)

    def _get_items(self):
        return [
            f"Volume dos Efeitos: < {int(round(settings.volume * 100))}% >",
            f"Volume da Musica: < {int(round(settings.music_volume * 100))}% >",
            f"Tela Cheia: < {'Sim' if settings.fullscreen else 'Nao'} >",
            f"Mostrar FPS: < {'Sim' if settings.show_fps else 'Nao'} >",
            "Salvar e Voltar ao Menu",
        ]

    def _alterar(self, delta):
        if self.selected == 0:
            settings.volume = round(max(0.0, min(1.0, settings.volume + delta * 0.1)), 2)
            if self.som_teste:
                self.som_teste.set_volume(settings.volume)
                self.som_teste.play()
        elif self.selected == 1:
            settings.music_volume = round(max(0.0, min(1.0, settings.music_volume + delta * 0.1)), 2)
            audio_manager.set_music_volume(settings.music_volume)
        elif self.selected == 2:
            settings.fullscreen = not settings.fullscreen
            self._aplicar_tela()
        elif self.selected == 3:
            settings.show_fps = not settings.show_fps

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        total = len(self._get_items())
        if event.key == pygame.K_ESCAPE:
            settings.save()
            from .menu_state import MenuState
            self.engine.change_state(MenuState(self.engine))
        elif event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % total
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % total
        elif event.key == pygame.K_LEFT:
            self._alterar(-1)
        elif event.key == pygame.K_RIGHT:
            self._alterar(1)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            if self.selected == 4:
                settings.save()
                from .menu_state import MenuState
                self.engine.change_state(MenuState(self.engine))
            else:
                self._alterar(1)

    def update(self, dt):
        pass

    def draw(self, screen):
        panel.draw_background(screen)
        w, h = screen.get_size()

        titulo = self.font_title.render("CONFIGURACOES", True, (90, 220, 255))
        screen.blit(titulo, titulo.get_rect(center=(w // 2, 75)))

        y = 155
        for idx, text in enumerate(self._get_items()):
            is_sel = idx == self.selected
            cor = (255, 255, 110) if is_sel else (230, 230, 230)
            surf = self.font_item.render(("> " if is_sel else "  ") + text, True, cor)
            screen.blit(surf, surf.get_rect(center=(w // 2, y)))
            y += 54

        dica = self.font_small.render("Setas Esq/Dir: Ajustar  |  Enter/ESC: Salvar e Voltar", True, (180, 190, 210))
        screen.blit(dica, dica.get_rect(center=(w // 2, h - 30)))