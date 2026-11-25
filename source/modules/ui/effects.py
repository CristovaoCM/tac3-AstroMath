import math
import random
import pygame


class EffectsManager:
    """Gerencia efeitos visuais: disparo do canhão, partículas e flashes de tela."""
    def __init__(self):
        self.clear()
        self._flash_surface = None
        self._flash_size = None

    def clear(self):
        self.beams = []          # Feixes de laser do canhão até o cometa
        self.rings = []          # Ondas de choque (explosão / impacto)
        self.particles = []      # Fagulhas da explosão
        self.cannon_recoil = 0.0 # Recuo vertical do canhão (pixels)
        self.flash_color = None
        self.flash_timer = 0.0
        self.flash_duration = 0.0
        self.flash_max_alpha = 0

    def trigger_screen_flash(self, color, duration=0.25, max_alpha=65):
        self.flash_color = color
        self.flash_duration = duration
        self.flash_timer = duration
        self.flash_max_alpha = max_alpha

    def trigger_shot(self, start_pos, target_pos):
        """Animação de disparo do canhão + explosão no cometa + flash verde."""
        self.cannon_recoil = 14.0
        self.beams.append({
            "start": start_pos,
            "end": target_pos,
            "timer": 0.24,
            "duration": 0.24,
        })

        # Anel de explosão no cometa e clarão na boca do canhão
        self.rings.append({"pos": target_pos, "radius": 10.0, "max_radius": 72.0, "color": (100, 255, 160), "timer": 0.28, "duration": 0.28})
        self.rings.append({"pos": start_pos, "radius": 6.0, "max_radius": 34.0, "color": (160, 240, 255), "timer": 0.16, "duration": 0.16})

        # Partículas saindo do cometa destruído
        for _ in range(14):
            ang = random.uniform(0, math.tau)
            vel = random.uniform(70.0, 210.0)
            self.particles.append({
                "x": float(target_pos[0]),
                "y": float(target_pos[1]),
                "vx": math.cos(ang) * vel,
                "vy": math.sin(ang) * vel,
                "color": random.choice([(100, 255, 150), (255, 240, 120), (140, 230, 255)]),
                "timer": 0.35,
                "duration": 0.35,
            })

        self.trigger_screen_flash((50, 255, 110), duration=0.22, max_alpha=55)

    def trigger_wrong_answer(self):
        """Leve flash amarelo na tela ao errar a conta."""
        self.trigger_screen_flash((255, 220, 40), duration=0.25, max_alpha=65)

    def trigger_ground_hit(self, impact_pos):
        """Onda de impacto + flash vermelho quando o cometa toca o solo."""
        self.rings.append({"pos": impact_pos, "radius": 12.0, "max_radius": 85.0, "color": (255, 80, 60), "timer": 0.35, "duration": 0.35})
        for _ in range(12):
            ang = random.uniform(math.pi, math.tau)  # Sobe a partir do chão
            vel = random.uniform(60.0, 180.0)
            self.particles.append({
                "x": float(impact_pos[0]),
                "y": float(impact_pos[1]),
                "vx": math.cos(ang) * vel,
                "vy": math.sin(ang) * vel,
                "color": random.choice([(255, 80, 60), (255, 160, 50), (255, 220, 120)]),
                "timer": 0.35,
                "duration": 0.35,
            })

        self.trigger_screen_flash((255, 45, 45), duration=0.35, max_alpha=90)

    def update(self, dt):
        # Recuperação recuo do canhão
        if self.cannon_recoil > 0:
            self.cannon_recoil = max(0.0, self.cannon_recoil - 75.0 * dt)

        # Flash de tela
        if self.flash_timer > 0:
            self.flash_timer = max(0.0, self.flash_timer - dt)

        # Feixes de laser
        for beam in self.beams:
            beam["timer"] -= dt
        self.beams = [b for b in self.beams if b["timer"] > 0]

        # Anéis de explosão
        for ring in self.rings:
            ring["timer"] -= dt
            progresso = 1.0 - max(0.0, ring["timer"] / ring["duration"])
            ring["radius"] = 10.0 + (ring["max_radius"] - 10.0) * progresso
        self.rings = [r for r in self.rings if r["timer"] > 0]

        # Partículas
        for p in self.particles:
            p["timer"] -= dt
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
        self.particles = [p for p in self.particles if p["timer"] > 0]

    def draw_world_effects(self, screen):
        """Desenha o disparo do canhão, anéis e partículas sobre o cenário."""
        for beam in self.beams:
            ratio = max(0.0, beam["timer"] / beam["duration"])
            largura_externa = max(2, int(14 * ratio))
            largura_nucleo = max(1, int(5 * ratio))

            pygame.draw.line(screen, (70, 235, 255), beam["start"], beam["end"], largura_externa)
            pygame.draw.line(screen, (255, 255, 255), beam["start"], beam["end"], largura_nucleo)
            pygame.draw.circle(screen, (180, 255, 255), beam["start"], max(3, int(14 * ratio)))

        for ring in self.rings:
            ratio = max(0.0, ring["timer"] / ring["duration"])
            espessura = max(1, int(5 * ratio))
            pygame.draw.circle(screen, ring["color"], (int(ring["pos"][0]), int(ring["pos"][1])), int(ring["radius"]), espessura)

        for p in self.particles:
            ratio = max(0.0, p["timer"] / p["duration"])
            raio = max(1, int(4 * ratio))
            pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), raio)

    def draw_screen_flash(self, screen):
        """Desenha a camada translúcida verde, amarela ou vermelha na tela."""
        if self.flash_timer <= 0 or not self.flash_color:
            return

        size = screen.get_size()
        if self._flash_size != size:
            self._flash_surface = pygame.Surface(size)
            self._flash_size = size

        ratio = self.flash_timer / self.flash_duration
        alpha = int(self.flash_max_alpha * ratio)
        if alpha > 0:
            self._flash_surface.fill(self.flash_color)
            self._flash_surface.set_alpha(alpha)
            screen.blit(self._flash_surface, (0, 0))