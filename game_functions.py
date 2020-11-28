import math
import sys
import pygame

from bork import Bork
from kitty import Kitty

# The following functions contain code for game controls.


def check_events(settings, screen, stats, scoreboard, play_button,
                 kitties, corgi, borks):
    """Handle registration of all available key events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings,
                                 screen, stats, corgi, borks)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, stats, corgi)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats,
                              scoreboard, play_button, corgi,
                              kitties, borks, mouse_x, mouse_y)


def check_keydown_events(event, settings, screen, stats, corgi,
                         borks):
    """Manage key down events for moving the corgi and barking"""
    if event.key == pygame.K_RIGHT and stats.game_active:
        corgi.moving_right = True
    elif event.key == pygame.K_LEFT and stats.game_active:
        corgi.moving_left = True
    elif event.key == pygame.K_SPACE and stats.game_active:
        new_bork = Bork(settings, screen, corgi)
        new_bork.bork_sound.play()
        borks.add(new_bork)


def check_keyup_events(event, stats, corgi):
    """Manage key up event for stopping the corgi"""
    if event.key == pygame.K_RIGHT and stats.game_active:
        corgi.moving_right = False
    elif event.key == pygame.K_LEFT and stats.game_active:
        corgi.moving_left = False


def check_play_button(settings, screen, stats, scoreboard, play_button,
                      corgi, kitties, borks, mouse_x, mouse_y):
    """Register clicking of play button and start game accordingly"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_smallcorgis()

        kitties.empty()
        borks.empty()

        create_army(settings, screen, corgi, kitties)
        corgi.__init__(settings, screen)


def check_high_score(stats, scoreboard):
    """Check whether current score exceeds high score and adapt"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


# The following functions update objects on screen according to changes.

def update_borks(settings, screen, stats, scoreboard, corgi, kitties,
                 borks):
    """Update borks and act on new positions (delete when off screen, check
    for collisions with kitties)"""
    borks.update()

    for bork in borks.copy():
        if bork.rect.bottom <= 0:
            borks.remove(bork)

    check_bork_kitty_collisions(
        settings, screen, stats, scoreboard, corgi, kitties, borks)


def update_kitties(settings, stats, screen, scoreboard, corgi,
                   kitties, borks):
    """Update kitties and act on new positions (hit corgi or screen bottom)"""
    check_army_edges(settings, kitties)
    kitties.update()

    if pygame.sprite.spritecollideany(corgi, kitties):
        corgi_hit(settings, stats, scoreboard,
                  screen, corgi, kitties, borks)

    check_kitties_bottom(settings, stats,
                         scoreboard, screen, corgi, kitties, borks)


def update_screen(settings, screen, stats, scoreboard, corgi, kitties,
                  borks, play_button, logo):
    """update everything drawn on screen"""
    screen.fill(settings.bg_color)

    for bork in borks.sprites():
        bork.display_borks()
    corgi.blitme()
    kitties.draw(screen)
    scoreboard.show_score()

    if not stats.game_active:
        play_button.draw_button()
        logo.draw_logo(screen)

    pygame.display.flip()


# The following functions create the kitty army.

def create_army(settings, screen, corgi, kitties):
    """create rows of kitty sprites depending on screen size"""
    kitty = Kitty(settings, screen)
    number_kitties_per_row = get_number_kitties_per_row(
        settings, kitty.rect.width)
    number_rows = get_number_rows(
        settings, corgi.rect.height, kitty.rect.height)

    for row_number in range(number_rows):
        for kitty_number in range(number_kitties_per_row):
            create_kitty(settings, screen,
                         kitties, kitty_number, row_number)


def get_number_rows(settings, corgi_height, kitty_height):
    """calculate number of rows of kitties fitting to screen"""
    available_space_y = (settings.screen_height -
                         settings.buffer_zone - corgi_height)
    number_rows = math.floor(available_space_y / kitty_height)
    return number_rows


def get_number_kitties_per_row(settings, kitty_width):
    """calculate number of kitties fitting in one row on screen"""
    available_space_x = settings.screen_width
    number_kitties_per_row = math.floor(available_space_x /
                             (settings.kitty_buffer_factor * kitty_width))
    return number_kitties_per_row


def create_kitty(settings, screen, kitties, kitty_number, row_number):
    """create a kitty using a fixed position in the army"""
    kitty = Kitty(settings, screen)
    kitty_width = kitty.rect.width
    kitty.x = kitty_width + (settings.kitty_buffer_factor * kitty_width *
              kitty_number)
    kitty.rect.x = kitty.x
    kitty.rect.y = kitty.rect.height + (settings.kitty_buffer_factor *
                   kitty.rect.height * row_number)
    kitties.add(kitty)


# The following functions control the movement of the kitty army.

def check_army_edges(settings, kitties):
    """checks if army touches screen edges and if so, changes army direction"""
    for kitty in kitties.sprites():
        if kitty.check_edges():
            change_army_direction(settings, kitties)
            break


def change_army_direction(settings, kitties):
    """drops army vertically and changes horizonal movement direction"""
    for kitty in kitties.sprites():
        kitty.rect.y += settings.army_drop_speed
    # 1 means right, -1 means left movement.
    settings.army_direction *= -1


# The following functions serve to register and respond to main game events,
# such as scoring and losing.

def check_bork_kitty_collisions(settings, screen, stats, scoreboard,
                                corgi, kitties, borks):
    """A function to register and react to bork-kitty-collisions
    ...
    This function registers borks hitting kitties, deletes kitties, adjusts
    score and high score (via check_highscore()) if applicable. It also
    responds to a defeated kitty army by increasing the player's level,
    increasing game speed, deleting old borks and creating a new kitty army.
    """
    collisions = pygame.sprite.groupcollide(borks, kitties, True, True)
    for kitties in collisions.values():
        stats.score += settings.kitty_points * len(kitties)
        scoreboard.prep_score()
    check_high_score(stats, scoreboard)

    if len(kitties) == 0:
        stats.level += 1
        scoreboard.prep_level()
        settings.increase_speed()

        borks.empty()
        create_army(settings, screen, corgi, kitties)


def corgi_hit(settings, stats, scoreboard, screen, corgi,
              kitties, borks):
    """React to a corgi being hit by a kitty
    ...
    This function responds when a kitty hits the corgi. If there are corgis
    left, a corgi will be lost, current kitties and borks deleted, a new army
    created and the corgi centered. If there are no corgis left, the game will
    be over."""
    if stats.corgis_left > 1:

        stats.corgis_left -= 1

        scoreboard.prep_smallcorgis()

        kitties.empty()
        borks.empty()

        create_army(settings, screen, corgi, kitties)
        corgi.__init__(settings, screen)

        pygame.time.delay(settings.break_time)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_kitties_bottom(settings, stats, scoreboard, screen, corgi,
                         kitties, borks):
    """React to a kitty reaching screen bottom
    ...
    This function checks whether a kitty has reached the screen bottom. If one
    has, the game should react the same way as if a kitty has hit the corgi,
    i.e. call corgi_hit()."""
    for kitty in kitties.sprites():
        if kitty.rect.bottom >= settings.screen_height:
            corgi_hit(settings, stats, scoreboard,
                      screen, corgi, kitties, borks)
            break
