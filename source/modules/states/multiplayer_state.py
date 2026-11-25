import pygame
from .base_state import BaseState
from ..ui.panel import panel


class MultiplayerState(BaseState):
    """Tela base para o módulo Cliente/Servidor LAN (próxima etapa)."""
    def __init__(self, engine):
        super().__init__(engine)
        self.font_title = pygame.font.Font("assets/fonts/FreeSans.ttf", 40)
        self.font_text = pygame.font.Font("assets/fonts/FreeSans.ttf", 24)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
            from .menu_state import MenuState
            self.engine.change_state(MenuState(self.engine))

    def update(self, dt):
        pass

    def draw(self, screen):
        panel.draw_background(screen)
        w, h = screen.get_size()
        t1 = self.font_title.render("MULTIPLAYER LAN", True, (90, 220, 255))
        t2 = self.font_text.render("Modulo Cliente/Servidor em implementacao...", True, (230, 230, 230))
        t3 = self.font_text.render("Pressione ESC ou ENTER para voltar ao Menu", True, (255, 230, 100))
        screen.blit(t1, t1.get_rect(center=(w // 2, h // 2 - 50)))
        screen.blit(t2, t2.get_rect(center=(w // 2, h // 2 + 10)))
        screen.blit(t3, t3.get_rect(center=(w // 2, h // 2 + 65)))