import pygame
import random

class Death(pygame.sprite.Sprite):
    def __init__(self, chick, volume, soundType, *group):
        super(Death, self).__init__(*group)
        self.images = []
        for i in range(14):
            self.images.append(pygame.image.load("Resources\\Explode\\"+str(i)+".png"))
        self.index = 0
        self.image = self.images[self.index]
        
        self.rect = self.image.get_rect()
        self.rect.x = chick.rect.x + chick.rect.width//2 - self.rect.width//2
        self.rect.y = chick.rect.y + chick.rect.height//2 - self.rect.height//2

        if volume:
            if soundType == 1:
                soundRandomer = random.randint(0,2)
                if soundRandomer == 0:
                    self.sound = pygame.mixer.Sound("Resources\\Explode\\deathSound.wav")
                elif soundRandomer == 1:
                    self.sound = pygame.mixer.Sound("Resources\\Explode\\deathsound2.wav")
                else:
                    self.sound = pygame.mixer.Sound("Resources\\Explode\\deathsound3.wav")
              
                pygame.mixer.Sound.play(self.sound)
        
    def update(self, game):
        self.index += 1
        self.image = self.images[self.index]
        if self.index == len(self.images) - 1:
            self.kill()

class PlayerDeath(Death):
    def __init__(self, player, volume, soundType, *group):
        super(PlayerDeath, self).__init__(player, 0, soundType, *group)
        self.volume = volume
        
        self.images = []
        for i in range(20):
            self.images.append(pygame.image.load("Resources\\Burst\\" + str(i) + ".png"))
        self.image = self.images[self.index]
        
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + player.rect.width//2 - self.rect.width//2
        self.rect.y = player.rect.y + player.rect.height//2 - self.rect.height//2
        
        if self.volume:
            self.sound = pygame.mixer.Sound("Resources\\Sounds\\crash.wav")
            pygame.mixer.Sound.play(self.sound)

