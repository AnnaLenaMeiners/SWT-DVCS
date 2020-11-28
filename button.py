import pygame.font


class Button:
    """
    A class to represent a button
    ...
    Methods
    -------
    prep_text() - prepare the text to be shown on the button
    draw_button() - draw button to screen
    """

    def __init__(self, screen, settings, text):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.button_color = settings.button_color
        self.text_color = settings.text_color

        self.font = pygame.font.SysFont(None, settings.font_size)

        self.left = self.screen_rect.left + settings.button_left_margin
        self.top = self.screen_rect.top + settings.button_top_margin
        self.width, self.height = settings.button_width, settings.button_height
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

        self.text_image = None
        self.text_image_rect = None

        self.prep_text(text)

    def prep_text(self, text):
        self.text_image = self.font.render(
            text, True, self.text_color, self.button_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)
