import pygame

import Menus

from constants import *

from Doors import *
from ScoreProcessor import *

class HighScore(object):
    def __init__(self, screen, playerClass, score, volume):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.score = score
        self.playerClass = playerClass

        if volume:
            winSound = pygame.mixer.Sound("Resources\\Sounds\\win.wav")
            pygame.mixer.Sound.play(winSound) 
        
        self.name = ""
        self.background = pygame.image.load("Resources\\Generals\\party.jpg")
        self.font = pygame.font.Font("Resources\\Generals\\font.ttf", 40)

        self.done = False
        self.alreadyClick = False

        self.doorList = pygame.sprite.Group()
        self.upperDoor = UpperDoor(self.doorList)
        self.lowerDoor = LowerDoor(self.doorList)

        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        
    def eventsInput(self):
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.name += chr(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.processChoice()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def processChoice(self):
        self.alreadyClick = True
        self.upperDoor.playSound()

    def displayFrame(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, [0, 0])
        text = self.font.render("your score: " + str(self.score), True, WHITE)
        x = SCREEN_WIDTH//2 - text.get_width()//2
        y = SCREEN_HEIGHT*3//5 + text.get_height()//2
        self.screen.blit(text,[x,y])
        
        text = self.font.render("enter your name: " + self.name, True, WHITE)
        x = SCREEN_WIDTH//2 - text.get_width()//2
        y = SCREEN_HEIGHT*4//5 - text.get_height()//2
        self.screen.blit(text,[x,y])
        
        self.doorList.draw(self.screen)
        pygame.display.update()

    def runLogic(self):
        if len(self.name):
            lastChar = ord(self.name[-1:])
            if lastChar == 8:
                self.name = self.name[:-2]
            elif lastChar == 13:
                self.name = self.name[:-1]
                self.processChoice()
            elif lastChar not in range(49, 58) and lastChar not in range(65, 91) and lastChar not in range(97, 123):
                self.name = self.name[:-1]
        if self.alreadyClick:
            self.doorList.update(self)
        
    def main(self):
        while not self.done:
            self.displayFrame()
            self.eventsInput()
            self.runLogic()
            self.clock.tick(60)
        ScoreProcessor().writeScore(self.score, self.name.strip(), self.playerClass)
        Menus.MainMenu(self.screen).main()

