import pygame

class Bullet:
    def __init__(self, image, startingPosition, screen):
        self.image = image
        self.rect = image.get_rect().move(startingPosition)
        self.screen = screen
    
    def draw(self):
        self.screen.blit(self.image, self.rect)
    
    def move(self):
        self.rect = self.rect.move((0, -6))