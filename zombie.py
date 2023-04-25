import pygame
from pygame.sprite import Sprite

class Zombie(Sprite):

	def __init__(self, zs_game, x, y):
		super().__init__()
		self.screen = zs_game.screen
		self.settings = zs_game.settings
		self.image = pygame.image.load('images/zombie.bmp')
		self.rect = self.image.get_rect()
		self.y = y
		self.x = x - self.rect.width

		self.rect.x = self.x
		self.rect.y = self.y


	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if self.rect.top < screen_rect.top:
			return True
		if self.rect.bottom > screen_rect.bottom:
			return True
		return False

	def update(self):
		self.update_y(self.settings.zombie_speed * self.settings.zombies_direction)

	def update_y(self, y):
		self.y += y
		self.rect.y += y

	def update_x(self, x):
		self.x += x
		self.rect.x += x