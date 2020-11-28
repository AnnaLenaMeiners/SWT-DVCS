import pygame
from pygame.sprite import Sprite


class Bork(Sprite):
    """
    A class used to represent the borks

    ...

    Methods
    -------
    update() - Update borks position
    display_borks() - Draw borks to the screen
    """

    def __init__(self, invaders_settings, screen, corgi):
        super(Bork, self).__init__()
        self.screen = screen
        self.invaders_settings = invaders_settings

        self.image = pygame.image.load(invaders_settings.bork_image)
        self.rect = self.image.get_rect()
        self.rect.centerx = corgi.rect.centerx
        self.rect.bottom = corgi.rect.top
        self.y = float(self.rect.y)

        self.speed = invaders_settings.bork_speed

        self.bork_sound = pygame.mixer.Sound(invaders_settings.bork_sound)
        self.bork_sound.set_volume(invaders_settings.sound_volume)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def display_borks(self):
        self.screen.blit(self.image, self.rect)
