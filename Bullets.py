import pygame
import random
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bend, piercing, *group):
        super(Bullet, self).__init__(*group)
        self.bend = bend
        self.piercing = piercing

    def update(self, game):
        try:
            self.rect.y -= math.cos(self.bend * math.pi / 180) * self.speed
            self.rect.x += math.tan(self.bend * math.pi / 180) * self.speed
        except:
            self.bend += 1
            self.rect.y -= math.cos(self.bend * math.pi / 180) * self.speed
            self.rect.x += math.tan(self.bend * math.pi / 180) * self.speed
            
        if self.rect.y <= -self.rect.height:
            self.kill()      

class Bullet1(Bullet):
    def __init__(self, ship, volume, soundType, bend = 0, *group):
        super(Bullet1, self).__init__(bend, ship.piercing, *group)

        self.speed = 30
        
        self.image = pygame.image.load("Resources\\Sprites\\bullet1.png")
        self.image = pygame.transform.rotate(self.image, -self.bend)
        self.rect = self.image.get_rect()
        self.rect.x = ship.rect.x + ship.rect.width//2 - self.rect.width//2
        self.rect.y = ship.rect.y + 10

        if volume:
            if soundType == 1:
                soundRandomer = random.randint(0,2)
                if soundRandomer == 0:
                    self.sound = pygame.mixer.Sound("Resources\\Sounds\\laser.wav")
                elif soundRandomer == 1:
                    self.sound = pygame.mixer.Sound("Resources\\Sounds\\laser2.wav")
                else:
                    self.sound = pygame.mixer.Sound("Resources\\Sounds\\laser3.wav")    
            else:
                self.sound = pygame.mixer.Sound("Resources\\Sounds\\speciallaser.wav")
            pygame.mixer.Sound.play(self.sound)
        
class Bullet2(Bullet):
    def __init__(self, ship, volume, soundType, x, bend = 0, *group):
        super(Bullet2, self).__init__(bend, ship.piercing, *group)

        self.speed = 20
        
        self.image = pygame.image.load("Resources\\Sprites\\bullet2.png")
        self.image = pygame.transform.rotate(self.image, -self.bend)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = ship.rect.y + 25

        if volume:
            self.sound = pygame.mixer.Sound("Resources\\Sounds\\ak.wav")
            if soundType == 1:
                pygame.mixer.Sound.play(self.sound)


class Bullet3(Bullet):
    def __init__(self, ship, volume, soundType, bend = 0, *group):
        super(Bullet3, self).__init__(bend, ship.piercing, *group)

        self.speed = 20
        
        self.image = pygame.image.load("Resources\\Sprites\\bullet3New.png")
        self.image = pygame.transform.rotate(self.image, -self.bend)
        self.rect = self.image.get_rect()
        self.rect.x = ship.rect.x + ship.rect.width//2 - self.rect.width//2
        self.rect.y = ship.rect.y + 10

        if volume:
            self.sound = pygame.mixer.Sound("Resources\\Sounds\\pulse.wav")
            if soundType:
                pygame.mixer.Sound.play(self.sound)
            
class Bullet4(Bullet):
    def __init__(self, ship, volume, soundType, bend = 0, *group):
        super(Bullet4, self).__init__(bend, ship.piercing, *group)

        self.speed = 25
        
        self.image = pygame.image.load("Resources\\Sprites\\bullet4New.png")
        self.image = pygame.transform.rotate(self.image, -self.bend)
        self.rect = self.image.get_rect()
        self.rect.x = ship.rect.x + ship.rect.width//2 - self.rect.width//2
        self.rect.y = ship.rect.y + 10

        if volume:
            if soundType == 1:
                self.sound = pygame.mixer.Sound("Resources\\Sounds\\pulse.wav")
            else:
                self.sound = pygame.mixer.Sound("Resources\\Sounds\\ak.wav")
            pygame.mixer.Sound.play(self.sound)
            
                            
