import pygame
from .base_state import BaseState
from ..ui.panel import panel
from ..level_manager import level_manager, DEFAULT_LEVEL
from ..entities.cometa import CometaFactory
from ..config.settings import settings
from ..audio_manager import audio_manager


class EditorState(BaseState):
    def enter(self):
        audio_manager.play_music("menu")
        
    def __init__(self, engine, initial_config=None):
        super().__init__(engine)
        self.config = (initial_config or DEFAULT_LEVEL).copy()
        self.config["operacoes"] = list(self.config.get("operacoes", ["+"]))
        self.filename = "fase_custom"
        self.selected = 0
        self.feedback = ""
        self.feedback_timer = 0.0
        self.preview_cometa = None

        self.font_title = pygame.font.Font("assets/fonts/FreeSans.ttf", 34)
        self.font_item = pygame.font.Font("assets/fonts/FreeSans.ttf", 22)
        self.font_small = pygame.font.Font("assets/fonts/FreeSans.ttf", 18)
        self._atualizar_preview()

    def _atualizar_preview(self):
        self.preview_cometa = CometaFactory.criar_cometa(self.config, 800, x_forcado=0)

    def _get_fields(self):
        ops_str = "  ".join(
            f"[{op}]" if op in self.config["operacoes"] else f" {op} "
            for op in ["+", "-", "*", "/"]
        )
        meta = self.config["meta_pontos"]
        meta_txt = "Infinito (0)" if meta == 0 else str(meta)

        return [
            ("Nome do Arquivo", f"{self.filename}.json"),
            ("Nome da Fase", self.config["nome"]),
            ("Operacoes (1-4)", ops_str),
            ("Valor Minimo", str(self.config["min_valor"])),
            ("Valor Maximo", str(self.config["max_valor"])),
            ("Velocidade Max", f"{int(self.config['vel_max'])} px/s"),
            ("Intervalo Spawn", f"{self.config['intervalo_spawn']:.1f} s"),
            ("Vidas Iniciais", str(self.config["vidas"])),
            ("Meta de Acertos", meta_txt),
            ("SALVAR FASE (JSON)", ""),
            ("TESTAR FASE AGORA", ""),
            ("Voltar ao Menu", ""),
        ]

    def _toggle_op(self, op):
        ops = self.config["operacoes"]
        if op in ops and len(ops) > 1:
            ops.remove(op)
        elif op not in ops:
            ops.append(op)
        self._atualizar_preview()

    def _adjust_value(self, delta):
        idx = self.selected
        if idx == 3:  # min_valor
            self.config["min_valor"] = max(1, min(self.config["max_valor"], self.config["min_valor"] + delta))
        elif idx == 4:  # max_valor
            self.config["max_valor"] = max(self.config["min_valor"], min(99, self.config["max_valor"] + delta))
        elif idx == 5:  # vel_max
            self.config["vel_max"] = max(40.0, min(250.0, self.config["vel_max"] + delta * 10))
            self.config["vel_min"] = max(25.0, self.config["vel_max"] - 35.0)
        elif idx == 6:  # intervalo_spawn
            self.config["intervalo_spawn"] = round(max(0.8, min(8.0, self.config["intervalo_spawn"] + delta * 0.2)), 1)
        elif idx == 7:  # vidas
            self.config["vidas"] = max(1, min(10, self.config["vidas"] + delta))
        elif idx == 8:  # meta_pontos
            self.config["meta_pontos"] = max(0, min(100, self.config["meta_pontos"] + delta * 5))
        self._atualizar_preview()

    def _trigger_action(self):
        if self.selected == 9:  # Salvar
            nome_limpo = self.filename.strip() or "fase_custom"
            saved = level_manager.save_level(nome_limpo, self.config)
            settings.selected_level = saved
            settings.save()
            self.feedback = f"Salvo em source/data/levels/{saved}!"
            self.feedback_timer = 3.0
        elif self.selected == 10:  # Testar
            from .play_state import PlayState
            self.engine.change_state(PlayState(self.engine, self.config.copy(), return_state_cls=EditorState))
        elif self.selected == 11:  # Voltar
            from .menu_state import MenuState
            self.engine.change_state(MenuState(self.engine))

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        total = len(self._get_fields())
        if event.key == pygame.K_ESCAPE:
            from .menu_state import MenuState
            self.engine.change_state(MenuState(self.engine))
            return

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % total
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % total
        elif event.key == pygame.K_LEFT:
            self._adjust_value(-1)
        elif event.key == pygame.K_RIGHT:
            self._adjust_value(1)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._trigger_action()
        elif self.selected == 2:
            mapa = {pygame.K_1: "+", pygame.K_2: "-", pygame.K_3: "*", pygame.K_4: "/"}
            if event.key in mapa:
                self._toggle_op(mapa[event.key])
        elif self.selected == 0:  # Editar nome do arquivo
            if event.key == pygame.K_BACKSPACE:
                self.filename = self.filename[:-1]
            elif (event.unicode.isalnum() or event.unicode in "_-") and len(self.filename) < 20:
                self.filename += event.unicode
        elif self.selected == 1:  # Editar nome visível da fase
            if event.key == pygame.K_BACKSPACE:
                self.config["nome"] = self.config["nome"][:-1]
            elif event.unicode.isprintable() and len(self.config["nome"]) < 26:
                self.config["nome"] += event.unicode

    def update(self, dt):
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            if self.feedback_timer <= 0:
                self.feedback = ""

    def draw(self, screen):
        panel.draw_background(screen)
        w, h = screen.get_size()

        titulo = self.font_title.render("EDITOR DE FASES", True, (90, 220, 255))
        screen.blit(titulo, (40, 20))

        fields = self._get_fields()
        y = 75
        for idx, (label, val) in enumerate(fields):
            is_sel = idx == self.selected
            cor = (255, 255, 110) if is_sel else (225, 225, 225)
            prefixo = "> " if is_sel else "  "
            texto = f"{prefixo}{label}: {val}" if val else f"{prefixo}[ {label} ]"
            if idx == 9:
                cor = (100, 255, 140) if is_sel else (70, 200, 110)
            elif idx == 10:
                cor = (120, 220, 255) if is_sel else (80, 170, 220)

            surf = self.font_item.render(texto, True, cor)
            screen.blit(surf, (40, y))
            y += 34

        # Painel preview
        box = pygame.Rect(w - 280, 90, 240, 240)
        pygame.draw.rect(screen, (20, 28, 50), box, border_radius=12)
        pygame.draw.rect(screen, (90, 200, 255), box, 2, border_radius=12)

        lbl_prev = self.font_small.render("Preview do Cometa", True, (200, 220, 255))
        screen.blit(lbl_prev, lbl_prev.get_rect(center=(box.centerx, box.top + 25)))

        if self.preview_cometa:
            screen.blit(self.preview_cometa.image, self.preview_cometa.image.get_rect(center=(box.centerx, box.centery + 10)))
            resp_txt = self.font_small.render(f"Resp: {self.preview_cometa.resposta}", True, (120, 255, 150))
            screen.blit(resp_txt, resp_txt.get_rect(center=(box.centerx, box.bottom - 22)))

        if self.feedback:
            fb = self.font_small.render(self.feedback, True, (100, 255, 140))
            screen.blit(fb, (40, h - 55))

        dica = self.font_small.render("Cima/Baixo: Campo | Esq/Dir: Ajustar | Teclas 1-4: Operacoes | Enter: Acao", True, (180, 190, 210))
        screen.blit(dica, (40, h - 28))