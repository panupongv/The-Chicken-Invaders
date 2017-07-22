import pygame

from constants import *

from Bullets import *
from Projectiles import *
from Deaths import *

class Player(pygame.sprite.Sprite):
    def  __init__(self, *group):
        super(Player, self).__init__(*group)

        self.firing = False
        self.haveSpecial = False
        self.inBound = True
        self.scoreRate = 1

        self.counter = 0
        self.index = 0
    
        self.bulletCounter = 20
        self.bulletLimit = 20
        
    def update(self, game):
        if game.gameOver:
            self.kill()
        if self.counter >= 5:
            self.index = (self.index + 1) % 2
            self.image = self.images[self.index]
            self.counter = 0
        self.counter += 1
        if game.mouseX + self.rect.width//2 < 590 and game.mouseX - self.rect.width//2 > 10 \
           and game.mouseY - self.rect.height//2 > 10 and game.mouseY + self.rect.height//2 < 690:
            self.rect.x = game.mouseX - self.rect.width//2
            self.rect.y = game.mouseY - self.rect.height//2
            self.inBound = True
        else:
            self.inBound = False

        if self.firing:
            self.bulletCounter += self.fireRate
            if self.bulletCounter >= self.bulletLimit:
                self.fireBullet(game)
                self.bulletCounter = 0
        else:
            self.bulletCounter = self.bulletLimit
        self.getItem(game)

    def fireBullet(self, game):
        pass

    def special(self, game):
        pass

    def takeDamage(self, game):
        playerDeath = PlayerDeath(self, game.volume, 1, game.allSpriteList)
        self.health -= 1

    def getItem(self, game):
        getList = pygame.sprite.spritecollide(self, game.itemList, True)
        for item in getList:
            item.getPower(game)
        

class Ship1(Player):
    def __init__(self, *group):
        super(Ship1, self).__init__(*group)
        self.health = 3
        self.damage = 18
        self.fireRate = 2
        self.images = [pygame.image.load("Resources\\Sprites\\ship11.png"),
                       pygame.image.load("Resources\\Sprites\\ship12.png")]
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.radius = self.rect.width//2
        self.piercing = True

    def update(self, game):
        super().update(game)

    def fireBullet(self, game):
        bullet = Bullet1(self, game.volume, 1, 0, game.bulletList, game.allSpriteList)

    def special(self, game):
        if self.haveSpecial:
            for i in range(60):
                bullet = Bullet1(self, game.volume, 2, random.randint(-45,45), game.bulletList, game.allSpriteList)
                bullet.speed = random.randint(25,35)
            self.haveSpecial = False

        
class Ship2(Player):
    def __init__(self, *group):
        super(Ship2, self).__init__(*group)
        self.health = 5
        self.damage = 10
        self.fireRate = 4
        self.images = [pygame.image.load("Resources\\Sprites\\ship21.png"),
                       pygame.image.load("Resources\\Sprites\\ship22.png")]
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.radius = self.rect.width//2
        self.piercing = False

        self.specialCounter = 0
        self.branch = 1

    def update(self, game):
        super().update(game)
        if self.branch > 1:
            self.specialCounter += 1
        if self.specialCounter > 150:
            self.branch -= 1
            self.specialCounter = 0
            

    def fireBullet(self, game):
        for i in range(2):
            for j in range(-self.branch + 1, self.branch):
                bullet = Bullet2(self, game.volume, not i and not j, (self.rect.x + 7 + (i * 43)), (j * 20),
                                 game.bulletList, game.allSpriteList)

    def special(self, game):
        if self.haveSpecial:
            self.branch += 1
            self.haveSpecial = False

class Ship3(Player):
    def __init__(self, *group):
        super(Ship3, self).__init__(*group)
        self.health = 4
        self.damage = 15
        self.fireRate = 3
        self.images = [pygame.image.load("Resources\\Sprites\\ship31.png"),
                       pygame.image.load("Resources\\Sprites\\ship32.png")]
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.radius = self.rect.width//2
        self.piercing = False    

    def update(self, game):
        super().update(game)

    def fireBullet(self, game):
        bullet = Bullet3(self, game.volume, 1, 0, game.bulletList, game.allSpriteList)

    def special(self, game):
        if self.haveSpecial:
            missile = Missile(self, game.volume, game.allSpriteList)
            self.haveSpecial = False

class Ship4(Player):
    def __init__(self, *group):
        super(Ship4, self).__init__(*group)
        self.health = 4
        self.damage = 25
        self.fireRate = 1
        self.images = [pygame.image.load("Resources\\Sprites\\ship41.png"),
                       pygame.image.load("Resources\\Sprites\\ship42.png")]
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.radius = self.rect.width//2
        self.piercing = True

        self.specialCounter = 0
    
    def update(self, game):
        if game.gameOver:
            self.kill()
        self.image = self.images[int(self.firing)]
        pos = pygame.mouse.get_pos()
        if game.mouseX + self.rect.width//2 < 590 and game.mouseX - self.rect.width//2 > 10 \
           and game.mouseY - self.rect.height//2 > 10 and game.mouseY + self.rect.height//2 < 690:
            self.rect.x = game.mouseX - self.rect.width//2
            self.rect.y = game.mouseY - self.rect.height//2
            self.inBound = True
        else:
            self.inBound = False
            
        if self.firing:
            self.bulletCounter += self.fireRate
            if self.bulletCounter >= self.bulletLimit:
                self.fireBullet(game)
                self.bulletCounter = 0
        else:
            self.bulletCounter = self.bulletLimit
                
        if self.fireRate >= 100:
            self.specialCounter += 1
        if self.specialCounter >= 150:
            self.fireRate = 2
            self.specialCounter = 0
            
        self.getItem(game)

    def fireBullet(self, game):
        if self.fireRate < 100:
            bullet = Bullet4(self, game.volume, 1, 0, game.bulletList, game.allSpriteList)
        else:
            bullet = Bullet4(self, game.volume, 2, random.randint(-5,5), game.bulletList, game.allSpriteList)

    def special(self, game):
        if self.haveSpecial:
            self.fireRate += 100
            self.haveSpecial = False
    
