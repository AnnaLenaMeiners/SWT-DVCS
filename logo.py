import pygame


class Logo:
    """
    A class to represent the logo on the start screen
    ...
    Methods
    -------
    draw_logo() - draws logo onto screen
    """

    def __init__(self, settings, screen):
        self.image = pygame.image.load(settings.logo_image)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top + settings.logo_top_margin

    def draw_logo(self, screen):
        screen.blit(self.image, self.rect)
