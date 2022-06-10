import pygame

import game_functions as gf
from ship import Ship
from settings import Settings
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # initialize game and a screen object
    pygame.init()
    user_settings = Settings()
    screen = pygame.display.set_mode((user_settings.screen_width, user_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # make the play button
    play_button = Button(user_settings, screen, "play")

    # create an instance to store game statistics and create a scoreboard
    stats = GameStats(user_settings)
    sb = Scoreboard(user_settings, screen, stats)
    # make a ship a group of aliens and a group of bullets
    ship = Ship(user_settings, screen)
    bullets = Group()
    aliens = Group()

    # create the fleet of aliens
    gf.create_fleet(user_settings, screen, ship, aliens)

    # start the main loop for the game
    while True:
        gf.check_events(user_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(user_settings, stats, screen, sb, ship, aliens, bullets)
            gf.update_aliens(user_settings, stats,  screen, sb, ship, aliens, bullets)
            gf.update_screen(user_settings, stats, screen, sb, ship, aliens, bullets, play_button)

run_game()
