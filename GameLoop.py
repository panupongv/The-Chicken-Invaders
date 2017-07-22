import pygame

import Menus

import shortcuts

from Game import *
from BossBattle import *

class GameLoop(object):
    def __init__(self, screen, playerClass):
        self.screen = screen
        self.playerClass = playerClass
        
        self.gameOver = False
        self.mainScore = 0
        self.mainVolume = True
        self.musicPlayed = []

        self.mutables = [self.gameOver,
                         self.mainScore,
                         self.mainVolume,
                         self.musicPlayed]
        
    def main(self):
        for i in range(1, 6): 
            shortcuts.GameConstructor().get(i, self.screen, self.playerClass, self.mutables).main()
            self.gameOver = self.mutables[0]
            if self.gameOver:
                Menus.MainMenu(self.screen).main()
        if not self.gameOver:
            BossBattle(self.screen, self.playerClass, self.mutables).main()
           

            
    
    




    
