import pygame
import sys
import random

import shortcuts

from constants import *

from Enemies import *
from Items import *
from Hazards import *
from Projectiles import *

class Game(object):
    def __init__(self, screen,
                 playerClass, mutables,
                 chickenPerLine, chickenNum, chickenFrequency,
                 bigChickNum, bigChickFrequency,
                 meteorNum, boxNum,
                 bomberLeft, bomberRight,
                 picName):

        self.screen = screen       
        self.clock = pygame.time.Clock()
        self.mouseX, self.mouseY = pygame.mouse.get_pos()

        self.mutables = mutables
        self.gameOver = self.mutables[0]
        self.score = self.mutables[1]
        self.volume = self.mutables[2]
        self.musicPlayed = self.mutables[3]
        
        self.bonusScore = 0
        self.win = False
        self.pause = False
        self.done = False
        self.broken = False
        self.lost = False

        self.chickenPerLine = chickenPerLine
        self.chickenNum = chickenNum
        self.bigChickNum = bigChickNum
        self.meteorNum = meteorNum
        self.boxNum = boxNum

        self.bomberLeft = bomberLeft 
        self.bomberRight = bomberRight

        self.chickenFrequency = chickenFrequency
        self.bigChickFrequency = bigChickFrequency

        self.enemyList = pygame.sprite.Group()
        self.bulletList = pygame.sprite.Group()
        self.boxList = pygame.sprite.Group()
        self.itemList = pygame.sprite.Group()
        self.hazardList = pygame.sprite.Group()
        self.fireworkList = pygame.sprite.Group()
        self.allSpriteList = pygame.sprite.Group()

        self.picName = picName
        self.spaceBG = pygame.image.load(self.picName)
        self.HUD = pygame.image.load("Resources\\Generals\\background.png")
        self.pausemask = pygame.image.load("Resources\\Generals\\pausing.png")
        self.heart = pygame.image.load("Resources\\Generals\\heart.png")
        self.clear = pygame.image.load("Resources\\Generals\\clear.png")
        self.broke = pygame.image.load("Resources\\Generals\\broken.png")

        self.index = 0
        self.gameOverPics = [pygame.image.load("Resources\\Generals\\gonone.png"),
                             pygame.image.load("Resources\\Generals\\goquit.png"),
                             pygame.image.load("Resources\\Generals\\goretry.png")]

        self.volOn = pygame.image.load("Resources\\Generals\\volumeon.png")
        self.volOff = pygame.image.load("Resources\\Generals\\volumeoff.png")

        self.loseSound = pygame.mixer.Sound("Resources\\Sounds\\lose.wav")

        if not pygame.mixer.music.get_busy():
            self.trackNum = random.randint(0, 11)
            while self.trackNum in self.musicPlayed:
                self.trackNum = random.randint(0, 11)
            pygame.mixer.music.load("Resources\\Musics\\track" + str(self.trackNum) + ".mp3")
            pygame.mixer.music.play(-1, 0.0)
            self.mutables[3] = self.mutables[3] + [self.trackNum]

        self.font = pygame.font.Font("Resources\\Generals\\font.ttf", 25)
                
        for i in range(self.chickenNum):
            for j in range(self.chickenPerLine):
                chick = Chicken((i + 1) * -self.chickenFrequency, self.enemyList, self.allSpriteList)
                
        for i in range(self.bigChickNum):
            bigchick = BigChick((i + 1) * -self.bigChickFrequency, self.enemyList, self.allSpriteList)     

        if self.bomberRight > 0:
            self.bomber = Bomber(self.bomberLeft, self.bomberRight, self.allSpriteList)
            
        for i in range(self.boxNum):
            box = Box((i + 1) * random.randint(-600,-400), self.boxList, self.allSpriteList)

        for i in range(self.meteorNum):
            self.meteor = Meteor(self.hazardList, self.allSpriteList)

        for i in range(6):
            firework = Firework(self.fireworkList)

        self.playerClass = playerClass
        self.player = shortcuts.PlayerDict().get(self.playerClass, self.allSpriteList)
   
    def processEvents(self):
        self.mouseX, self.mouseY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SCREEN_WIDTH - self.volOn.get_width() - 20 < self.mouseX < SCREEN_WIDTH - 20 and \
                   SCREEN_HEIGHT - self.volOn.get_height() - 20 < self.mouseY < SCREEN_HEIGHT - 20:
                    self.volume = not self.volume
                    pygame.mixer.music.set_volume(float(self.volume))
                else:
                    if self.win:
                        if event.button == 2:
                            if pygame.mixer.music.get_busy():
                                pygame.mixer.music.stop()
                            if self.bonusScore > 0:
                                self.score += self.bonusScore
                            self.done = True
                    if self.gameOver:
                        if self.index == 1:
                            self.done = True
                        elif self.index == 2:
                            self.mutables[2] = self.volume
                            if self.__class__.__name__ == "Game":
                                self.mutables[1] -= 3000
                                self.__init__(self.screen,
                                              self.playerClass, self.mutables,
                                              self.chickenPerLine, self.chickenNum, self.chickenFrequency,
                                              self.bigChickNum, self.bigChickFrequency,
                                              self.meteorNum, self.boxNum,
                                              self.bomberLeft, self.bomberRight,
                                              self.picName)
                            elif self.__class__.__name__ == "BossBattle":
                                self.__init__(self.screen, self.playerClass, self.mutables)
                                
                    elif event.button == 1:
                        self.player.firing = True
                    elif event.button == 3:
                        self.player.special(self)
                    
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.player.firing = False
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.pause:
                        pygame.mouse.set_pos([self.player.rect.x + self.player.rect.width//2,
                                              self.player.rect.y + self.player.rect.height//2])
                    self.pause = not self.pause
    
    def runLogic(self):
        if self.player.inBound and not self.pause and not self.gameOver:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
            
        if not self.pause:
            if len(self.enemyList) == 0 and not self.gameOver:
                self.win = True
            elif self.player.health <= 0:
                self.gameOver = True
                  
            if self.win:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.fadeout(2000)
                for thing in self.hazardList:
                    thing.kill()
                for box in self.boxList:
                    box.kill()
                try:
                    self.bomber.kill()
                except AttributeError:
                    pass
                
                self.fireworkList.update(self)
                if self.bonusScore > 0:
                    self.bonusScore -= 10
                    self.score += 10
                
            elif self.gameOver:
                if 10 < self.mouseX < 300:
                    self.index = 1
                elif 300 < self.mouseX < 590:
                    self.index = 2
                else:
                    self.index = 0
                if not self.lost and self.volume:
                    pygame.mixer.Sound.play(self.loseSound)
                self.lost = True
                
            else:
                self.bonusScore = self.score * self.player.health//100

            self.allSpriteList.update(self)

            if len(self.fireworkList) == 0 and self.bonusScore < 0:
                self.done = True
             
    def displayFrame(self):  
        self.screen.blit(self.spaceBG, [10,10])
        self.allSpriteList.draw(self.screen)
        self.fireworkList.draw(self.screen)
            
        self.screen.blit(self.HUD, [0,0])

        if self.volume:
            currentVol = self.volOn
        else:
            currentVol = self.volOff
            
        self.screen.blit(currentVol, [SCREEN_WIDTH - 84,
                                      SCREEN_HEIGHT - 84])

        text = self.font.render("score: " + str(int(self.score)), True, WHITE)
        x = 625
        y = (SCREEN_HEIGHT//3 - text.get_height()//2)
        self.screen.blit(text,[x,y])

        for i in range(self.player.health):
            self.screen.blit(self.heart, (625 + (i * 32), SCREEN_HEIGHT*2//3 - self.heart.get_height()//2))

        tempCol = WHITE
        if self.player.haveSpecial:
            if random.randint(0,1):
                tempCol = RED
            textStr = "special ready!"
            text = self.font.render(textStr, True, tempCol)
            x = 625
            y = (SCREEN_HEIGHT//2 - text.get_height()//2)
            self.screen.blit(text,[x,y])
            
        try:
            if not self.boss.mad:
                self.screen.blit(self.bossQuote, [self.boss.rect.x + self.boss.rect.width*2//3,
                                                  self.boss.rect.y + self.boss.rect.height*2//3])
            pygame.draw.rect(self.screen, self.boss.color, (50, 20, self.boss.health//40, 20))
        except:
            pass

        if self.win:
            if self.bonusScore > 0:
                scoreStr = "bonus: " + str(int(self.bonusScore))
            else:
                scoreStr = "bonus: 0"
            text = self.font.render(scoreStr, True, WHITE)
            x = (SCREEN_WIDTH//3 - text.get_width()//2)
            y = (SCREEN_HEIGHT//2 - text.get_height()*5//2)
            self.screen.blit(text,[x,y])
            
            text = self.font.render("-middle mouse to skip-", True, WHITE)
            x = (SCREEN_WIDTH//3 - text.get_width()//2)
            y = (SCREEN_HEIGHT//2 + text.get_height()*3//2)
            self.screen.blit(text,[x,y])
            
            self.screen.blit(self.clear ,[300 - self.clear.get_width()//2,100])
            
        elif self.gameOver:
            self.screen.blit(self.gameOverPics[self.index], [10, 10])

        if self.broken:
            self.screen.blit(self.broke, [10, 10])

        if self.pause:
            self.screen.blit(self.pausemask, [10, 10])
            
        pygame.display.update()
        
        
    def main(self):
        while not self.done:
            self.processEvents()
            self.runLogic()
            self.displayFrame()
            self.clock.tick(60)
        self.mutables[0] = self.gameOver
        self.mutables[1] = int(self.score)
        self.mutables[2] = self.volume


