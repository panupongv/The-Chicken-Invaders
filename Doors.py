import pygame

from constants import *

class UpperDoor(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(UpperDoor, self).__init__(*group)
        self.image = pygame.image.load("Resources\\Menus\\upper.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -self.rect.height - 10

        self.sound = pygame.mixer.Sound("Resources\\Sounds\\doorsound.wav")

    def playSound(self):
        pygame.mixer.Sound.play(self.sound)

    def update(self, menu):
        self.rect.y += 20
        if self.rect.y + self.rect.height >= menu.lowerDoor.rect.y + 20:
            menu.done = True

class LowerDoor(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(LowerDoor, self).__init__(*group)
        self.image = pygame.image.load("Resources\\Menus\\lower.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT + 10

    def playSound(self):
        pass

    def update(self, menu):
        self.rect.y -= 20

class SpecialUpperDoor(UpperDoor):
    def __init__(self, *group):
        super(SpecialUpperDoor, self).__init__(*group)
        self.rect.y = 350 - self.rect.height

    def update(self, menu):
        self.rect.y -= 20
        if self.rect.y + self.rect.height < 0 and menu.lowerDoor.rect.y > SCREEN_HEIGHT:
            menu.done = True

class SpecialLowerDoor(LowerDoor):
    def __init__(self, *group):
        super(SpecialLowerDoor, self).__init__(*group)
        self.rect.y = 350

    def update(self, menu):
        self.rect.y += 20
    
