import pygame

from pygame.sprite import Sprite

class Star(Sprite):
    def __init__(self, screen):
        super().__init__()
        image = pygame.image.load("images/star-half.jpg")
        new_image = pygame.transform.scale(image, (100, 100))
        self.image = new_image
        self.image_rect = self.image.get_rect()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.rect = self.image_rect
