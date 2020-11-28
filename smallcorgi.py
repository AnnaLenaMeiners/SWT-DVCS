import pygame
from pygame.sprite import Sprite


class SmallCorgi(Sprite):
    """
    A class to represent the small corgis used to indicate how many lives the
    player has got left.
    ...
    Methods
    -------
    blitme() - draws small corgi onto screen
    """

    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        self.image = pygame.image.load('images/smallcorgibutt.png')
        self.rect = self.image.get_rect()

    def blitme(self):
        self.screen.blit(self.image, self.rect)
