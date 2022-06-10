import stars_functions as f

import pygame
from star_settings import Settings
from pygame.sprite import Group

def run_game():
    pygame.init()
    user_settings = Settings()
    screen = pygame.display.set_mode((user_settings.screen_width, user_settings.screen_height))
    pygame.display.set_caption("counting stars")

    star = Group()

    f.create_stars(user_settings, screen, star)

    while True:
        f.check_events()
        f.update_screen(user_settings, screen, star)


run_game()