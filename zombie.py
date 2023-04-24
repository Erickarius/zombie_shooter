import pygame
from pygame.sprite import Sprite

class Zombie(Sprite):

	def __init__(self, zs_game):
		super().__init__()
		self.screen = zs_game.screen
		self.settings = zs_game.settings
		self.image = pygame.image.load('images/zombie.bmp')
		self.rect = self.image.get_rect()

		self.rect.x = self.screen.get_width() - self.rect.width
		self.rect.y = 0

		self.y = float(self.rect.y)
	


	def update(self):
		"""Przesunięcie zombiaka w prawo lub w lewo."""
		self.x += self.settings.zombie_speed
		self.rect.x = self.x