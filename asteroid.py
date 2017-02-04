import pygame

class Asteroid:
    def __init__(self, size, image, startingPosition, screen):
        self.size = size
        self.image = image
        self.rect = image.get_rect().move(startingPosition)
        self.screen = screen
    
    def draw(self):
        self.screen.blit(self.image, self.rect)
    
    def move(self):
        self.rect = self.rect.move((0, 1))
        
