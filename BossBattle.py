import Menus

from Game import *
from HighScore import *

class BossBattle(Game):
    def __init__(self, screen, playerClass, mutables):
        super(BossBattle, self).__init__(screen,
                                      playerClass, mutables,
                                      0, 0, 0,
                                      0, 0,
                                      1, 5,
                                      -100, -50,
                                      "Resources\\Generals\\bossbg.jpg")

        self.bonusScore = 10000
        self.boss = Boss(self.allSpriteList)
        self.bossQuote = pygame.image.load("Resources\\Generals\\quote.png")


    def processEvents(self):
        super().processEvents()
             
    def runLogic(self):
        if self.player.inBound and not self.pause and not self.gameOver:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
            
        if not self.pause:
            if not self.gameOver and not self.win:
                if self.boss.health <= 0:
                    self.win = True
                elif self.player.health <= 0:
                    self.gameOver = True

            if self.win:
                for thing in self.hazardList:
                    thing.kill()
                for box in self.boxList:
                    box.kill()
                    
                self.fireworkList.update(self)
                self.bonusScore -= 20
                self.score += 20

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

            self.allSpriteList.update(self)
            
            if len(self.fireworkList) == 0 and self.bonusScore <= 0:
                self.done = True               

    def displayFrame(self):
        super().displayFrame()

    def main(self):
        while not self.done:
            self.processEvents()
            self.runLogic()
            self.displayFrame()
            self.clock.tick(60)
        if not self.gameOver:
            HighScore(self.screen, self.playerClass, self.score, self.volume).main()
        else:
            Menus.MainMenu(self.screen).main()
            

