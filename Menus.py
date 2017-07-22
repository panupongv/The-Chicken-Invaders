import pygame
import sys
import random

import GameLoop
import Instruction
import Ranking

from constants import *

from Buttons import *
from Doors import *

class StartScreen(object):
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.done = False
        pygame.mixer.music.load("Resources\\Musics\\intro.mp3")
        pygame.mixer.music.play()
        self.startImages = [pygame.image.load("Resources\\Menus\\sun1.jpg"),
                            pygame.image.load("Resources\\Menus\\sun2.jpg"),
                            pygame.image.load("Resources\\Menus\\sun3.jpg"),
                            pygame.image.load("Resources\\Menus\\sun4.jpg")]

    def eventsInput(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
    def main(self):
        index = 0
        counter = 0
        done = False
        while not done:
            done = self.eventsInput()
            self.screen.blit(self.startImages[index], (0,(700 - 563)//2))
            if counter >= 15:
                index = (index + 1) % 4
                counter = 0
            counter += 1
            self.clock.tick(60)
            pygame.display.update()
        MainMenu(self.screen).main()


class MainMenu(object):
    def __init__(self, screen):
        pygame.mouse.set_visible(True)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(4000)
        
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.index = 0
        self.counter = 0
        self.images = [pygame.image.load("Resources\\Menus\\default.jpg"),
                       pygame.image.load("Resources\\Menus\\flashing.jpg")]

        self.done = False
        self.choice = 0
        self.alreadyClick = False

        self.buttonList = pygame.sprite.Group()
        self.playBut = PlayButton(900 * 0.63, 68.5 + (563 * 0.2), self.buttonList)
        self.learnBut = LearnButton(900 * 0.63, 68.5 + (563 * 0.45), self.buttonList)
        self.rankingBut = RankingButton(900 * 0.63, 68.5 + (563 * 0.7), self.buttonList)
        self.quitBut = QuitButton(900 * 0.1, 68.5 + (563 * 0.7), self.buttonList)

        self.doorList = pygame.sprite.Group()
        self.upperDoor = UpperDoor(self.doorList)
        self.lowerDoor = LowerDoor(self.doorList)

        self.mouseX = 0
        self.mouseY = 0
        
    def eventsInput(self):
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.processChoice()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def processChoice(self):
        if self.choice:
            self.alreadyClick = True
            self.upperDoor.playSound()

    def displayFrame(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.images[self.index], [0,(SCREEN_HEIGHT - self.images[self.index].get_height())//2])
        self.buttonList.draw(self.screen)
        self.doorList.draw(self.screen)
        pygame.display.update()

    def runLogic(self):
        self.counter += random.randint(0,2)
        if self.counter % 50 == 0 or self.counter % 51 == 0 or \
           self.counter % 60 == 0 or self.counter % 61 == 0 or \
           self.counter % 62 == 0:
            self.index = 1
        else:
            self.index = 0
        if not self.alreadyClick:
            self.choice = 0
            for button in self.buttonList:
                if button.pointing:
                    self.choice = button.getChoice()
        self.buttonList.update(self)
        if self.alreadyClick:
            self.doorList.update(self)
        
    def main(self):
        while not self.done:
            self.eventsInput()
            self.displayFrame()
            self.runLogic()
            self.clock.tick(60)
        if self.choice == "Quit":
            pygame.quit()
            sys.exit()
        elif self.choice == "Play":
            CharacterSelect(self.screen).main()
        elif self.choice == "Learn":
            Instruction.Instruction(self.screen).main()
        elif self.choice == "Ranking":
            Ranking.Ranking(self.screen).main()


class CharacterSelect(object):
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.done = False
        self.playerClass = 1

        self.moveOn = False

        self.allSpriteList = pygame.sprite.Group()
        self.lowerDoor = SpecialLowerDoor(self.allSpriteList)
        self.upperDoor = SpecialUpperDoor(self.allSpriteList)

        self.tempBackground = pygame.image.load("Resources\\Generals\\level1.jpg")
        self.mask = pygame.image.load("Resources\\Generals\\background.png")
        self.leftArrow = pygame.image.load("Resources\\Generals\\arrow14.png")
        self.rightArrow = pygame.transform.flip(self.leftArrow, True, False)

        self.stats = [pygame.image.load("Resources\\Stats\\1stat.png"),
                      pygame.image.load("Resources\\Stats\\2stat.png"),
                      pygame.image.load("Resources\\Stats\\3stat.png"),
                      pygame.image.load("Resources\\Stats\\4stat.png")]
        

        self.mouseX = 0
        self.mouseY = 0

    def logics(self):        
        if self.moveOn:
            self.allSpriteList.update(self)
        
    def eventsInput(self):
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mouseX < 10 + self.leftArrow.get_width():
                    if self.playerClass > 1:
                        self.playerClass -= 1
                elif self.mouseX > SCREEN_WIDTH -self.leftArrow.get_width() - 10:
                    if self.playerClass < 4:
                        self.playerClass += 1
                else:
                    self.processChoice()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.playerClass > 1:
                        self.playerClass -= 1
                elif event.key == pygame.K_RIGHT:
                    if self.playerClass < 4:
                        self.playerClass += 1

    def processChoice(self):
        self.moveOn = True
        self.upperDoor.playSound()
               
    def displayFrame(self):
        self.screen.blit(self.tempBackground, [10, 10])
        self.screen.blit(self.mask, [0, 0])
        self.allSpriteList.draw(self.screen)
        if not self.moveOn:
            self.screen.blit(self.stats[self.playerClass - 1], [0, 0])
            if self.playerClass != 1:
                self.screen.blit(self.leftArrow, [10, SCREEN_HEIGHT//2 - self.leftArrow.get_height()//2])
            if self.playerClass != 4:
                self.screen.blit(self.rightArrow, [SCREEN_WIDTH - self.rightArrow.get_width() - 10,
                                                   SCREEN_HEIGHT//2 - self.leftArrow.get_height()//2])
        pygame.display.update()

    def main(self):
        while not self.done:
            self.eventsInput() 
            self.displayFrame()
            self.logics()
            self.clock.tick(60)
        GameLoop.GameLoop(self.screen, self.playerClass).main()
