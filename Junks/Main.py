import pygame
import random

from constants import *
from shortcuts import *

from Game import *
from BossBattle import *
from Menus import *
from HighScore import *
from Ranking import *

def main():
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.display.set_caption("The Chicken Invaders")
    pygame.mixer.init()

    StartScreen(screen).main()
    
    mainVolume = True
    while True:
        mainScore = 0
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(4000)
        pygame.mouse.set_visible(True)
        choice = MainMenu(screen).main()
        if choice == 1:
            playerClass = CharacterSelect(screen).main()
            for i in range(1, 6): #########
                gameOver, mainScore, mainVolume = eval(LevelDict().get(i)).main()
                if gameOver:
                    break
            #gameOver = False ########
            if not gameOver:
                BossBattle(screen, playerClass, mainScore, mainVolume).main()
        elif choice == 2:
            print("Instruction")
        elif choice == 3:
            Ranking(screen).main()
    pygame.quit()

        
if __name__ == "__main__":
    main()

    
    




    
