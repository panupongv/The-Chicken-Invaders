import pygame
import random
import math

from constants import *

from Bullets import *

class Firework(Bullet):
    def __init__(self, *group):
        super(Firework, self).__init__(random.randint(-25,25), False, *group)
        
        self.speed = random.randint(4,6)
        self.color = random.randint(0,2)
        self.limit = random.randint(100,200)

        self.index = 0
        self.images = [pygame.image.load("Resources\\Fireworks\\set"+str(self.color)+ "0.png"),
                       pygame.image.load("Resources\\Fireworks\\set"+str(self.color)+ "1.png"),
                       pygame.image.load("Resources\\Fireworks\\set"+str(self.color)+ "2.png"),
                       pygame.image.load("Resources\\Fireworks\\set"+str(self.color)+ "3.png"),
                       pygame.image.load("Resources\\Fireworks\\set"+str(self.color)+ "4.png")]
                       

        self.image = pygame.transform.rotate(self.images[self.index], -self.bend)
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = SCREEN_HEIGHT + random.randint(25,75)

        self.runSound = pygame.mixer.Sound("Resources\\Sounds\\fwrun.wav")
        self.crackSound = pygame.mixer.Sound("Resources\\Sounds\\fwcrack.wav")

        self.ran = False
        self.exploded = False

    def update(self, game):
        if self.rect.y > self.limit:
            super().update(game)
            if not self.ran and self.rect.y > SCREEN_HEIGHT:
                if game.volume:
                    pygame.mixer.Sound.play(self.runSound)
                self.ran = True
        else:
            if not self.exploded:
                if game.volume:
                    pygame.mixer.Sound.play(self.crackSound)
                self.exploded = True
            self.index += 1
            self.image = self.images[self.index]
            if self.index == 4:
                self.kill()

class Missile(Bullet):
    def __init__(self, ship, volume, *group):
        super(Missile, self).__init__(0, False, *group)
        self.image = pygame.image.load("Resources\\Sprites\\missile.png")
        self.rect = self.image.get_rect()
        self.rect.x = ship.rect.x + ship.rect.width//2 - self.rect.width//2
        self.rect.y = ship.rect.y - 10

        self.centered = False
        self.hitted = False
        self.explodeImage = pygame.image.load("Resources\\Sprites\\boom.png")

        self.sideMove = -3
        if self.rect.x + self.rect.width//2 < 300:
            self.sideMove = 3
        
        self.delayHit = 0

        if volume:
            self.initSound = pygame.mixer.Sound("Resources\\Sounds\\cannon.wav")
            pygame.mixer.Sound.play(self.initSound)
        self.explodeSound = pygame.mixer.Sound("Resources\\Sounds\\explosion.wav")

    def update(self, game):
        if 290 < self.rect.x + self.rect.width//2 < 310:
            self.centered = True
        if not self.hitted:
            if not self.centered:
                self.rect.x += self.sideMove
            else:
                self.rect.y -= 8
                self.checkHitAnything(game)
        else:
            if self.delayHit > 60:
                self.kill()
            self.delayHit += 1

    def checkHitAnything(self, game):
        if pygame.sprite.spritecollide(self, game.enemyList, False) or \
           pygame.sprite.spritecollide(self, game.hazardList, False):
            if game.volume:
                pygame.mixer.Sound.play(self.explodeSound)
            game.broken = True
            self.hitted = True
            self.rect.x -= self.explodeImage.get_width()//2 - self.image.get_width()//2
            self.rect.y -= self.explodeImage.get_height()//2 - self.image.get_height()//2
            self.image = self.explodeImage
            for enemy in game.enemyList:
                if enemy.rect.y > 0:
                    game.score += int(enemy.health * game.player.scoreRate)
                    enemy.kill(game, True)
        try:
            if pygame.sprite.collide_rect(self, game.boss):
                if game.volume:
                    pygame.mixer.Sound.play(self.explodeSound)
                self.hitted = True
                self.rect.x -= self.explodeImage.get_width()//2 - self.image.get_width()//2
                self.rect.y -= self.explodeImage.get_height()//2 - self.image.get_height()//2
                self.image = self.explodeImage
                game.boss.health -= game.player.damage * 50
        except AttributeError:
            pass
        
