import pygame
from pygame.sprite import Sprite

# This file contains the kitty sprite. Kitties move via the update function to
# the left or to the right depending on a speed factor and their army's
# direction factor. They are displayed via a simple display function. There
# also needs to be a function to check whether a kitty has touched the screens
# left or right edge (check_edges()).


class Kitty(Sprite):
    """
    A class to represent a kitty
    ...
    Methods
    -------
    update() - updates the kitty's position
    display_kitties() - draws kitties on new position
    check_edges() - registers kitty touching the left or right screen edges
        returns true if kitty touches edge
    """

    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load(settings.kitty_image)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.settings.kitty_speed_factor *
                   self.settings.army_direction)
        self.rect.x = self.x

    def display_kitties(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        else:
            return False
