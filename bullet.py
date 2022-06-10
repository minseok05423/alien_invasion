import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """a class to manage bullets fired from ship"""

    def __init__(self, user_settings, screen, ship):
        """create bullet object at the ship's current position"""
        super().__init__()
        self.screen = screen

        # create bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0, 0, user_settings.bullet_width,
                                user_settings.bullet_height)

        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = user_settings.bullet_color
        self.speed_factor = user_settings.bullet_speed_factor

    def update(self):
        """move the bullet up the screen"""
        # update the decimal position for bullet
        self.y -= self.speed_factor
        # update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)