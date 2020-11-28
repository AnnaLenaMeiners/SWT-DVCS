import pygame
from pygame.sprite import Sprite


class Corgi(Sprite):
    """
    A class to represent the corgi
    ...
    Methods
    -------
    update() - updates the corgi's position
    blitme() - draws corgi on new position
    """

    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load(settings.corgi_image)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # sets starting position of the corgi to bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.corgi_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.corgi_speed

        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)
