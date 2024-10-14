import pygame
import sys
import interface

def main():

    running = True
    pygame.mixer.init()
    pygame.mixer.music.load(r"Musicas\song1.wav")
    pygame.mixer.music.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        interface.homepage()

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()