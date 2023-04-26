class GameStats:
	def __init__(self, zs_game):
		self.settings = zs_game.settings
		self.reset_stats()
		self.game_active = False

	def reset_stats(self):
		self.soldier_left = self.settings.soldier_limit