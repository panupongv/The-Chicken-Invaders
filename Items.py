import pygame
import random

import shortcuts

from constants import *

class Box(pygame.sprite.Sprite):
    def __init__(self, y, *group):
        super(Box, self).__init__(*group)
        self.image = pygame.image.load("Resources\\Sprites\\box.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, 590 - self.rect.width)
        self.rect.y = y

    def resetPos(self):
        self.rect.x = random.randint(10, 590 - self.rect.width)
        self.rect.y = -random.randint(1400,1600)

    def update(self, game):
        self.rect.y += 4
        if self.rect.y > SCREEN_HEIGHT + 100:
            self.resetPos()
        if self.checkGotHit(game):
            self.createBonus(game)
            self.resetPos()
            
    def checkGotHit(self, game):
        if pygame.sprite.spritecollide(self, game.bulletList, False):
            return True
        return False

    def createBonus(self, game):
        item = shortcuts.ItemDict().get(random.randint(1,5), self, game.itemList, game.allSpriteList)

class Item(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(Item, self).__init__(*group)
        self.tag = None

    def update(self, game):
        self.rect.y += 3

    def getPower(self, game):
        game.player.scoreRate += 0.25
        itemTag = ItemDisplay(self, self.tag, game.volume, game.allSpriteList)

class PowerUp1(Item):
    def __init__(self, box, *group):
        super(PowerUp1, self).__init__(*group)
        self.image = pygame.image.load("Resources\\Sprites\\getmissile.png")   
        self.rect = self.image.get_rect()
        self.rect.x = box.rect.x
        self.rect.y = box.rect.y
        self.tag = "Resources\\Sprites\\missileready.png"

    def getPower(self, game):
        super().getPower(game)
        game.player.haveSpecial = True

class PowerUp2(Item):
    def __init__(self, box, *group):
        super(PowerUp2, self).__init__(*group)
        self.image = pygame.image.load("Resources\\Sprites\\gethealth.png")
        self.rect = self.image.get_rect()
        self.rect.x = box.rect.x
        self.rect.y = box.rect.y
        self.tag = "Resources\\Sprites\\health++.png"
        
    def getPower(self, game):
        super().getPower(game)
        if game.player.health < 7:
            game.player.health += 1

class PowerUp3(Item):
    def __init__(self, box, *group):
        super(PowerUp3, self).__init__(*group)
        self.image = pygame.image.load("Resources\\Sprites\\getdamage.png")
        self.rect = self.image.get_rect()
        self.rect.x = box.rect.x
        self.rect.y = box.rect.y
        self.tag = "Resources\\Sprites\\damage++.png"

    def getPower(self, game):
        super().getPower(game)
        game.player.damage += 5

class PowerUp4(Item):
    def __init__(self, box, *group):
        super(PowerUp4, self).__init__(*group)
        self.image = pygame.image.load("Resources\\Sprites\\getfirerate.png")
        self.rect = self.image.get_rect()
        self.rect.x = box.rect.x
        self.rect.y = box.rect.y
        self.tag = "Resources\\Sprites\\firerate++.png"

    def getPower(self, game):
        super().getPower(game)
        game.player.fireRate += 1

class PowerUp5(Item):
    def __init__(self, box, *group):
        super(PowerUp5, self).__init__(*group)
        self.image = pygame.image.load("Resources\\Sprites\\getpierce.png")
        self.rect = self.image.get_rect()
        self.rect.x = box.rect.x
        self.rect.y = box.rect.y
        self.tag1 = "Resources\\Sprites\\piercingbullet.png"
        self.tag2 = "Resources\\Sprites\\damage++.png"

    def getPower(self, game):
        game.player.scoreRate += 0.25
        if not game.player.piercing:
            game.player.damage += 1
            game.player.piercing = True
            itemTag = ItemDisplay(self, self.tag1, game.volume, game.allSpriteList)
        else:
            game.player.damage += 5
            itemTag = ItemDisplay(self, self.tag2, game.volume, game.allSpriteList)

class ItemDisplay(pygame.sprite.Sprite):
    def __init__(self, bonus, tag, volume, *group):
        super(ItemDisplay, self).__init__(*group)
        self.counter = 0
        self.image = pygame.image.load(tag)
        self.rect = self.image.get_rect()
        self.rect.x = bonus.rect.x + bonus.rect.width//2 - self.rect.width//2
        self.rect.y = bonus.rect.y

        if volume:
            self.sound = pygame.mixer.Sound("Resources\\Sounds\\coin.wav")
            pygame.mixer.Sound.play(self.sound)

    def update(self, game):
        self.rect.y -= 3
        self.counter += 1
        if self.counter >= 30:
            self.kill()
