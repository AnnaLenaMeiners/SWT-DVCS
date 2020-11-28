import pygame
from pygame.sprite import Group

import game_functions as gf
from corgi import Corgi
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from logo import Logo
from settings import Settings


def run_game():
    """Run the game
    ...
    This function starts the game. It initializes pygame, instantiates the
    screen, play button, stats, scoreboard, corgi, borks, kitties and an army
    thereof. It then starts the main loop which updates the screen and checks
    for events. When the game is active, it also updates the corgi, the borks
    and the kitties."""
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption(settings.caption)

    logo = Logo(settings, screen)
    play_button = Button(screen, settings, settings.play_button_text)
    stats = GameStats(settings)
    scoreboard = Scoreboard(settings, screen, stats)
    corgi = Corgi(settings, screen)
    borks = Group()
    kitties = Group()

    gf.create_army(settings, screen, corgi, kitties)

    # game loop
    while True:
        gf.update_screen(settings, screen, stats,
                         scoreboard, corgi, kitties, borks, play_button, logo)
        gf.check_events(settings, screen, stats,
                        scoreboard, play_button, kitties, corgi, borks)

        if stats.game_active:
            corgi.update()
            gf.update_borks(settings, screen, stats,
                            scoreboard, corgi, kitties, borks)
            gf.update_kitties(settings, stats, screen,
                              scoreboard, corgi, kitties, borks)


run_game()
