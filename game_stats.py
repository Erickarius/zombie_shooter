class GameStats:
	def __init__(self, zs_game):
		self.settings = zs_game.settings
		self.reset_stats()
		self.game_active = False

		self.high_score = 0

	def reset_stats(self):
		self.soldier_left = self.settings.soldier_limit
		self.score = 0
		self.level = 1