import pygame
import sys
import interface
import game_loop as gm
import geracao_mapa as gm_mapa

def quit_game():
    pygame.quit()
    sys.exit()

def main():

    running = True
    pygame.mixer.init()
    pygame.mixer.music.load(r"Musicas\song1.wav")
    pygame.mixer.music.play(-1)

    #loop inicialização
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Desenhar a imagem de fundo
        
        interface.homepage()

        
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()