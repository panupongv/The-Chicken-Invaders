import pygame
import random

from constants import *

from Hazards import *
from Deaths import *

class Chicken(pygame.sprite.Sprite):         
    def __init__(self, y, *group):
        super(Chicken, self).__init__(*group)

        self.moveX = random.randint(-2,2) * 3
        while self.moveX == 0:
            self.moveX = random.randint(-2,2) * 3
        self.moveY = 6
        self.health = 20
        self.slowLine = random.randint(275, 325)
        self.moveSlow = 2
        self.wingSpeed = 2
    
        self.index = random.randint(1,2)
        self.changer = -1
        self.counter = 0

        self.images = [pygame.image.load("Resources\\Sprites\\chicken1.png"),
                       pygame.image.load("Resources\\Sprites\\chicken2.png"),
                       pygame.image.load("Resources\\Sprites\\chicken3.png"),
                       pygame.image.load("Resources\\Sprites\\chicken4.png")]

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(11, 589 - self.rect.width)
        self.rect.y = y + random.randint(-30,30)
    
    def reset_pos(self):
        self.rect.y = random.randint(-300, - 20)
        self.rect.x = random.randint(10, 590 - self.rect.width)
        
    def update(self, game):
        if self.moveX < 0:
            self.image = pygame.transform.flip(self.images[self.index], True, False)
        else:
            self.image = self.images[self.index]
            
        if self.counter == 10:
            if self.index == 0 or self.index == 3:
                self.changer *= -1
            self.index += self.changer
            self.counter = 0
        self.counter += self.wingSpeed
        
        if self.rect.left < 10 or self.rect.right > 590:
            self.moveX *= -1
        self.rect.x += self.moveX
        if self.rect.y <= self.slowLine:
            self.rect.y += self.moveY
        else:
            self.rect.y += self.moveSlow

        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
        if self.health <= 0:
            self.kill(game, True)
            
        try:
            if not game.gameOver:
                self.checkHitPlayer(game)
            self.checkGotHit(game)
        except AttributeError:
            pass

    def checkGotHit(self, game):
        for bullet in pygame.sprite.spritecollide(self, game.bulletList, False):
            self.health -= game.player.damage
            game.score += int(game.player.damage * game.player.scoreRate)
            if not bullet.piercing:
                bullet.kill()

    def checkHitPlayer(self, game):
        if pygame.sprite.collide_rect(self, game.player):
            self.kill(game, True)
            game.player.takeDamage(game)

    def kill(self, game = None, inScreen = False):
        super().kill()
        if inScreen:
            death = Death(self, game.volume, 1, game.allSpriteList)

class BigChick(Chicken):
    def __init__(self, y, *group):
        super(BigChick, self).__init__(y, *group)
        self.moveY = 4
        self.health = 500
        self.slowLine = 150
        self.moveSlow = 1
        self.wingSpeed = 1

        self.images = [pygame.image.load("Resources\\Sprites\\bigchick1.png"),
                       pygame.image.load("Resources\\Sprites\\bigchick2.png"),
                       pygame.image.load("Resources\\Sprites\\bigchick3.png"),
                       pygame.image.load("Resources\\Sprites\\bigchick4.png")]
        self.rect = self.images[self.index].get_rect()
        self.rect.x = random.randint(11, 589 - self.rect.width)
        self.rect.y = y
            
