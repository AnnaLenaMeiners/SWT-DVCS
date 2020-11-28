class GameStats:
    """A class to keep track of the game status"""
    def __init__(self, settings):
        self.settings = settings

        self.game_active = False
        self.corgis_left = None
        self.score = None
        self.level = None
        self.high_score = 0

        self.reset_stats()

    def reset_stats(self):
        """Reset the game stats to starting values"""
        self.corgis_left = self.settings.corgi_limit
        self.score = 0
        self.level = 1
