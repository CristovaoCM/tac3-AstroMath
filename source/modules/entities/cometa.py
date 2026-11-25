import random
import pygame


class Cometa(pygame.sprite.Sprite):
    def __init__(self, x, y, operacao, resposta, velocidade):
        super().__init__()
        self.operacao = operacao
        self.resposta = str(resposta)
        self.velocidade = float(velocidade)

        tamanho = 115
        try:
            img_cometa = pygame.image.load("assets/image/cometa.png").convert_alpha()
            img_cometa = pygame.transform.scale(img_cometa, (tamanho, tamanho))
        except FileNotFoundError:
            img_cometa = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
            pygame.draw.circle(img_cometa, (210, 70, 50), (tamanho // 2, tamanho // 2), tamanho // 2)

        fonte = pygame.font.Font("assets/fonts/FreeSans.ttf", 28)
        sombra = fonte.render(self.operacao, True, (0, 0, 0))
        texto = fonte.render(self.operacao, True, (255, 255, 255))

        self.image = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
        self.image.blit(img_cometa, (0, 0))

        centro = (tamanho // 2, tamanho // 2)
        self.image.blit(sombra, sombra.get_rect(center=(centro[0] + 2, centro[1] + 2)))
        self.image.blit(texto, texto.get_rect(center=centro))

        self.rect = self.image.get_rect(center=(x, y))
        self.pos_y = float(self.rect.y)

    def update(self, dt):
        self.pos_y += self.velocidade * dt
        self.rect.y = int(self.pos_y)


class CometaFactory:
    """Factory Method para instanciar cometas conforme as regras da fase."""
    @staticmethod
    def criar_cometa(level_config, largura_tela, x_forcado=None):
        operacoes = level_config.get("operacoes") or ["+"]
        op = random.choice(operacoes)

        min_v = int(level_config.get("min_valor", 1))
        max_v = max(min_v, int(level_config.get("max_valor", 9)))
        vel_min = float(level_config.get("vel_min", 40.0))
        vel_max = max(vel_min, float(level_config.get("vel_max", 75.0)))

        a = random.randint(min_v, max_v)
        b = random.randint(min_v, max_v)

        if op == "+":
            expr, resp = f"{a} + {b}", a + b
        elif op == "-":
            if b > a:
                a, b = b, a
            expr, resp = f"{a} - {b}", a - b
        elif op == "*":
            expr, resp = f"{a} x {b}", a * b
        elif op == "/":
            pares_nao_triviais = [
                (dividendo, divisor)
                for dividendo in range(max(1, min_v), max_v + 1)
                for divisor in range(max(2, min_v), dividendo)
                if dividendo % divisor == 0
            ]
            if pares_nao_triviais:
                dividendo, divisor = random.choice(pares_nao_triviais)
            else:
                pares_validos = [
                    (dividendo, divisor)
                    for dividendo in range(max(1, min_v), max_v + 1)
                    for divisor in range(max(1, min_v), dividendo + 1)
                    if dividendo % divisor == 0
                ]
                dividendo, divisor = (
                    random.choice(pares_validos)
                    if pares_validos
                    else (max(1, min_v), max(1, min_v))
                )
            expr, resp = f"{dividendo} / {divisor}", dividendo // divisor
        else:
            expr, resp = f"{a} + {b}", a + b

        x = x_forcado if x_forcado is not None else random.randint(80, max(120, largura_tela - 80))
        velocidade = random.uniform(vel_min, vel_max)
        return Cometa(x, -60, expr, resp, velocidade)