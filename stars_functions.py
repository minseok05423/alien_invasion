import pygame

import sys

from stars2 import Star
from random import randint


def get_available_x(user_settings, star):
    star_width = star.image_rect.width
    available_x = (user_settings.screen_width - star_width * 2) / star_width
    return int(available_x)

def get_available_y(user_settings, star):
    star_height = star.image_rect.height
    available_y = (user_settings.screen_height - star_height * 2) / star_height
    return int(available_y)

def create_stars(user_settings, screen, star):
    stars = Star(screen)
    number_star_x = int(user_settings.screen_width /
                        (stars.image_rect.width * 2))
    number_star_y = int(user_settings.screen_height /
                        (stars.image_rect.height * 2))
    for x_number in range(number_star_x):
        for y_number in range(number_star_y):
            draw_stars(screen, star, x_number, y_number)

def draw_stars(screen, star, x_number, y_number):
    stars = Star(screen)
    stars_x = stars.image_rect.width * (2 * x_number)
    stars_y = stars.image_rect.height * (2 * y_number)
    stars.image_rect.x = stars_x + randint(-50, 50)
    stars.image_rect.y = stars_y + randint(-50, 50)

    star.add(stars)


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if pygame.K_q:
                sys.exit()

def update_screen(user_settings, screen, star):
    screen.fill(user_settings.bg_color)
    star.draw(screen)
    pygame.display.flip()
