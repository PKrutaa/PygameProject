import pygame
import sys
import interface

def main():

    running = True
    pygame.mixer.init()


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