class Bomber(Chicken):
    def __init__(self, leftBorder, rightBorder, *group):
        super(Bomber, self).__init__(random.randint(50, 150), *group)
        self.leftBorder = leftBorder
        self.rightBorder = rightBorder
        self.index = 1
        self.counter = 0
        self.changer = 1

        self.moveY = 0
        self.moveX = 10

        self.images = [pygame.image.load("Resources\\Sprites\\bomber1.png"),
                       pygame.image.load("Resources\\Sprites\\bomber2.png"),
                       pygame.image.load("Resources\\Sprites\\bomber3.png"),
                       pygame.image.load("Resources\\Sprites\\bomber4.png")]

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = self.leftBorder
        self.rect.y = 100
        
    def update(self, game):
        self.rect.x += self.moveX

        if self.rect.right > self.rightBorder or self.rect.left < self.leftBorder:
            self.moveX *= -1
            self.rect.y = random.randint(50, 150)
        if self.moveX < 0:
            self.image = pygame.transform.flip(self.images[self.index], True, False)
        else:
            self.image = self.images[self.index]
        if self.counter == 10:
            if self.index == 0 or self.index == 3:
                self.changer *= -1
            self.index += self.changer
            self.counter = 0
        self.counter += 1

        try:
            self.checkGotHit(game)
        except AttributeError:
            pass

    def checkGotHit(self, game):
        for bullet in pygame.sprite.spritecollide(self, game.bulletList, True):
            self.createBomb(game)
            bullet.kill()

    def createBomb(self, game):
        if 10 < self.rect.x < 590 - self.rect.width:
            if len(game.hazardList) - game.meteorNum < 1:
                egg = EggBomb(self, game.volume, game.hazardList, game.allSpriteList)
        
class Boss(pygame.sprite.Sprite):         
    def __init__(self, *group):
        super(Boss, self).__init__(*group)
        
        self.health = 20000
        self.mad = False

        self.index = 0
        self.image = pygame.image.load("Resources\\Sprites\\boss.png")
        self.cry = pygame.image.load("Resources\\Sprites\\bosscry.png")
        self.original = self.image

        self.color = [0, 255, 0]
        
        self.rect = self.image.get_rect()
        self.rect.x = 300 - self.rect.width//2
        self.rect.y = 31
        self.radius = 100

        self.moveX = 0
        self.moveY = 8
        self.madSpeed = 3

        self.roundTime = 0
        self.firstMove = True

    def update(self, game):
        if self.health > 0:
            if not self.mad:
                if self.roundTime > 50:
                    self.shootFireball(game)
                    self.mad = True
                    self.firstMove = True
                    self.roundTime = 0
                    self.madSpeed += 1
                self.image = self.original
                self.moveX = 0
                self.moveY = 0
                
            else:
                if self.roundTime > 400 and self.rect.y < 100 and 200 < self.rect.x + self.rect.width//2 < 400:
                    self.mad = False
                    self.roundTime = 0
                self.image = pygame.transform.rotate(self.image, 90)
                if self.firstMove:
                    if random.randint(0,1):
                        self.moveX = self.madSpeed
                    else:
                        self.moveX = -self.madSpeed
                    self.moveY = -self.madSpeed
                    self.firstMove = False
                if self.rect.x + self.rect.width >= 590 or self.rect.x <= 10:
                    self.moveX *= -1
                if self.rect.y + self.rect.height >= 690 or self.rect.y <= 10:
                    self.moveY *= -1

                if not game.gameOver:
                    self.checkHitPlayer(game)
                
            self.checkHitBullet(game)
                    
            self.rect.x += self.moveX
            self.rect.y += self.moveY
            self.roundTime += 1
        else:
            self.image = self.cry
        self.updateColor()

    def shootFireball(self, game):
        for i in range(-2, 3):
            fireball = Fireball(self, game.volume, i * 10, game.hazardList, game.allSpriteList)


    def checkHitPlayer(self, game):
        if pygame.sprite.collide_circle(self, game.player):
            game.player.takeDamage(game)
            self.moveX *= -1
            self.moveY *= -1

    def checkHitBullet(self, game):
        hitList = pygame.sprite.spritecollide(self, game.bulletList, True)
        for bullet in hitList:
            if not self.mad:
                self.health -= game.player.damage
            else:
                self.health -= game.player.damage//2

    def updateColor(self):
        if self.health > 10000:
            self.color[0] = (1 - ((self.health - 10000)/10000)) * 255
        else:
            self.color[0] = 255
            self.color[1] = self.health/10000 * 255

