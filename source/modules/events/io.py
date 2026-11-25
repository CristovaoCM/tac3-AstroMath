import pygame
from ..game import game #instancia global do jogo



def io_events():
    # Coleta todos os eventos de input gerados pelo sistema
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
            
        elif event.type == pygame.KEYDOWN:
            # Sair do jogo
            if event.key == pygame.K_ESCAPE:
                game.running = False
                
            # Apagar o ultimo numero digitado
            elif event.key == pygame.K_BACKSPACE:
                game.input_text = game.input_text[:-1]
                
            # Validar a resposta ao apertar Enter
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                verificar_resposta()
                
            # Capturar teclado
            else:
                if event.unicode.isnumeric():
                    game.input_text += event.unicode

def verificar_resposta():
    resposta_digitada = game.input_text
    game.input_text = ""  
    
    cometa_alvo = None
    maior_y = -1000
    
    # Procura nos cometas ativos qual tem a resposta correta
    for cometa in game.cometas:
        if cometa.resposta == resposta_digitada:
            # Se houver mais de um com a mesma resposta prioriza o que está mais baixo na tela (maior y)
            if cometa.rect.y > maior_y:
                maior_y = cometa.rect.y
                cometa_alvo = cometa
                
    # Se encontrou destroi o cometa e toca o som
    if cometa_alvo:
        cometa_alvo.kill() 
        if game.som_acerto:
            game.som_acerto.play()