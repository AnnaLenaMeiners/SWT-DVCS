import pygame
from pygame.sprite import Group

from smallcorgi import SmallCorgi


class Scoreboard:
    """
    A class to represent the scoreboard
    ...
    Methods
    -------
    prep_score() - prepare current score
    prep_high_score() - prepare high score
    prep_level() - prepare player's current level
    prep_smallcorgis() - prepare small corgis, i.e. player's lives
    """

    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        self.score_image = None
        self.score_rect = None
        self.high_score_image = None
        self.high_score_rect = None
        self.level_image = None
        self.level_rect = None
        self.smallcorgis = None

        self.text_color = settings.score_text_color
        self.font = pygame.font.SysFont(None, settings.score_font_size)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_smallcorgis()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "Your Score: " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color,
            self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = (self.screen_rect.right -
                                self.settings.medium_margin)
        self.score_rect.top = self.settings.medium_margin

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "High Score: " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color,
            self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = (self.screen_rect.left +
                                    self.settings.medium_margin)
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        level_str = "Your Level: " + str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color,
            self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = (self.score_rect.bottom +
                              self.settings.small_margin)

    def prep_smallcorgis(self):
        self.smallcorgis = Group()
        for smallcorgi_number in range(self.stats.corgis_left):
            smallcorgi = SmallCorgi(self.screen)
            smallcorgi.rect.x = (self.settings.small_margin +
                                (smallcorgi_number * smallcorgi.rect.width))
            smallcorgi.rect.y = (self.high_score_rect.bottom +
                                self.settings.small_margin)
            self.smallcorgis.add(smallcorgi)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.smallcorgis.draw(self.screen)
