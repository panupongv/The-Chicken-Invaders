import pygame

from constants import *

from Menus import *

class TheChickenInvaders(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Chicken Invaders")
        pygame.display.set_icon(pygame.image.load("Resources\\Generals\\redicon.png"))
        pygame.mixer.init()

        self.screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

    def main(self):
        StartScreen(self.screen).main()
    
   
    




    
