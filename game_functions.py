import sys

import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(user_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """responds to keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, user_settings, stats, screen, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(user_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y)

def check_play_button(user_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """starts a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset the game settings
        user_settings.initialize_dynamic_settings()

        start_game(user_settings, screen, stats, sb, ship, aliens, bullets)

def start_game(user_settings, screen, stats, sb, ship, aliens, bullets):
    """start a new game when the player clicks play"""
    # hide the mouse cursor
    pygame.mouse.set_visible(False)

    # reset the game statistics
    stats.reset_stats()
    stats.game_active = True

    # reset the scoreboard image
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    # create a new fleet and center the ship
    create_fleet(user_settings, screen, ship, aliens)
    ship.center_ship()


def check_keydown_events(event, user_settings, stats, screen, sb, ship, aliens, bullets):
    """responds to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(user_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(user_settings, screen, stats, sb, ship, aliens, bullets)

def check_keyup_events(event, ship):
    """responds to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def update_screen(user_settings, stats, screen, sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # redraw the color of the screen during each pass through the loop
    screen.fill(user_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)

    # redraw all bullets behind ships and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # draw the score information
    sb.show_score()

    # draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # make the most recently drawn screen visible
    pygame.display.flip()

def update_bullets(user_settings, stats, screen, sb, ship, aliens, bullets):
    """update the position of bullets and get rid of old bullets"""
    # update bullet positions
    bullets.update()
    # get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(user_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(user_settings, screen, stats, sb, ship, aliens, bullets):
    # check for any bullets that have hit aliens
    # if so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += user_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # if the entire fleet is destroyed, start a new level
        bullets.empty()
        user_settings.increase_speed()

        # increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(user_settings, screen, ship, aliens)

def fire_bullet(user_settings, screen, ship, bullets):
    # create new bullet and add it to the bullets group
    if len(bullets) <= user_settings.bullet_allowed:
        new_bullet = Bullet(user_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(user_settings, alien_width):
    """determine the number of aliens that fit in the row"""
    available_space_x = user_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def create_alien(user_settings, screen, aliens, alien_number, row_number):
    """create an alien and place it in the row"""
    alien = Alien(user_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(user_settings, screen, ship, aliens):
    """create a full fleet of aliens"""
    # create an alien and find the number of aliens in a row
    alien = Alien(user_settings, screen)
    number_aliens_x = get_number_aliens_x(user_settings, alien.rect.width)
    number_rows = get_number_rows(user_settings, ship.rect.height,
                                  alien.rect.height)

    # create the fleet of aliens
    for row_number in range(number_rows):
         for alien_number in range(number_aliens_x):
            create_alien(user_settings, screen, aliens, alien_number, row_number)

def get_number_rows(user_settings, ship_height, alien_height):
    """determine the number of rows of aliens that fit on the screen"""
    available_space_y = (user_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(user_settings, stats, screen, sb, ship, aliens, bullets):
    """check if the fleet is at an edge,
    and then update the positions of all aliens in the fleet"""
    check_fleet_edges(user_settings, aliens)
    aliens.update()

    # look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(user_settings, stats, screen, sb, ship, aliens, bullets)

    # look for aliens hitting the bottom of the ship
    check_aliens_bottom(user_settings, stats, screen, sb, ship, aliens, bullets)

def check_fleet_edges(user_settings, aliens):
    """respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(user_settings, aliens)
            break

def change_fleet_direction(user_settings, aliens):
    """drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += user_settings.fleet_drop_speed
    user_settings.fleet_direction *= -1

def ship_hit(user_settings, stats, screen, sb, ship, aliens, bullets):
    """respond to ship being hit by alien"""
    if stats.ships_left > 0:
        # decrement ships left
        stats.ships_left -= 1

        # update scoreboard
        sb.prep_ships()

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create new fleet and center the ship
        create_fleet(user_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(user_settings, stats, screen, sb, ship, aliens, bullets):
    """check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat this the same as if the ship got hit
            ship_hit(user_settings, stats, screen, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()