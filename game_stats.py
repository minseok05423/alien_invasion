class GameStats():
    """track statistics for alien invasion"""

    def __init__(self, user_settings):
        """initialize statistics"""
        self.user_settings = user_settings
        self.reset_stats()
        # start alien invasion in an active state
        self.game_active = True
        # high score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """initialize statistics that can change during the game"""
        self.ships_left = self.user_settings.ship_limit
        self.score = 0
        self.level = 1
        