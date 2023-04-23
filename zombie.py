import pygame
from pygame.sprite import Sprite

class Zombie(Sprite):

	def __init__(self, zs_game):
		super().__init__()
		self.screen = zs_game.screen
		self.image = pygame.image.load('images/zombie.bmp')
		self.rect = self.image.get_rect()

		self.rect.x = self.rect.height
		self.rect.y = self.rect.width

		#Przechowywanie dokładnego poziomu położenia obceg.
		self.y = float(self.rect.y)