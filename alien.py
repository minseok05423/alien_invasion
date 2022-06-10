import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """a class to represent a single alien in the fleet"""

    def __init__(self, user_settings, screen):
        super().__init__()
        self.screen = screen
        self.user_settings = user_settings

        # load the alien image and set its rect value
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # store the alien's exact position
        self.x = float(self.rect.x)

    def update(self):
        """move the alien right or left"""
        self.x += (self.user_settings.fleet_direction *
                   self.user_settings.alien_speed_factor)
        self.rect.x = self.x

    def check_edges(self):
        """return true is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



