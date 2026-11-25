import pygame
from ..display import display


class Panel:
    def __init__(self):
        self.font_title = None
        self.font_hud = None
        self.font_small = None
        self.bg = None
        self.img_chao = None
        self.img_astronauta = None
        self.img_canhao = None
        self.altura_chao = 150

    def create(self):
        self.font_title = pygame.font.Font("assets/fonts/FreeSans.ttf", 44)
        self.font_hud = pygame.font.Font("assets/fonts/FreeSans.ttf", 32)
        self.font_small = pygame.font.Font("assets/fonts/FreeSans.ttf", 22)

        try:
            fundo_orig = pygame.image.load("assets/image/back.jpg").convert()
            self.bg = pygame.transform.scale(fundo_orig, display.size)
        except FileNotFoundError:
            self.bg = pygame.Surface(display.size)
            self.bg.fill((10, 12, 28))

        try:
            chao_orig = pygame.image.load("assets/image/chao.png").convert_alpha()
            self.img_chao = pygame.transform.scale(chao_orig, (display.size[0], self.altura_chao))
        except FileNotFoundError:
            self.img_chao = pygame.Surface((display.size[0], self.altura_chao))
            self.img_chao.fill((70, 75, 90))

        try:
            astro_orig = pygame.image.load("assets/image/astronauta.png").convert_alpha()
            self.img_astronauta = pygame.transform.scale(astro_orig, (80, 80))
        except FileNotFoundError:
            self.img_astronauta = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.rect(self.img_astronauta, (100, 200, 255), (0, 0, 80, 80))

        try:
            canhao_orig = pygame.image.load("assets/image/canhao.png").convert_alpha()
            self.img_canhao = pygame.transform.scale(canhao_orig, (100, 100))
        except FileNotFoundError:
            self.img_canhao = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.polygon(self.img_canhao, (220, 200, 40), [(0, 100), (50, 0), (100, 100)])

    def draw_background(self, screen):
        screen.blit(self.bg, (0, 0))

    def draw_scenario(self, screen, cannon_recoil=0):
        self.draw_background(screen)
        w, h = display.size
        y_chao = h - self.altura_chao
        screen.blit(self.img_chao, (0, y_chao))
        screen.blit(self.img_canhao, (w // 2 - 50, y_chao + 20 + int(cannon_recoil)))
        screen.blit(self.img_astronauta, (w // 2 - 150, y_chao + 40))

    def draw_hud(self, screen, vidas, pontos, meta, input_text, nome_fase, status="playing"):
        w, h = display.size

        # Barra superior
        txt_vidas = self.font_hud.render(f"Vidas: {vidas}", True, (255, 230, 80))
        screen.blit(txt_vidas, (20, 15))

        meta_str = f"{pontos}/{meta}" if meta > 0 else f"{pontos}"
        txt_pts = self.font_hud.render(f"Pontos: {meta_str}", True, (120, 255, 160))
        screen.blit(txt_pts, (w - txt_pts.get_width() - 20, 15))

        txt_fase = self.font_small.render(nome_fase, True, (200, 220, 255))
        screen.blit(txt_fase, txt_fase.get_rect(center=(w // 2, 28)))

        if status == "game_over":
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            go = self.font_title.render("GAME OVER!", True, (255, 70, 70))
            sub = self.font_small.render("ENTER: Tentar novamente  |  ESC: Menu Principal", True, (240, 240, 240))
            screen.blit(go, go.get_rect(center=(w // 2, h // 2 - 25)))
            screen.blit(sub, sub.get_rect(center=(w // 2, h // 2 + 30)))

        elif status == "victory":
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            vic = self.font_title.render("FASE CONCLUIDA!", True, (80, 255, 120))
            sub = self.font_small.render("ENTER: Jogar novamente  |  ESC: Menu Principal", True, (240, 240, 240))
            screen.blit(vic, vic.get_rect(center=(w // 2, h // 2 - 25)))
            screen.blit(sub, sub.get_rect(center=(w // 2, h // 2 + 30)))

        else:
            if input_text:
                texto, cor = f"Resposta: {input_text}", (80, 255, 100)
            else:
                texto, cor = "Digite o resultado e tecle Enter...", (255, 235, 80)

            surf = self.font_hud.render(texto, True, cor)
            screen.blit(surf, surf.get_rect(center=(w // 2, h - 22)))


panel = Panel()