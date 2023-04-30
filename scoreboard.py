import pygame.font
from pygame.sprite import Group

from soldier import Soldier

class Scoreboard:

	def __init__(self, zs_game):
		"""Initialize scoreboard attributes"""
		# Initialize the game screen
		self.zs_game = zs_game
		self.screen = zs_game.screen
		self.screen_rect = zs_game.screen.get_rect()

		# Set the game settings and statistics
		self.settings = zs_game.settings
		self.stats = zs_game.stats

		# Set the scoreboard text and font settings
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# Prepare the scoreboard images
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_soldiers()

	def prep_score(self):
		"""Convert the current score to an image to display on the scoreboard"""
		rounded_score = round(self.stats.score, -1)
		score_str = "Points: {:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color,
			self.settings.bg_color)

		# Position the score image
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		"""Convert the high score to an image to display on the scoreboard"""
		high_score = round(self.stats.high_score, -1)
		high_score_str = "High Score: {:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True, 
			self.text_color, self.settings.bg_color)

		# Position the high score image
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def check_high_score(self):
		"""Check if the current score is higher than the high score"""
		if self.stats.score > self.stats.high_score:
			self.stats.high_score = self.stats.score
			self.prep_high_score()

	def prep_level(self):
		"""Convert the current level to an image to display on the scoreboard"""
		level_str = "Lvl: {}".format(self.stats.level)
		self.level_image = self.font.render(level_str, True, self.text_color,
			self.settings.bg_color)

		# Position the level image
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10

	def prep_soldiers(self):
		"""Create soldier images to display on the scoreboard"""
		self.soldiers = Group()
		for soldier_number in range(self.stats.soldier_left):
			# Create a new soldier image
			soldier = Soldier(self.zs_game)

			# Position the soldier image
			soldier.rect.x = self.high_score_rect.left - 150 - (10 + soldier_number * soldier.rect.width)
			soldier.rect.y = 10

			# Add the soldier image to the group
			self.soldiers.add(soldier)

	def show_score(self):
		"""Draw the scoreboard images to the screen"""
		# Draw the score, high score, level, and soldier images to the screen
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.soldiers.draw(self.screen)

