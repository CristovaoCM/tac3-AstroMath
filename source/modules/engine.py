import gc
import pygame
from .display import display
from .ui.panel import panel
from .config.settings import settings
from .states.menu_state import MenuState


class GameEngine:
    """Facade e Contexto da Máquina de Estados (Singleton)."""
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.init()

        display.create_display()
        if not settings.fullscreen:
            display.screen = pygame.display.set_mode(display.size, pygame.SCALED, display=0, vsync=1)

        panel.create()
        self.running = False
        self.state = None
        self.fps_font = pygame.font.Font("assets/fonts/FreeSans.ttf", 18)

    def change_state(self, new_state):
        self.state = new_state
        self.state.enter()

    def get_screen_size(self):
        return display.screen.get_size()

    def run(self):
        gc.disable()
        self.running = True
        self.change_state(MenuState(self))

        try:
            while self.running:
                display.game_tick()
                self.handle_events()
                self.update(display.delta_time)
                self.draw()
        except Exception as e:
            print(f"Erro na execucao: {e}")
            raise
        finally:
            pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.state:
                self.state.handle_event(event)

    def update(self, dt):
        if self.state:
            self.state.update(dt)

    def draw(self):
        if self.state:
            self.state.draw(display.screen)

        if settings.show_fps:
            fps_val = int(display.clock.get_fps())
            fps_surf = self.fps_font.render(f"FPS: {fps_val}", True, (180, 255, 180))
            display.screen.blit(fps_surf, (display.size[0] - 85, display.size[1] - 25))

        pygame.display.flip()


engine = GameEngine()