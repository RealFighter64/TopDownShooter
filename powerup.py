import pygame

class Powerup:
    def __init__(self, powerupType, image, startingPosition, screen):
        self.powerupType = powerupType
        self.image = image
        self.rect = image.get_rect().move(startingPosition)
        self.screen = screen
    
    def draw(self):
        self.screen.blit(self.image, self.rect)
    
    def move(self):
        self.rect = self.rect.move((0, 2))