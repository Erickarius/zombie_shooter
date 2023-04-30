class GameStats:
    def __init__(self, zs_game):
        """Initialize statistics."""
        self.settings = zs_game.settings
        self.reset_stats()
        self.game_active = False

        # Load the high score from a file
        self.high_score = 0
        self.load_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.soldier_left = self.settings.soldier_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        """Load the high score from a file."""
        filename = 'high_score.txt'
        try:
            with open(filename) as file:
                contents = file.read()
                if contents:
                    self.high_score = int(contents)
                else:
                    self.high_score = 0
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        """Save the high score to a file."""
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

