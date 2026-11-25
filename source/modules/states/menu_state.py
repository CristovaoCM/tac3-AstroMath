import pygame
from .base_state import BaseState
from ..ui.panel import panel
from ..config.settings import settings
from ..level_manager import level_manager
from ..audio_manager import audio_manager


class MenuState(BaseState):
    def enter(self):
        audio_manager.play_music("menu")
        
    def __init__(self, engine):
        super().__init__(engine)
        self.levels = level_manager.list_levels()
        if settings.selected_level in self.levels:
            self.level_idx = self.levels.index(settings.selected_level)
        else:
            self.level_idx = 0

        self.selected = 0
        self.option_rects = []
        self.font_title = pygame.font.Font("assets/fonts/FreeSans.ttf", 48)
        self.font_item = pygame.font.Font("assets/fonts/FreeSans.ttf", 26)
        self.font_hint = pygame.font.Font("assets/fonts/FreeSans.ttf", 18)

    def _get_options(self):
        fase_atual = self.levels[self.level_idx] if self.levels else "fase_1.json"
        return [
            "Novo Jogo",
            f"Fase Selecionada: < {fase_atual} >",
            "Editor de Fases",
            "Configuracoes",
            "Multiplayer (LAN)",
            "Sair",
        ]

    def _activate_option(self):
        from .play_state import PlayState
        from .editor_state import EditorState
        from .settings_state import SettingsState
        from .multiplayer_state import MultiplayerState

        if self.selected == 0:
            fase = self.levels[self.level_idx]
            settings.selected_level = fase
            settings.save()
            config = level_manager.load_level(fase)
            self.engine.change_state(PlayState(self.engine, config))
        elif self.selected == 1:
            self.level_idx = (self.level_idx + 1) % len(self.levels)
        elif self.selected == 2:
            self.engine.change_state(EditorState(self.engine))
        elif self.selected == 3:
            self.engine.change_state(SettingsState(self.engine))
        elif self.selected == 4:
            self.engine.change_state(MultiplayerState(self.engine))
        elif self.selected == 5:
            self.engine.running = False

    def handle_event(self, event):
        options = self._get_options()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(options)
            elif event.key == pygame.K_LEFT and self.selected == 1:
                self.level_idx = (self.level_idx - 1) % len(self.levels)
            elif event.key == pygame.K_RIGHT and self.selected == 1:
                self.level_idx = (self.level_idx + 1) % len(self.levels)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._activate_option()
            elif event.key == pygame.K_ESCAPE:
                self.engine.running = False

        elif event.type == pygame.MOUSEMOTION:
            for idx, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected = idx

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected = idx
                    self._activate_option()
                    break

    def update(self, dt):
        pass

    def draw(self, screen):
        panel.draw_background(screen)
        w, h = screen.get_size()

        titulo = self.font_title.render("ASTROMATH", True, (90, 220, 255))
        screen.blit(titulo, titulo.get_rect(center=(w // 2, 75)))

        options = self._get_options()
        self.option_rects = []
        start_y = 160
        step_y = 52

        for idx, text in enumerate(options):
            is_sel = idx == self.selected
            rect = pygame.Rect(0, 0, 460, 42)
            rect.center = (w // 2, start_y + idx * step_y)
            self.option_rects.append(rect)

            bg_color = (35, 90, 140) if is_sel else (20, 28, 50)
            border_color = (100, 230, 255) if is_sel else (70, 90, 120)
            txt_color = (255, 255, 120) if is_sel else (230, 230, 230)

            pygame.draw.rect(screen, bg_color, rect, border_radius=8)
            pygame.draw.rect(screen, border_color, rect, 2, border_radius=8)

            surf = self.font_item.render(text, True, txt_color)
            screen.blit(surf, surf.get_rect(center=rect.center))

        dica = self.font_hint.render("Setas/Mouse: Navegar  |  Enter/Clique: Confirmar", True, (180, 190, 210))
        screen.blit(dica, dica.get_rect(center=(w // 2, h - 25)))