import pygame
import random
from .entities.cometa import Cometa

class Game:
    def __init__(self):
        self.running = False
        self.game_over = False
        self.vidas = 3 

        # Grupos de sprites do Pygame
        self.all_sprites = pygame.sprite.Group()
        self.cometas = pygame.sprite.Group() 
        
        # Variáveis de controle do jogo
        self.tempo_spawn = 0
        self.input_text = ""
        self.som_acerto = None 

    def init_assets(self):
        # som
        self.som_acerto = pygame.mixer.Sound("assets/sounds/1up.wav")
    

    def start(self):
        self.running = True

    def stop(self):
        self.running = False



    def update(self, dt):
        
        if self.game_over:
            return

        #Atualiza a fisica
        self.all_sprites.update(dt)

        #Gerencia o nascimento de novos cometas
        self.tempo_spawn += dt
        if self.tempo_spawn > 4.0:
            x_aleatorio = random.randint(100, 700)
            novo_cometa = Cometa(x_aleatorio, -50)
            self.all_sprites.add(novo_cometa)
            self.cometas.add(novo_cometa)
            self.tempo_spawn = 0

        #Verifica a colisao com o chao
        altura_chao_y = pygame.display.get_surface().get_height() - 15
        
        for cometa in self.cometas:
            
            if cometa.rect.bottom >= altura_chao_y:
                cometa.kill() 
                self.vidas -= 1
                
                if self.vidas <= 0:
                    self.game_over = True
                    self.input_text = ""
game = Game()
