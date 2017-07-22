import pygame
import math
import sys
import random

from constants import *

class Meteor(pygame.sprite.Sprite):
    index = 0
    def __init__(self, *group):
        super(Meteor, self).__init__(*group)
        self.images = []
        self.images.append(pygame.image.load("Resources\\Sprites\\meteor.png"))
        for i in range(72):
            self.images.append(pygame.transform.rotate(self.images[0], (i + 1)*5))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, 590 - self.rect.width)
        self.rect.y = -1000

        self.passed = False

        self.sound = pygame.mixer.Sound("Resources\\Sounds\\meteorpass.wav")

    def resetPos(self):
        self.rect.x = random.randint(10, 590 - self.rect.width)
        self.rect.y -= 3000
        self.passed = False
        
    def update(self, game):
        self.index = (self.index + 1) % 72
        self.image = self.images[self.index]
        self.rect.y += 15
        if self.rect.y > SCREEN_HEIGHT + 100:
            self.resetPos()
        if not self.passed and self.rect.y > -50:
            if game.volume:
                self.playSound()
            self.passed = True
        if not game.gameOver:
            self.checkHitPlayer(game)
        self.checkHitBullet(game)

    def checkHitPlayer(self, game):
        if pygame.sprite.collide_rect(self, game.player):
            game.player.takeDamage(game)
            self.resetPos()

    def checkHitBullet(self, game):
        pygame.sprite.spritecollide(self, game.bulletList, True)

    def playSound(self):
        pygame.mixer.Sound.play(self.sound)
        self.passed = True

class EggBomb(Meteor):
    def __init__(self, bomber, volume, *group):
        super(EggBomb, self).__init__(*group)
        self.image = pygame.image.load("Resources\\Sprites\\rotten.png")
        
        self.rect = self.image.get_rect()
        self.rect.x = bomber.rect.x + bomber.rect.width//2 - self.rect.width//2
        self.rect.y = bomber.rect.y

        if volume:
            self.sound = pygame.mixer.Sound("Resources\\Sounds\\bounce.wav")
            pygame.mixer.Sound.play(self.sound)

    def update(self, game):
        self.rect.y += 15
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
        self.checkHitPlayer(game)
        self.checkHitBullet(game)

    def checkHitPlayer(self, game):
        if pygame.sprite.collide_rect(self, game.player):
            game.player.takeDamage(game)
            self.kill()

class Fireball(EggBomb):
    def __init__(self, boss, volume, bend, *group):
        super(Fireball, self).__init__(boss, False, *group)

        self.bend = bend

        self.image = pygame.image.load("Resources\\Sprites\\fireball.png")
        self.image = pygame.transform.rotate(self.image, self.bend)
        self.rect = self.image.get_rect()
        self.rect.x = boss.rect.x + boss.rect.width//2 - self.rect.width//2
        self.rect.y = boss.rect.y + boss.rect.height//2 - self.rect.height//2

        if volume:
            self.sound = pygame.mixer.Sound("Resources\\Sounds\\fireball.wav")
            pygame.mixer.Sound.play(self.sound)

    def update(self, game):
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
        self.rect.y += math.cos(self.bend * math.pi / 180) * 15
        self.rect.x += math.tan(self.bend * math.pi / 180) * 15
        if not game.gameOver:
            self.checkHitPlayer(game)
        self.checkHitBullet(game)
