import pygame
from .base_state import BaseState
from ..entities.cometa import CometaFactory
from ..ui.panel import panel
from ..ui.effects import EffectsManager
from ..config.settings import settings
from ..audio_manager import audio_manager


class PlayState(BaseState):
    def __init__(self, engine, level_config, return_state_cls=None):
        super().__init__(engine)
        self.level_config = level_config
        self.return_state_cls = return_state_cls
        self.effects = EffectsManager()
        self.som_acerto = None
        try:
            self.som_acerto = pygame.mixer.Sound("assets/sounds/1up.wav")
            self.som_acerto.set_volume(settings.volume)
        except Exception:
            pass
        self._reset()

    def enter(self):
        audio_manager.play_music("game")

    def _reset(self):
        self.all_sprites = pygame.sprite.Group()
        self.cometas = pygame.sprite.Group()
        self.effects.clear()
        self.vidas = int(self.level_config.get("vidas", 3))
        self.meta_pontos = int(self.level_config.get("meta_pontos", 10))
        self.intervalo_spawn = float(self.level_config.get("intervalo_spawn", 3.5))
        self.nome_fase = self.level_config.get("nome", "AstroMath")
        self.pontos = 0
        self.tempo_spawn = self.intervalo_spawn * 0.7
        self.input_text = ""
        self.status = "playing"

    def _voltar(self):
        if self.return_state_cls:
            self.engine.change_state(self.return_state_cls(self.engine, self.level_config))
        else:
            from .menu_state import MenuState
            self.engine.change_state(MenuState(self.engine))

    def _get_cannon_muzzle(self):
        w, h = self.engine.get_screen_size()
        y_chao = h - panel.altura_chao
        return (w // 2, y_chao + 28)

    def _verificar_resposta(self):
        resp = self.input_text
        self.input_text = ""
        if not resp:
            return

        alvo = None
        maior_y = -1000
        for cometa in self.cometas:
            if cometa.resposta == resp and cometa.rect.y > maior_y:
                maior_y = cometa.rect.y
                alvo = cometa

        if alvo:
            # Disparo canhão até o centro do cometa
            self.effects.trigger_shot(self._get_cannon_muzzle(), alvo.rect.center)
            alvo.kill()
            self.pontos += 1
            if self.som_acerto:
                self.som_acerto.set_volume(settings.volume)
                self.som_acerto.play()

            if self.meta_pontos > 0 and self.pontos >= self.meta_pontos:
                self.status = "victory"
        else:
            # Errou a conta
            self.effects.trigger_wrong_answer()

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self._voltar()
            return

        if self.status != "playing":
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._reset()
            return

        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._verificar_resposta()
        elif event.unicode.isnumeric() and len(self.input_text) < 6:
            self.input_text += event.unicode

    def update(self, dt):
       
        self.effects.update(dt)

        if self.status != "playing":
            return

        self.all_sprites.update(dt)

        w, h = self.engine.get_screen_size()
        self.tempo_spawn += dt
        if self.tempo_spawn >= self.intervalo_spawn:
            novo = CometaFactory.criar_cometa(self.level_config, w)
            self.all_sprites.add(novo)
            self.cometas.add(novo)
            self.tempo_spawn = 0.0

        limite_chao = h - panel.altura_chao + 70
        for cometa in list(self.cometas):
            if cometa.rect.bottom >= limite_chao:
                # efeito vermelho
                self.effects.trigger_ground_hit((cometa.rect.centerx, limite_chao))
                cometa.kill()
                self.vidas -= 1
                if self.vidas <= 0:
                    self.status = "game_over"
                    self.input_text = ""

    def draw(self, screen):
        panel.draw_scenario(screen, cannon_recoil=self.effects.cannon_recoil)
        self.all_sprites.draw(screen)
        self.effects.draw_world_effects(screen)
        self.effects.draw_screen_flash(screen)
        panel.draw_hud(
            screen,
            self.vidas,
            self.pontos,
            self.meta_pontos,
            self.input_text,
            self.nome_fase,
            self.status,
        )